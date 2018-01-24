-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 24, 2018 at 04:25 PM
-- Server version: 10.0.33-MariaDB-0ubuntu0.16.04.1
-- PHP Version: 7.0.22-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hudoc`
--

-- --------------------------------------------------------

--
-- Table structure for table `articles`
--

CREATE TABLE `articles` (
  `Application Number` int(11) NOT NULL,
  `Article Number` float NOT NULL,
  `Protocol` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `case-text`
--

CREATE TABLE `case-text` (
  `Application Number` int(11) NOT NULL,
  `Case Text` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `conclusions`
--

CREATE TABLE `conclusions` (
  `Application Number` int(11) NOT NULL,
  `Conclusion` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `judgements`
--

CREATE TABLE `judgements` (
  `Document Title` text NOT NULL,
  `Application Number` int(11) NOT NULL,
  `Document Type` varchar(16) NOT NULL,
  `Originating Body` text NOT NULL,
  `Date` date NOT NULL,
  `Conclusion` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `keywords`
--

CREATE TABLE `keywords` (
  `Application Number` int(11) NOT NULL,
  `Keyword` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `linked-case-law`
--

CREATE TABLE `linked-case-law` (
  `Application Number` int(11) NOT NULL,
  `Link Number` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `stats`
--

CREATE TABLE `stats` (
  `last_sync` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `articles`
--
ALTER TABLE `articles`
  ADD UNIQUE KEY `ix_uq_art` (`Application Number`,`Article Number`,`Protocol`);

--
-- Indexes for table `case-text`
--
ALTER TABLE `case-text`
  ADD UNIQUE KEY `Application Number` (`Application Number`);

--
-- Indexes for table `conclusions`
--
ALTER TABLE `conclusions`
  ADD UNIQUE KEY `ix_uq_conc` (`Application Number`,`Conclusion`(128));

--
-- Indexes for table `keywords`
--
ALTER TABLE `keywords`
  ADD UNIQUE KEY `ix_uq_keyword` (`Application Number`,`Keyword`(128)) USING BTREE;

--
-- Indexes for table `linked-case-law`
--
ALTER TABLE `linked-case-law`
  ADD UNIQUE KEY `ix_uq_link` (`Application Number`,`Link Number`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
