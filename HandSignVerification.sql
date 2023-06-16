-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Waktu pembuatan: 06 Jan 2023 pada 11.56
-- Versi server: 10.4.21-MariaDB
-- Versi PHP: 7.4.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `HandSignVerification`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `tandatangan`
--

CREATE TABLE `tandatangan` (
  `id_tandatangan` int(11) NOT NULL,
  `nomor_tandatangan` varchar(255) COLLATE latin1_general_ci NOT NULL,
  `content` text COLLATE latin1_general_ci NOT NULL,
  `image` varchar(255) COLLATE latin1_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Dumping data untuk tabel `tandatangan`
--

INSERT INTO `tandatangan` (`id_tandatangan`, `nomor_tandatangan`, `content`, `image`) VALUES
(0, 'ttd1', '', NULL),
(1, 'ttd2', '', NULL),
(2, 'ttd3', '', NULL),
(3, 'ttd4', '', NULL),
(4, 'ttd5', '', NULL),
(5, 'ttd6', '', NULL),
(6, 'ttd7', '', NULL),
(7, 'ttd8\r\n', '', NULL),
(8, 'ttd9', '', NULL),
(9, 'ttd10', '', NULL),
(10, 'ttd11', '', NULL),
(11, 'ttd12', '', NULL),
(12, 'ttd13', '', NULL),
(13, 'ttd14', '', NULL),
(14, 'ttd15', '', NULL),
(16, 'ttd17', '', NULL),
(17, 'ttd18', '', NULL),
(18, 'ttd19', '', NULL),
(19, 'ttd20', '', NULL);

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `tandatangan`
--
ALTER TABLE `tandatangan`
  ADD PRIMARY KEY (`id_tandatangan`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
