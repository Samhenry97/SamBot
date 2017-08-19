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
) ENGINE=InnoDB AUTO_INCREMENT=196 DEFAULT CHARSET=utf8;
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
  `uuid` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chats`
--

LOCK TABLES `chats` WRITE;
/*!40000 ALTER TABLE `chats` DISABLE KEYS */;
INSERT INTO `chats` VALUES (1,1,-242171399,'t',NULL),(2,1,-188494517,'t',NULL),(3,1,-188149398,'t',NULL),(4,1,-183293264,'t',NULL),(5,1,-164436920,'t',NULL),(6,1,-4506728,'t',NULL),(7,0,62926687,'t',NULL),(8,0,76034823,'t',NULL),(9,0,129962488,'t',NULL),(10,0,131453030,'t',NULL),(11,0,306971735,'t',NULL),(12,0,325188032,'t',NULL),(13,0,379040133,'t',NULL),(14,0,408711677,'t',NULL),(34,0,100001231441202,'m',NULL),(35,1,1585938714810258,'m',NULL),(36,1,1469909653101496,'m',NULL),(37,1,1413022615479390,'m',NULL),(38,1,1482589455162859,'m',NULL),(39,1,1425620214174564,'m',NULL),(45,0,18648845767,'s',NULL),(72,0,4014368160,'k','951b72b51c1361932087a274033545dc52fc7f13d608c0cbed296d341741027f'),(73,0,16786288778,'s',NULL),(74,0,17709147712,'s',NULL),(75,1,3582919522,'k','3c0ad5d375d1c8c79d8f0c6e8bc24f560ef6f851487f72df5d9ac5aa2ff975c3'),(76,1,-242185160,'t',NULL),(77,0,18648845767,'w','18648845767@s.whatsapp.net'),(78,1,88457671503093036,'w','18648845767-1503093036@g.us'),(79,0,100011656953537,'m',NULL);
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
  `chatId` bigint(20) NOT NULL,
  `userId` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chatusers`
--

