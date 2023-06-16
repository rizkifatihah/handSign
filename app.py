from logging import debug
from flask import Flask, render_template,jsonify,request, redirect, url_for, session
import cv2
from PIL import Image
from io import BytesIO
import numpy as np
from matplotlib import pyplot as plt
import mysql.connector
import tensorflow as tf
from tensorflow import keras
import uuid


app = Flask(__name__)

app.secret_key="handSign"

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="HandSignSignature2023!",
  database="HandSignVerification"
)


modelHandSign = keras.models.load_model("HandSign")


# defining the canny detector function
  
# here weak_th and strong_th are thresholds for
# double thresholding step
def Canny_detector(img, weak_th = None, strong_th = None):

     
    # conversion of image to grayscale
    img = cv2.cvtColor(np.float32(img), cv2.COLOR_BGR2GRAY)
      
    # Noise reduction step
    img = cv2.GaussianBlur(img, (5, 5), 1.4)
      
    # Calculating the gradients
    gx = cv2.Sobel(np.float32(img), cv2.CV_64F, 1, 0, 3)
    gy = cv2.Sobel(np.float32(img), cv2.CV_64F, 0, 1, 3)
     
    # Conversion of Cartesian coordinates to polar
    mag, ang = cv2.cartToPolar(gx, gy, angleInDegrees = True)
      
    # setting the minimum and maximum thresholds
    # for double thresholding
    mag_max = np.max(mag)
    if not weak_th:weak_th = mag_max * 0.1
    if not strong_th:strong_th = mag_max * 0.5
     
    # getting the dimensions of the input image 
    height, width = img.shape
      
    # Looping through every pixel of the grayscale
    # image
    for i_x in range(width):
        for i_y in range(height):
              
            grad_ang = ang[i_y, i_x]
            grad_ang = abs(grad_ang-180) if abs(grad_ang)>180 else abs(grad_ang)
              
            # selecting the neighbours of the target pixel
            # according to the gradient direction
            # In the x axis direction
            if grad_ang<= 22.5:
                neighb_1_x, neighb_1_y = i_x-1, i_y
                neighb_2_x, neighb_2_y = i_x + 1, i_y
             
            # top right (diagonal-1) direction
            elif grad_ang>22.5 and grad_ang<=(22.5 + 45):
                neighb_1_x, neighb_1_y = i_x-1, i_y-1
                neighb_2_x, neighb_2_y = i_x + 1, i_y + 1
             
            # In y-axis direction
            elif grad_ang>(22.5 + 45) and grad_ang<=(22.5 + 90):
                neighb_1_x, neighb_1_y = i_x, i_y-1
                neighb_2_x, neighb_2_y = i_x, i_y + 1
             
            # top left (diagonal-2) direction
            elif grad_ang>(22.5 + 90) and grad_ang<=(22.5 + 135):
                neighb_1_x, neighb_1_y = i_x-1, i_y + 1
                neighb_2_x, neighb_2_y = i_x + 1, i_y-1
             
            # Now it restarts the cycle
            elif grad_ang>(22.5 + 135) and grad_ang<=(22.5 + 180):
                neighb_1_x, neighb_1_y = i_x-1, i_y
                neighb_2_x, neighb_2_y = i_x + 1, i_y
              
            # Non-maximum suppression step
            if width>neighb_1_x>= 0 and height>neighb_1_y>= 0:
                if mag[i_y, i_x]<mag[neighb_1_y, neighb_1_x]:
                    mag[i_y, i_x]= 0
                    continue
  
            if width>neighb_2_x>= 0 and height>neighb_2_y>= 0:
                if mag[i_y, i_x]<mag[neighb_2_y, neighb_2_x]:
                    mag[i_y, i_x]= 0
  
    weak_ids = np.zeros_like(img)
    strong_ids = np.zeros_like(img)             
    ids = np.zeros_like(img)
      
    # double thresholding step
    for i_x in range(width):
        for i_y in range(height):
             
            grad_mag = mag[i_y, i_x]
             
            if grad_mag<weak_th:
                mag[i_y, i_x]= 0
            elif strong_th>grad_mag>= weak_th:
                ids[i_y, i_x]= 1
            else:
                ids[i_y, i_x]= 2
      
      
    # finally returning the magnitude of
    # gradients of edges
    return mag

class_names_hand_sign = ['ttd1','ttd2','ttd3','ttd4','ttd5','ttd6','ttd7','ttd8','ttd9','ttd10','ttd11','ttd12','ttd13','ttd14','ttd15','ttd16','ttd17','ttd18','ttd19','ttd20']

####### API ROUTE #######

# GET

@app.route("/")
def index():
    return "Gilbert Sihura"



@app.route("/classificationHandsign", methods=["POST"])
def classificationHandsign():
    try:
        files = request.files["image"].read()

        image = Image.open(BytesIO(files))

        imagearray = np.array(image)
        
        resized = cv2.resize(imagearray, (360, 360))

        # expected shape=(None, 360, 360, 3)

        # change resized to expected shape
        

        expanded = tf.expand_dims(resized,0)

        predictions = modelHandSign.predict(expanded)
        score = tf.nn.softmax(predictions[0])

        text = "Gambar ini adalah tanda tangan nomor {} dengan tingkat keyakinan {:.2f}%.".format(class_names_hand_sign[np.argmax(score)], 100 * np.max(score))
        index = np.argmax(score)
        tingkatkeyakinan = 100 * np.max(score)
        if tingkatkeyakinan < 70:
            text = "Gambar ini tidak tertera dalam database"
        namaHandSign = class_names_hand_sign[np.argmax(score)]

        mydb.connect()
        
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM tandatangan WHERE id_tandatangan=%s",(int(index),))

        rows = cursor.fetchone()

        cursor.close()
        mydb.close()

        return jsonify({
            "success":True,
            "text":text,
            "dataHandSign":{
                "id_tandatangan":rows[0],
                "nomor_tandatangan":rows[1],
                "content":rows[2],
                "image":rows[3]
            },
            "data":{
                "text":text,
                "score":str(score),
                "index_class":int(index),
                "class_name":class_names_hand_sign,
                "keyakinan":tingkatkeyakinan,
                "klasifikasi":namaHandSign
            }
        })
        

    except Exception as e:

        print(e)
        return jsonify({
            "success":False,
            "msg":str(e)
        })


if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True)

