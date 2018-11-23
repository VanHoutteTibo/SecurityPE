CREATE DATABASE  IF NOT EXISTS `project1` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `project1`;
-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: project1
-- ------------------------------------------------------
-- Server version	5.7.21-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bollen`
--

DROP TABLE IF EXISTS `bollen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bollen` (
  `ID` int(11) NOT NULL,
  `BolID` int(11) DEFAULT NULL,
  `Ronde` int(11) DEFAULT NULL,
  `Status` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_Bollen_Zet1_idx` (`Ronde`),
  CONSTRAINT `fk_Bollen_Zet1` FOREIGN KEY (`Ronde`) REFERENCES `zet` (`Ronde`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bollen`
--

LOCK TABLES `bollen` WRITE;
/*!40000 ALTER TABLE `bollen` DISABLE KEYS */;
/*!40000 ALTER TABLE `bollen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historiek`
--

DROP TABLE IF EXISTS `historiek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `historiek` (
  `Ronde` int(11) NOT NULL,
  `SpelID` int(11) NOT NULL,
  `HistoriekID` int(11) DEFAULT NULL,
  `Datum` date DEFAULT NULL,
  PRIMARY KEY (`Ronde`,`SpelID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historiek`
--

LOCK TABLES `historiek` WRITE;
/*!40000 ALTER TABLE `historiek` DISABLE KEYS */;
/*!40000 ALTER TABLE `historiek` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spel`
--

DROP TABLE IF EXISTS `spel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spel` (
  `SpelID` int(11) NOT NULL AUTO_INCREMENT,
  `Winnaar` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`SpelID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spel`
--

LOCK TABLES `spel` WRITE;
/*!40000 ALTER TABLE `spel` DISABLE KEYS */;
/*!40000 ALTER TABLE `spel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `UserID` int(11) NOT NULL AUTO_INCREMENT,
  `Naam` varchar(45) DEFAULT NULL,
  `Voornaam` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_has_spel`
--

DROP TABLE IF EXISTS `user_has_spel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_has_spel` (
  `User_UserID` int(11) NOT NULL,
  `Spel_SpelID` int(11) NOT NULL,
  PRIMARY KEY (`User_UserID`,`Spel_SpelID`),
  KEY `fk_User_has_Spel_Spel1_idx` (`Spel_SpelID`),
  KEY `fk_User_has_Spel_User1_idx` (`User_UserID`),
  CONSTRAINT `fk_User_has_Spel_Spel1` FOREIGN KEY (`Spel_SpelID`) REFERENCES `spel` (`SpelID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_User_has_Spel_User1` FOREIGN KEY (`User_UserID`) REFERENCES `user` (`UserID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_has_spel`
--

LOCK TABLES `user_has_spel` WRITE;
/*!40000 ALTER TABLE `user_has_spel` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_has_spel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zet`
--

DROP TABLE IF EXISTS `zet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zet` (
  `Ronde` int(11) NOT NULL,
  `SpelID` int(11) NOT NULL,
  `Kleur` varchar(45) DEFAULT NULL,
  `Lichaamsdeel` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Ronde`,`SpelID`),
  KEY `fk_Zet_Spel1_idx` (`SpelID`),
  CONSTRAINT `fk_Zet_Historiek1` FOREIGN KEY (`Ronde`) REFERENCES `historiek` (`Ronde`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Zet_Spel1` FOREIGN KEY (`SpelID`) REFERENCES `spel` (`SpelID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zet`
--

LOCK TABLES `zet` WRITE;
/*!40000 ALTER TABLE `zet` DISABLE KEYS */;
/*!40000 ALTER TABLE `zet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'project1'
--

--
-- Dumping routines for database 'project1'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-12 16:59:02