LOCK TABLES `chatusers` WRITE;
/*!40000 ALTER TABLE `chatusers` DISABLE KEYS */;
INSERT INTO `chatusers` VALUES (2,10,6),(3,4,6),(4,3,6),(5,6,2),(6,6,6),(7,5,6),(8,5,5),(9,6,7),(10,6,1),(11,4,3),(12,5,4),(13,12,11),(14,3,11),(15,9,5),(16,7,3),(17,11,10),(18,2,6),(19,6,4),(20,2,8),(21,5,9),(22,14,13),(23,8,4),(24,1,6),(25,13,12),(26,1,12),(31,34,34),(32,35,34),(33,35,35),(34,35,36),(35,36,34),(36,37,34),(37,36,37),(38,37,38),(39,38,34),(40,39,34),(41,39,39),(42,38,40),(47,35,44),(48,45,46),(63,72,65),(64,73,66),(65,74,67),(66,75,65),(67,76,6),(68,76,84),(69,77,85),(70,78,85),(71,78,86),(72,79,35);
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
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
INSERT INTO `likes` VALUES (4,'coding',6),(5,'french fries',6),(6,'chicken',0),(9,'glitter',11),(15,'your face',10),(16,'tacos',10),(17,'chickens',10),(18,'my bros',10),(20,'spotify',10),(21,'pandora',10),(22,'my imaginary sister',10),(23,'you',10),(24,'me',10),(25,'stars',10),(26,'planets',10),(27,'comets',10),(28,'and pianos',10),(29,'python',10),(30,'tacquitos',10),(31,'oreos',10),(32,'serial killers',10),(33,'axe murderers',10),(34,'and argyle socks',10),(35,'rats and potatoes',10),(36,'cookies',4),(37,'puppies',4),(38,'food',4),(39,'sweaters',10),(40,'chicken flamingo turkeys that way potatoes on fridays inside hidden treasuries located in the side of a cliff that crumbled when earth was destroyed',10),(46,'pie',6),(47,'programming',6),(51,'food',6),(53,'piñatas',6),(54,'french fries',6),(55,'bananas',6),(56,'bananas',6),(62,'bananas',34),(64,'unicorns and fluff',36),(65,'chicken',34),(66,'Minecraft',34),(67,'food',6),(68,'chicken',6);
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` bigint(20) NOT NULL,
  `text` text NOT NULL,
  `fromUser` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (7,90,'Hello',1),(8,90,'How\'s life, Andrew? ????',0),(9,90,'can you fix my computer',1),(10,90,'',0),(11,90,'Call me dinn dinn gunga boy',1),(12,90,'Okay, from now on, I\'ll call you dinn dinn gunga boy! ????',0),(13,90,'thank you',1),(14,90,'',0),(15,90,'When is samuel going back to school?',1),(16,90,'',0),(17,90,'Who is the president of the US?',1),(18,90,'',0),(19,90,'what\'s for lunch?',1),(20,90,'What.',0),(21,90,'twinkies or french fries?',1),(22,90,'',0),(23,90,'or how about bananas',1),(24,90,'I LIKE BANANAS',0),(25,90,'what do you like about bananas?',1),(26,90,'Fave word. ????',0),(27,90,'do you have any other favorite words?',1),(28,90,'',0);
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
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
  `password` text,
  `email` text,
  `admin` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Stephen','Laird','slaird','The Master Commander','nothing',49823246,'t',NULL,NULL,0),(2,'Joel','Sampson','Kurai579','Lurker','nothing',50580697,'t',NULL,NULL,0),(3,'Izaac','Morales','izaabsharp','Izaaaaaaaaaaaac','nothing',62926687,'t',NULL,NULL,0),(4,'Micah','Morrison','micahmo','ha maybe you should check for a space','nothing',76034823,'t',NULL,NULL,0),(5,'Ben','Clum','benclum11','Tim','nothing',129962488,'t',NULL,NULL,0),(6,'Samuel','Henry','SamHenry97','Sam','nothing',131453030,'t',NULL,NULL,1),(7,'Joshua','Donahue','thebruh','Ishmael','nothing',132547477,'t',NULL,NULL,0),(8,'Carter','Shean','Clshean','bae','nothing',287318701,'t',NULL,NULL,0),(9,'Andrew','Miller','andrewm621','bae','nothing',289267895,'t',NULL,NULL,0),(10,'Priscilla','Henry','AlissMarie','Chicken pants eating tacos','nothing',306971735,'t',NULL,NULL,0),(11,'Olivia','Gray','OliviaGray','Oliviabae','nothing',325188032,'t',NULL,NULL,0),(12,'ABHINAV','GAUTAM','gotham13121997','Gotham','nothing',379040133,'t',NULL,NULL,0),(13,'Heather','Henry','HeatherHen','doodle cakes','nothing',408711677,'t',NULL,NULL,0),(34,'Samuel','Henry','SamuelHenry','Sam','nothing',100001231441202,'m',NULL,NULL,1),(35,'Jonathan','Henry','JonathanHenry','not spiderman but Batman','nothing',100011656953537,'m',NULL,NULL,0),(36,'Priscilla','Henry','PriscillaHenry','sassafras pants','nothing',100004862706473,'m',NULL,NULL,0),(37,'Ben','Clum','BenClum','','nothing',100002045836549,'m',NULL,NULL,0),(38,'Bhushan','Khanale','BhushanKhanale','','nothing',100012496657648,'m',NULL,NULL,0),(39,'Mary','Elizabeth Conn','MaryElizabethConn','Mawee','nothing',100013376412188,'m',NULL,NULL,0),(40,'Josiah','Henry','JosiahHenry','@Sam Bot','nothing',100000714780192,'m',NULL,NULL,0),(44,'Keren','Henry','KerenHenry','chicken nuggets','nothing',100008641659261,'m',NULL,NULL,0),(46,'Samuel','Henry','GREENVILLE','Sam','nothing',18648845767,'s',NULL,NULL,1),(65,'Samuel','Henry','samuelhenry97','Sam','nothing',447146351102987856,'k',NULL,NULL,1),(66,'Ben','Clum ','ATLANTA','','nothing',16786288778,'s',NULL,'',0),(67,'Chicken','Gravy','MCDONOUGH','bat woman','nothing',17709147712,'s',NULL,NULL,0),(84,'Jagrit','Sabherwal','jagrit','jaggi','nothing',348527143,'t',NULL,NULL,0),(85,'Sam','Henry','18648845767@s.whatsapp.net','','nothing',18648845767,'w',NULL,'',1),(86,'Jagrit','','918699666256@s.whatsapp.net','','nothing',918699666256,'w',NULL,NULL,0),(87,'Samuel','Henry','samhenry1997','','nothing',-1,'o','$2a$12$XCpzMAS/Gn2doOVOPL2qUugs3DRrc.4LG04OGgI0nMbgoxjoQp30.','smlhnry@gmail.com',1),(90,'Andrew','Henry','ahenry','dinn dinn gunga boy','nothing',-1,'o','$2a$12$.GO5D5ufGrTOqAxVZ5LUJOQoNI0mKyXJymhMTHVbiI0Ajc5An.sVi','ahhenry4@juno.com',0);
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

-- Dump completed on 2017-08-19 12:42:21
