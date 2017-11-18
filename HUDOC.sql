SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;


CREATE TABLE `articles` (
  `Application Number` int(11) NOT NULL,
  `Article Number` float NOT NULL,
  `Protocol` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `case-text` (
  `Application Number` int(11) NOT NULL,
  `Case Text` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `conclusions` (
  `Application Number` int(11) NOT NULL,
  `Conclusion` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `judgements` (
  `Document Title` text NOT NULL,
  `Application Number` int(11) NOT NULL,
  `Document Type` enum('HEJUD','HFJUD') NOT NULL,
  `Originating Body` text NOT NULL,
  `Date` date NOT NULL,
  `Conclusion` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `keywords` (
  `Application Number` int(11) NOT NULL,
  `Keyword` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `linked-case-law` (
  `Application Number` int(11) NOT NULL,
  `Link Number` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


ALTER TABLE `articles`
  ADD UNIQUE KEY `ix_uq_art` (`Application Number`,`Article Number`,`Protocol`);

ALTER TABLE `case-text`
  ADD UNIQUE KEY `Application Number` (`Application Number`);

ALTER TABLE `conclusions`
  ADD UNIQUE KEY `ix_uq_conc` (`Application Number`,`Conclusion`(128));

ALTER TABLE `keywords`
  ADD UNIQUE KEY `ix_uq_keyword` (`Application Number`,`Keyword`(128)) USING BTREE;

ALTER TABLE `linked-case-law`
  ADD UNIQUE KEY `ix_uq_link` (`Application Number`,`Link Number`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
