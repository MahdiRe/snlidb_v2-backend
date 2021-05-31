CREATE DATABASE  IF NOT EXISTS `test` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `test`;
-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: test
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.11-MariaDB

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
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `age` int(11) NOT NULL,
  `marks` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1,'සුනිල්',15,75),(2,'නිමල්',15,80),(3,'ලකල්',15,35),(4,'ජනා',15,55),(5,'ප්‍රියා',15,74);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `user_name` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `role` varchar(45) NOT NULL,
  PRIMARY KEY (`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('admin','admin','admin'),('user','user','user');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `word_mappings`
--

DROP TABLE IF EXISTS `word_mappings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `word_mappings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sinhala_word` varchar(45) CHARACTER SET utf8 COLLATE utf8_sinhala_ci NOT NULL,
  `root_word` varchar(45) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `english_word` varchar(45) NOT NULL,
  `semantic_meaning` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `word_mappings`
--

LOCK TABLES `word_mappings` WRITE;
/*!40000 ALTER TABLE `word_mappings` DISABLE KEYS */;
INSERT INTO `word_mappings` VALUES (1,'සිසුවා','සිසුවා','student','table'),(2,'ශිෂ්‍යයා','ශිෂ්‍ය','student','table'),(3,'ශිෂ්යයා','ශිෂ්‍ය','student','table'),(4,'ළමයා','ළමයා','student','table'),(5,'ලමයා','ළමයා','student','table'),(6,'සිසුන්','සිසුන්','student','table'),(7,'නම්','නම','name','column'),(8,'අනන්‍යතාවය','අනන්‍යතා','id','column'),(9,'අනන්‍ය','අනන්‍ය','id','column'),(10,'හැදුනුම','හැඳුනුම','id','column'),(11,'ලිපිනය','ලිපින','address','column'),(12,'වයස්','වයස','age','column'),(13,'ලකුණු','ලකුණ','marks','column'),(14,'ලකුනු','ලකුන','marks','column'),(15,'සියලුම','සියලු','-','neglect'),(16,'සෑම','සෑම','-','neglect'),(17,'ලබාදෙන්න','දෙන්න','SELECT','command'),(18,'මොනවාද​','මොනවාද​','SELECT','command'),(19,'කුමක්ද','කුමක්','SELECT','command'),(20,'කීයද','කීයද','SELECT','command'),(21,'කොපමණද','කොපමණ','SELECT','command'),(22,'මකා','මකන්න','DELETE','command'),(23,'ඉවත්','ඉවත','DELETE','command'),(24,'යාවත්කාලීන','යාවත්කාලීන','UPDATE','command'),(25,'ඇතුළු','ඇතුළු','INSERT','command'),(26,'වෙනස්','වෙනස්','UPDATE','command'),(27,'මාරු','මාරු','UPDATE','command'),(28,'ඇතුලත්','ඇතුලත්','INSERT','command'),(29,'සමාන','සමාන','=','comparison'),(30,'වැඩි','වැඩි','>','comparison'),(31,'හෝවැඩි','හෝවැඩි','>=','comparison'),(32,'අඩු','අඩු','<','comparison'),(33,'හෝඅඩු','හෝඅඩු','<=','comparison'),(34,'සහ','සහ','AND','logic'),(35,'හා','හා','AND','logic'),(36,'හෝ','හෝ','OR','logic'),(37,'මධ්‍යනය ','මධ්‍යන','AVG','aggregate'),(38,'මධ්‍යස්ථය','මධ්‍යස්ථ','AVG','aggregate'),(39,'අඩුම','අඩුම','MIN','aggregate'),(40,'කුඩාම','කුඩාම','MIN','aggregate'),(41,'අවම','අවම','MIN','aggregate'),(42,'උපරිම','උපරිම','MAX','aggregate'),(43,'වැඩිම','වැඩිම','MAX','aggregate'),(44,'විශාලම','විශාලම','MAX','aggregate'),(45,'එකතුව','එකතු','COUNT','aggregate'),(46,'ගණන්','ගණන','COUNT','aggregate'),(47,'ලබාගත්','ලබාගත්','-','neglect'),(48,'නිසා','නිසා','-','neglect'),(49,'ඇත','ඇත','-','neglect'),(50,'බවට','බවට','-','neglect'),(51,'දත්ත','දත්ත','-','neglect'),(52,'තොරතුරු','තොරතුරු','-','neglect'),(53,'විස්තර​','විස්තර​','-','neglect'),(54,'ප්‍රතිඵලය','ප්‍රතිඵල','-','neglect'),(55,'නාමයන්','නාමය','name','column');
/*!40000 ALTER TABLE `word_mappings` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-01  2:14:37
