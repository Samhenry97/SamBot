-- MySQL dump 10.13  Distrib 5.7.12, for Win64 (x86_64)
--
-- Host: localhost    Database: telegram
-- ------------------------------------------------------
-- Server version	5.7.17-log

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
-- Table structure for table `alarms`
--

DROP TABLE IF EXISTS `alarms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alarms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `message` varchar(255) DEFAULT NULL,
  `userId` int(11) NOT NULL,
  `chatId` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_alarm_users` (`userId`),
  CONSTRAINT `fk_alarm_users` FOREIGN KEY (`userId`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alarms`
--

LOCK TABLES `alarms` WRITE;
/*!40000 ALTER TABLE `alarms` DISABLE KEYS */;
INSERT INTO `alarms` VALUES (127,'4754-12-05 17:25:17',NULL,131453030,131453030);
/*!40000 ALTER TABLE `alarms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chats`
--

DROP TABLE IF EXISTS `chats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chats` (
  `id` int(11) NOT NULL,
  `type` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chats`
--

LOCK TABLES `chats` WRITE;
/*!40000 ALTER TABLE `chats` DISABLE KEYS */;
INSERT INTO `chats` VALUES (-188494517,1),(-188149398,1),(-183293264,1),(-164436920,1),(-4506728,1),(62926687,0),(129962488,0),(131453030,0),(306971735,0),(325188032,0);
/*!40000 ALTER TABLE `chats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chatusers`
--

DROP TABLE IF EXISTS `chatusers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chatusers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chatId` int(11) NOT NULL,
  `userId` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_chats` (`chatId`),
  KEY `fk_users` (`userId`),
  CONSTRAINT `fk_chats` FOREIGN KEY (`chatId`) REFERENCES `chats` (`id`),
  CONSTRAINT `fk_users` FOREIGN KEY (`userId`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chatusers`
--

LOCK TABLES `chatusers` WRITE;
/*!40000 ALTER TABLE `chatusers` DISABLE KEYS */;
INSERT INTO `chatusers` VALUES (2,131453030,131453030),(3,-183293264,131453030),(4,-188149398,131453030),(5,-4506728,50580697),(6,-4506728,131453030),(7,-164436920,131453030),(8,-164436920,129962488),(9,-4506728,132547477),(10,-4506728,49823246),(11,-183293264,62926687),(12,-164436920,76034823),(13,325188032,325188032),(14,-188149398,325188032),(15,129962488,129962488),(16,62926687,62926687),(17,306971735,306971735),(18,-188494517,131453030),(19,-4506728,76034823),(20,-188494517,287318701),(21,-164436920,289267895);
/*!40000 ALTER TABLE `chatusers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `likes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `userId` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `user_id_fk` (`userId`),
  CONSTRAINT `user_id_fk` FOREIGN KEY (`userId`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
INSERT INTO `likes` VALUES (4,'coding',131453030),(5,'french fries',131453030),(9,'glitter',325188032),(10,'bananas',131453030),(15,'your face',306971735),(16,'tacos',306971735),(17,'chickens',306971735),(18,'my bros',306971735),(20,'spotify',306971735),(21,'pandora',306971735),(22,'my imaginary sister',306971735),(23,'you',306971735),(24,'me',306971735),(25,'stars',306971735),(26,'planets',306971735),(27,'comets',306971735),(28,'and pianos',306971735),(29,'python',306971735),(30,'tacquitos',306971735),(31,'oreos',306971735),(32,'serial killers',306971735),(33,'axe murderers',306971735),(34,'and argyle socks',306971735),(35,'rats and potatoes',306971735),(36,'cookies',76034823),(37,'puppies',76034823),(38,'food',76034823),(39,'sweaters',306971735),(40,'chicken flamingo turkeys that way potatoes on fridays inside hidden treasuries located in the side of a cliff that crumbled when earth was destroyed',306971735),(44,'olivia',131453030),(45,'bAnAnAs',131453030),(46,'pie',131453030),(47,'programming',131453030),(48,'chicken',131453030),(50,'bananas',131453030),(51,'food',131453030);
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(10) NOT NULL,
  `firstName` varchar(45) NOT NULL,
  `lastName` varchar(45) NOT NULL,
  `userName` varchar(45) NOT NULL,
  `nickName` varchar(45) DEFAULT NULL,
  `waitingFor` varchar(45) DEFAULT 'nothing',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (49823246,'Stephen','Laird','slaird','The Master Commander','nothing'),(50580697,'Joel','Sampson','Kurai579','Lurker','nothing'),(62926687,'Izaac','Morales','izaabsharp','Izaaaaaaaaaaaac','nothing'),(76034823,'Micah','Morrison','micahmo','ha maybe you should check for a space','nothing'),(129962488,'Ben','Clum','benclum11','Tim','nothing'),(131453030,'Samuel','Henry','SamHenry97','Sam','nothing'),(132547477,'Joshua','Donahue','thebruh','Ishmael','nothing'),(287318701,'Carter','Shean','Clshean','bae','nothing'),(289267895,'Andrew','Miller','andrewm621','bae','nothing'),(306971735,'Priscilla','Henry','AlissMarie','Chicken pants eating tacos','nothing'),(325188032,'Olivia','Gray','OliviaGray','Oliviabae','nothing');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-02-09 19:34:36
