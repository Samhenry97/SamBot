-- MySQL dump 10.13  Distrib 5.5.57, for debian-linux-gnu (armv7l)
--
-- Host: localhost    Database: sambot
-- ------------------------------------------------------
-- Server version	5.5.57-0+deb8u1

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
  KEY `fk_alarm_users` (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=142 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alarms`
--

LOCK TABLES `alarms` WRITE;
/*!40000 ALTER TABLE `alarms` DISABLE KEYS */;
/*!40000 ALTER TABLE `alarms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chats`
--

DROP TABLE IF EXISTS `chats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `public` int(11) NOT NULL DEFAULT '0',
  `chatId` bigint(20) NOT NULL,
  `type` char(1) NOT NULL DEFAULT 't',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chats`
--

LOCK TABLES `chats` WRITE;
/*!40000 ALTER TABLE `chats` DISABLE KEYS */;
INSERT INTO `chats` VALUES (1,1,-242171399,'t'),(2,1,-188494517,'t'),(3,1,-188149398,'t'),(4,1,-183293264,'t'),(5,1,-164436920,'t'),(6,1,-4506728,'t'),(7,0,62926687,'t'),(8,0,76034823,'t'),(9,0,129962488,'t'),(10,0,131453030,'t'),(11,0,306971735,'t'),(12,0,325188032,'t'),(13,0,379040133,'t'),(14,0,408711677,'t'),(34,0,100001231441202,'m');
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
  KEY `fk_users` (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chatusers`
--

LOCK TABLES `chatusers` WRITE;
/*!40000 ALTER TABLE `chatusers` DISABLE KEYS */;
INSERT INTO `chatusers` VALUES (2,10,6),(3,4,6),(4,3,6),(5,6,2),(6,6,6),(7,5,6),(8,5,5),(9,6,7),(10,6,1),(11,4,3),(12,5,4),(13,12,11),(14,3,11),(15,9,5),(16,7,3),(17,11,10),(18,2,6),(19,6,4),(20,2,8),(21,5,9),(22,14,13),(23,8,4),(24,1,6),(25,13,12),(26,1,12),(31,34,34);
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
  KEY `user_id_fk` (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
INSERT INTO `likes` VALUES (4,'coding',6),(5,'french fries',6),(6,'chicken',0),(9,'glitter',11),(15,'your face',10),(16,'tacos',10),(17,'chickens',10),(18,'my bros',10),(20,'spotify',10),(21,'pandora',10),(22,'my imaginary sister',10),(23,'you',10),(24,'me',10),(25,'stars',10),(26,'planets',10),(27,'comets',10),(28,'and pianos',10),(29,'python',10),(30,'tacquitos',10),(31,'oreos',10),(32,'serial killers',10),(33,'axe murderers',10),(34,'and argyle socks',10),(35,'rats and potatoes',10),(36,'cookies',4),(37,'puppies',4),(38,'food',4),(39,'sweaters',10),(40,'chicken flamingo turkeys that way potatoes on fridays inside hidden treasuries located in the side of a cliff that crumbled when earth was destroyed',10),(46,'pie',6),(47,'programming',6),(50,'bananas',6),(51,'food',6),(53,'piñatas',6),(54,'french fries',6),(55,'bananas',6),(56,'bananas',6);
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `firstName` varchar(45) NOT NULL,
  `lastName` varchar(45) NOT NULL,
  `userName` varchar(45) NOT NULL,
  `nickName` text NOT NULL,
  `waitingFor` varchar(32) NOT NULL DEFAULT 'nothing',
  `userId` bigint(20) NOT NULL,
  `type` char(1) NOT NULL DEFAULT 't',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Stephen','Laird','slaird','The Master Commander','nothing',49823246,'t'),(2,'Joel','Sampson','Kurai579','Lurker','nothing',50580697,'t'),(3,'Izaac','Morales','izaabsharp','Izaaaaaaaaaaaac','nothing',62926687,'t'),(4,'Micah','Morrison','micahmo','ha maybe you should check for a space','nothing',76034823,'t'),(5,'Ben','Clum','benclum11','Tim','nothing',129962488,'t'),(6,'Samuel','Henry','SamHenry97','frank','nothing',131453030,'t'),(7,'Joshua','Donahue','thebruh','Ishmael','nothing',132547477,'t'),(8,'Carter','Shean','Clshean','bae','nothing',287318701,'t'),(9,'Andrew','Miller','andrewm621','bae','nothing',289267895,'t'),(10,'Priscilla','Henry','AlissMarie','Chicken pants eating tacos','nothing',306971735,'t'),(11,'Olivia','Gray','OliviaGray','Oliviabae','nothing',325188032,'t'),(12,'ABHINAV','GAUTAM','gotham13121997','Gotham','nothing',379040133,'t'),(13,'Heather','Henry','HeatherHen','doodle cakes','nothing',408711677,'t'),(34,'Samuel','Henry','SamuelHenry','Bob','nothing',100001231441202,'m');
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

-- Dump completed on 2017-08-15 13:30:16
