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
) ENGINE=InnoDB AUTO_INCREMENT=219 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alarms`
--

LOCK TABLES `alarms` WRITE;
/*!40000 ALTER TABLE `alarms` DISABLE KEYS */;
INSERT INTO `alarms` VALUES (216,'2017-08-21 08:00:00',' get up ',87,-1);
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
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chats`
--

LOCK TABLES `chats` WRITE;
/*!40000 ALTER TABLE `chats` DISABLE KEYS */;
INSERT INTO `chats` VALUES (1,1,-242171399,'t',NULL),(2,1,-188494517,'t',NULL),(3,1,-188149398,'t',NULL),(4,1,-183293264,'t',NULL),(5,1,-164436920,'t',NULL),(6,1,-4506728,'t',NULL),(7,0,62926687,'t',NULL),(8,0,76034823,'t',NULL),(9,0,129962488,'t',NULL),(10,0,131453030,'t',NULL),(11,0,306971735,'t',NULL),(12,0,325188032,'t',NULL),(13,0,379040133,'t',NULL),(14,0,408711677,'t',NULL),(34,0,100001231441202,'m',NULL),(35,1,1585938714810258,'m',NULL),(36,1,1469909653101496,'m',NULL),(37,1,1413022615479390,'m',NULL),(38,1,1482589455162859,'m',NULL),(39,1,1425620214174564,'m',NULL),(45,0,18648845767,'s',NULL),(72,0,4014368160,'k','951b72b51c1361932087a274033545dc52fc7f13d608c0cbed296d341741027f'),(73,0,16786288778,'s',NULL),(74,0,17709147712,'s',NULL),(75,1,3582919522,'k','3c0ad5d375d1c8c79d8f0c6e8bc24f560ef6f851487f72df5d9ac5aa2ff975c3'),(76,1,-242185160,'t',NULL),(77,0,18648845767,'w','18648845767@s.whatsapp.net'),(78,1,88457671503093036,'w','18648845767-1503093036@g.us'),(79,0,100011656953537,'m',NULL),(80,0,382467394,'t',NULL),(81,1,3898003617,'k','75d7794764473b8fb71828c451f230a0abe17181d56f593c845a3be918dcba42'),(82,0,100009792968369,'m',NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chatusers`
--

LOCK TABLES `chatusers` WRITE;
/*!40000 ALTER TABLE `chatusers` DISABLE KEYS */;
INSERT INTO `chatusers` VALUES (2,10,6),(3,4,6),(4,3,6),(5,6,2),(6,6,6),(7,5,6),(8,5,5),(9,6,7),(10,6,1),(11,4,3),(12,5,4),(13,12,11),(14,3,11),(15,9,5),(16,7,3),(17,11,10),(18,2,6),(19,6,4),(20,2,8),(21,5,9),(22,14,13),(23,8,4),(24,1,6),(25,13,12),(26,1,12),(31,34,34),(32,35,34),(33,35,35),(34,35,36),(35,36,34),(36,37,34),(37,36,37),(38,37,38),(39,38,34),(40,39,34),(41,39,39),(42,38,40),(47,35,44),(48,45,46),(63,72,65),(64,73,66),(65,74,67),(66,75,65),(67,76,6),(68,76,84),(69,77,85),(70,78,85),(71,78,86),(72,79,35),(73,80,94),(74,81,65),(75,82,97);
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
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `userId` bigint(20) NOT NULL,
  `text` text COLLATE utf8mb4_bin,
  `fromUser` tinyint(1) NOT NULL DEFAULT '1',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=284 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (7,90,'Hello',1,'2017-08-19 16:51:04'),(8,90,'How\'s life, Andrew? ????',0,'2017-08-19 16:51:04'),(9,90,'can you fix my computer',1,'2017-08-19 16:51:04'),(11,90,'Call me dinn dinn gunga boy',1,'2017-08-19 16:51:04'),(12,90,'Okay, from now on, I\'ll call you dinn dinn gunga boy! ????',0,'2017-08-19 16:51:04'),(13,90,'thank you',1,'2017-08-19 16:51:04'),(15,90,'When is samuel going back to school?',1,'2017-08-19 16:51:04'),(17,90,'Who is the president of the US?',1,'2017-08-19 16:51:04'),(19,90,'what\'s for lunch?',1,'2017-08-19 16:51:04'),(20,90,'What.',0,'2017-08-19 16:51:04'),(21,90,'twinkies or french fries?',1,'2017-08-19 16:51:04'),(23,90,'or how about bananas',1,'2017-08-19 16:51:04'),(24,90,'I LIKE BANANAS',0,'2017-08-19 16:51:04'),(25,90,'what do you like about bananas?',1,'2017-08-19 16:51:04'),(26,90,'Fave word. ????',0,'2017-08-19 16:51:04'),(27,90,'do you have any other favorite words?',1,'2017-08-19 16:51:04'),(153,87,'hi!',1,'2017-08-19 21:16:54'),(154,87,'Good to see you, Samuel! ?',0,'2017-08-19 21:16:54'),(155,87,'how\'s life?',1,'2017-08-19 21:16:57'),(156,87,'Pretty good! Just sitting up here in the cloud, waiting for people to talk to me ?????',0,'2017-08-19 21:16:57'),(157,87,'you\'re so weird',1,'2017-08-19 21:17:00'),(158,87,'haha',1,'2017-08-19 21:17:01'),(159,87,'I know, it\'s so funny, right??',0,'2017-08-19 21:17:01'),(160,87,'sup?',1,'2017-08-19 21:19:07'),(161,87,'Wassup?',0,'2017-08-19 21:19:07'),(162,87,'git status',1,'2017-08-19 23:53:29'),(163,87,'On branch master\nYour branch is up-to-date with \'origin/master\'.\nChanges not staged for commit:\n  (use \"git add/rm <file>...\" to update what will be committed)\n  (use \"git checkout -- <file>...\" to discard changes in working directory)\n\n	modified:   database.py\n	modified:   processes.py\n	modified:   server.py\n	deleted:    static/css/foundations.css\n	modified:   static/css/style.css\n	modified:   static/js/script.js\n	modified:   templates/about.html\n	modified:   templates/chat.html\n	modified:   templates/errors/404.html\n	modified:   templates/errors/500.html\n	modified:   templates/index.html\n	modified:   templates/layout.html\n	modified:   templates/login.html\n	modified:   templates/register.html\n	modified:   templates/users/edit.html\n	modified:   templates/users/index.html\n\nUntracked files:\n  (use \"git add <file>...\" to include in what will be committed)\n\n	res/kik.png\n	res/messenger.png\n	res/sambot.jpg\n	res/settings.png\n	res/telegram.png\n	res/whatsapp.png\n	static/css/foundation.css\n	static/css/foundation.min.css\n	templates/profile.html\n\nno changes added to commit (use \"git add\" and/or \"git commit -a\")\n',0,'2017-08-19 23:53:29'),(164,87,'git status',1,'2017-08-19 23:53:36'),(165,87,'On branch master\nYour branch is up-to-date with \'origin/master\'.\nChanges not staged for commit:\n  (use \"git add/rm <file>...\" to update what will be committed)\n  (use \"git checkout -- <file>...\" to discard changes in working directory)\n\n	modified:   database.py\n	modified:   processes.py\n	modified:   server.py\n	deleted:    static/css/foundations.css\n	modified:   static/css/style.css\n	modified:   static/js/script.js\n	modified:   templates/about.html\n	modified:   templates/chat.html\n	modified:   templates/errors/404.html\n	modified:   templates/errors/500.html\n	modified:   templates/index.html\n	modified:   templates/layout.html\n	modified:   templates/login.html\n	modified:   templates/register.html\n	modified:   templates/users/edit.html\n	modified:   templates/users/index.html\n\nUntracked files:\n  (use \"git add <file>...\" to include in what will be committed)\n\n	res/kik.png\n	res/messenger.png\n	res/sambot.jpg\n	res/settings.png\n	res/telegram.png\n	res/whatsapp.png\n	static/css/foundation.css\n	static/css/foundation.min.css\n	templates/profile.html\n\nno changes added to commit (use \"git add\" and/or \"git commit -a\")\n',0,'2017-08-19 23:53:36'),(166,87,'hi',1,'2017-08-19 23:53:42'),(167,87,'Why hello there, Samuel!',0,'2017-08-19 23:53:42'),(168,87,'how\'s life?',1,'2017-08-20 00:07:27'),(169,87,'Awesome ? I get to live in the sky!!! ',0,'2017-08-20 00:07:27'),(170,87,'haha',1,'2017-08-20 00:07:30'),(171,87,'I know, it\'s so funny, right??',0,'2017-08-20 00:07:30'),(172,87,'lol',1,'2017-08-20 00:08:57'),(173,87,'do you like chicken?',1,'2017-08-20 00:09:01'),(174,87,'Oh my word, I LOVE chicken!',0,'2017-08-20 00:09:01'),(175,87,'hi',1,'2017-08-20 00:09:47'),(176,87,'Why hello there, Samuel!',0,'2017-08-20 00:09:47'),(177,87,'remind me to eat in 2 seconds',1,'2017-08-20 00:10:02'),(178,87,'Okay, I\'ll remind you at Saturday, Aug 19, 2017 at 20:10:04 PM',0,'2017-08-20 00:10:02'),(179,87,'Reminder:  eat ',0,'2017-08-20 00:10:06'),(180,91,'hi!!',1,'2017-08-20 00:16:12'),(181,91,'Good to see you, Benjamin! ?',0,'2017-08-20 00:16:12'),(182,91,'NICE!!',1,'2017-08-20 00:16:17'),(183,91,'Thanks! It\'s pretty nice ?',0,'2017-08-20 00:16:17'),(184,91,'bo',1,'2017-08-20 00:16:20'),(185,91,'bob',1,'2017-08-20 00:16:21'),(186,91,'sambot',1,'2017-08-20 00:16:23'),(187,91,'What can I do for you?',0,'2017-08-20 00:16:23'),(188,91,'say hi',1,'2017-08-20 00:16:29'),(189,91,'Delivered ?',0,'2017-08-20 00:16:29'),(190,91,'say hi sam',1,'2017-08-20 00:16:32'),(191,91,'Delivered ?',0,'2017-08-20 00:16:32'),(192,91,'say this is great',1,'2017-08-20 00:16:37'),(193,91,'Delivered ?',0,'2017-08-20 00:16:37'),(194,91,'hi there sambot!',1,'2017-08-20 00:17:33'),(195,91,'Good to see you, Benjamin! ☺',0,'2017-08-20 00:17:33'),(196,87,'Hi',1,'2017-08-20 00:23:30'),(197,87,'Why hello there, Samuel!',0,'2017-08-20 00:23:30'),(198,87,'Hi',1,'2017-08-20 00:33:57'),(199,87,'Good to see you, Sammy! ?',0,'2017-08-20 00:33:57'),(200,87,'Remind me to be awesome in five seconds ',1,'2017-08-20 01:19:12'),(201,87,'Okay, I\'ll remind you at Saturday, Aug 19, 2017 at 21:19:17 PM',0,'2017-08-20 01:19:12'),(202,87,'Reminder:  be awesome ',0,'2017-08-20 01:19:18'),(203,87,'Tell me the duck story',1,'2017-08-20 01:19:33'),(204,87,'Tell me a joke',1,'2017-08-20 01:19:39'),(205,87,'One day, a brunette was jumping up and down on train tracks shouting \"23!! 23!! 23!!\". A blonde saw her doing this. So because blondes look up to brunettes, the blonde walked up and started copying her, shouting \"23! 23! 23!\". \nThen, out of nowhere, a train started coming. The blonde just kept jumping, but the brunette jumped off. The train ran the blonde over.\nThe brunette jumped back on the train tracks and started shouting \"24!! 24!! 24!!\"',0,'2017-08-20 01:19:39'),(206,87,'Remind me to sack Jonathan when he walks in the door ',1,'2017-08-20 01:20:10'),(207,87,'Commands for reminders (or alarms)\n\"list reminders\": list your reminders in the current chat\n\"list reminders all\": list all your reminders\n\"list reminders chat\": list all reminders in the current chat',0,'2017-08-20 01:20:10'),(208,87,'Remind me to sack Jonathan when he walks by in approximately one minute',1,'2017-08-20 01:20:36'),(209,87,'Commands for reminders (or alarms)\n\"list reminders\": list your reminders in the current chat\n\"list reminders all\": list all your reminders\n\"list reminders chat\": list all reminders in the current chat',0,'2017-08-20 01:20:36'),(210,87,'Remind me to get up and dance in two minutes',1,'2017-08-20 01:20:48'),(211,87,'Okay, I\'ll remind you at Saturday, Aug 19, 2017 at 21:22:48 PM',0,'2017-08-20 01:20:48'),(212,87,'In the meantime, tell me a joke',1,'2017-08-20 01:20:59'),(213,87,'JOKE',1,'2017-08-20 01:21:04'),(214,87,'One day, a brunette was jumping up and down on train tracks shouting \"23!! 23!! 23!!\". A blonde saw her doing this. So because blondes look up to brunettes, the blonde walked up and started copying her, shouting \"23! 23! 23!\". \nThen, out of nowhere, a train started coming. The blonde just kept jumping, but the brunette jumped off. The train ran the blonde over.\nThe brunette jumped back on the train tracks and started shouting \"24!! 24!! 24!!\"',0,'2017-08-20 01:21:04'),(215,87,'DO A DIFFERENT JOKE YOU JERK',1,'2017-08-20 01:21:11'),(216,87,'Gimme a joke',1,'2017-08-20 01:21:17'),(217,87,'Tell me a joke',1,'2017-08-20 01:21:24'),(218,87,'One day, a brunette was jumping up and down on train tracks shouting \"23!! 23!! 23!!\". A blonde saw her doing this. So because blondes look up to brunettes, the blonde walked up and started copying her, shouting \"23! 23! 23!\". \nThen, out of nowhere, a train started coming. The blonde just kept jumping, but the brunette jumped off. The train ran the blonde over.\nThe brunette jumped back on the train tracks and started shouting \"24!! 24!! 24!!\"',0,'2017-08-20 01:21:24'),(219,87,'NO STOP I DON\'T WANT TO SEE THIS ONE AGAIN GO AWAY',1,'2017-08-20 01:21:33'),(220,87,'TELL ME A JOKE',1,'2017-08-20 01:21:40'),(221,87,'Three drunks get into a taxi and tell the driver where to go. The driver has an idea of the address so he starts the engine, waits a few seconds and turns off the car. He says, \"Alright guys we\'re here!\" \nThe first drunk tips him £10 and gets out. \nThe second drunk tips him £20 and gets out. \nThe third drunk then slaps the driver across the face. \nWorried that the drunk had realized the car hadn\'t moved an inch, he asks the drunk, \"What was that for?\" \nThe drunk says, \"Control your speed next time. You almost killed us!\" ',0,'2017-08-20 01:21:40'),(222,87,'Reminder:  get up and dance ',0,'2017-08-20 01:22:49'),(223,87,'bruh',1,'2017-08-20 02:25:42'),(224,87,'What up, brutha?',0,'2017-08-20 02:25:42'),(225,87,'reload',1,'2017-08-20 02:25:47'),(226,87,'Refreshing Response List Done!',0,'2017-08-20 02:25:47'),(227,87,'wow you\'re fast!',1,'2017-08-20 02:25:51'),(228,87,'haha',1,'2017-08-20 02:25:53'),(229,87,'Lol yep',0,'2017-08-20 02:25:53'),(230,87,'remind me to eat in 2 seconds',1,'2017-08-20 03:07:19'),(231,87,'I\'ve added your reminder for Saturday, Aug 19, 2017 at 23:07:21 PM',0,'2017-08-20 03:07:19'),(232,87,'Reminder:  eat ',0,'2017-08-20 03:07:22'),(233,87,'remind me to eat in 2 seconds',1,'2017-08-20 03:14:33'),(234,87,'I\'ve added your reminder for Saturday, Aug 19, 2017 at 23:14:35 PM',0,'2017-08-20 03:14:33'),(235,87,'Reminder for Sammy:  eat ',0,'2017-08-20 03:14:37'),(236,87,'remind me to go to bed in 30 seconds',1,'2017-08-20 03:14:51'),(237,87,'I\'ve added your reminder for Saturday, Aug 19, 2017 at 23:15:21 PM',0,'2017-08-20 03:14:51'),(238,87,'Reminder for Sammy:  go to bed ',0,'2017-08-20 03:15:51'),(239,87,'remind me to go to bed in 30 seconds',1,'2017-08-20 03:24:44'),(240,87,'Okay, I\'ll remind you at Saturday, Aug 19, 2017 at 23:25:14 PM',0,'2017-08-20 03:24:44'),(241,87,'Reminder for Sammy:  go to bed ',0,'2017-08-20 03:25:15'),(242,87,'Reminder for Sammy:  go to bed ',0,'2017-08-20 03:25:25'),(243,87,'remind me to eat in 20 seconds',1,'2017-08-20 03:26:39'),(244,87,'Sounds good! Reminder set for Saturday, Aug 19, 2017 at 23:26:59 PM',0,'2017-08-20 03:26:39'),(245,87,'Reminder for Sammy:  eat ',0,'2017-08-20 03:27:00'),(246,87,'Reminder for Sammy:  eat ',0,'2017-08-20 03:27:19'),(247,87,'remind me to go to bed in 20 seconds',1,'2017-08-20 03:35:51'),(248,87,'Alrighty, there will be a reminder for you at Saturday, Aug 19, 2017 at 23:36:11 PM',0,'2017-08-20 03:35:51'),(249,87,'Reminder for Sammy:  go to bed ',0,'2017-08-20 03:36:12'),(250,87,'Remind me to sleep in 2 minutes',1,'2017-08-20 04:10:00'),(251,87,'Alrighty, there will be a reminder for you at Sunday, Aug 20, 2017 at 00:12:00 AM',0,'2017-08-20 04:10:00'),(252,87,'Reminder for Sammy:  sleep ',0,'2017-08-20 04:12:01'),(253,87,'Remind me to get up at 8:00 tomorrow',1,'2017-08-20 04:19:42'),(254,87,'I\'ve added your reminder for Monday, Aug 21, 2017 at 08:00:00 AM',0,'2017-08-20 04:19:42'),(255,96,'Hey, Sambot!',1,'2017-08-20 12:53:29'),(256,96,'How\'s life, Priscilla ? ☺',0,'2017-08-20 12:53:29'),(257,96,'Pretty good! What\'s the weather today?',1,'2017-08-20 12:53:42'),(258,96,'Couldn\'t get the weather... Try Again?',0,'2017-08-20 12:53:42'),(259,96,'Weather',1,'2017-08-20 12:53:48'),(260,96,'Couldn\'t get the weather... Try Again?',0,'2017-08-20 12:53:48'),(261,96,'Tell me a joke!',1,'2017-08-20 12:53:56'),(262,96,'One day, a brunette was jumping up and down on train tracks shouting \"23!! 23!! 23!!\". A blonde saw her doing this. So because blondes look up to brunettes, the blonde walked up and started copying her, shouting \"23! 23! 23!\". \nThen, out of nowhere, a train started coming. The blonde just kept jumping, but the brunette jumped off. The train ran the blonde over.\nThe brunette jumped back on the train tracks and started shouting \"24!! 24!! 24!!\"',0,'2017-08-20 12:53:56'),(263,96,'Call me Aliss Pickory',1,'2017-08-20 12:54:22'),(264,96,'Okay, from now on, I\'ll call you Aliss Pickory! ?',0,'2017-08-20 12:54:22'),(265,87,'Weather in Syracuse ',1,'2017-08-20 13:17:32'),(266,87,'Couldn\'t get the weather... Try Again?',0,'2017-08-20 13:17:32'),(267,87,'Weather',1,'2017-08-20 13:17:48'),(268,87,'Couldn\'t get the weather... Try Again?',0,'2017-08-20 13:17:48'),(269,87,'Remind me to say hi in 3 minutes',1,'2017-08-20 13:18:33'),(270,87,'Sounds good! Reminder set for Sunday, Aug 20, 2017 at 09:21:33 AM',0,'2017-08-20 13:18:33'),(271,87,'Reminder for Sammy:  say hi ',0,'2017-08-20 13:21:34'),(272,87,'weather',1,'2017-08-20 17:24:54'),(273,87,'It\'s very pretty in her! Great weather for a run ?\nSky is clear today, and it\'s currently 80.6° with cloud coverage at 0% and humidity at 18%.',0,'2017-08-20 17:24:54'),(274,87,'weather ',1,'2017-08-20 17:26:14'),(275,87,'Couldn\'t get the weather... Try Again?',0,'2017-08-20 17:26:14'),(276,87,'weather',1,'2017-08-20 17:26:17'),(277,87,'Couldn\'t get the weather... Try Again?',0,'2017-08-20 17:26:17'),(278,87,'hi',1,'2017-08-20 17:28:16'),(279,87,'How goes it, Sammy? ☺?',0,'2017-08-20 17:28:16'),(280,87,'weather',1,'2017-08-20 17:28:19'),(281,87,'Couldn\'t get the weather... Try Again?',0,'2017-08-20 17:28:19'),(282,87,'weather',1,'2017-08-20 17:29:21'),(283,87,'It\'s quite hot out in McDonough, GA... ? Keep cool and drink lots of water!\nFew clouds today, and it\'s currently 89.6° with cloud coverage at 20% and humidity at 43%.',0,'2017-08-20 17:29:21');
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
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Stephen','Laird','slaird','The Master Commander','nothing',49823246,'t',NULL,NULL,0),(2,'Joel','Sampson','Kurai579','Lurker','nothing',50580697,'t',NULL,NULL,0),(3,'Izaac','Morales','izaabsharp','Izaaaaaaaaaaaac','nothing',62926687,'t',NULL,NULL,0),(4,'Micah','Morrison','micahmo','ha maybe you should check for a space','nothing',76034823,'t',NULL,NULL,0),(5,'Ben','Clum','benclum11','Tim','nothing',129962488,'t',NULL,NULL,0),(6,'Samuel','Henry','SamHenry97','Sam','nothing',131453030,'t',NULL,NULL,1),(7,'Joshua','Donahue','thebruh','Ishmael','nothing',132547477,'t',NULL,NULL,0),(8,'Carter','Shean','Clshean','bae','nothing',287318701,'t',NULL,NULL,0),(9,'Andrew','Miller','andrewm621','bae','nothing',289267895,'t',NULL,NULL,0),(10,'Priscilla','Henry','AlissMarie','Chicken pants eating tacos','nothing',306971735,'t',NULL,NULL,0),(11,'Olivia','Gray','OliviaGray','Oliviabae','nothing',325188032,'t',NULL,NULL,0),(12,'ABHINAV','GAUTAM','gotham13121997','Gotham','nothing',379040133,'t',NULL,NULL,0),(13,'Heather','Henry','HeatherHen','doodle cakes','nothing',408711677,'t',NULL,NULL,0),(34,'Samuel','Henry','SamuelHenry','Sam','nothing',100001231441202,'m',NULL,NULL,1),(35,'Jonathan','Henry','JonathanHenry','not spiderman but Batman','nothing',100011656953537,'m',NULL,NULL,0),(36,'Priscilla','Henry','PriscillaHenry','sassafras pants','nothing',100004862706473,'m',NULL,NULL,0),(37,'Ben','Clum','BenClum','','nothing',100002045836549,'m',NULL,NULL,0),(38,'Bhushan','Khanale','BhushanKhanale','','nothing',100012496657648,'m',NULL,NULL,0),(39,'Mary','Elizabeth Conn','MaryElizabethConn','Mawee','nothing',100013376412188,'m',NULL,NULL,0),(40,'Josiah','Henry','JosiahHenry','@Sam Bot','nothing',100000714780192,'m',NULL,NULL,0),(44,'Keren','Henry','KerenHenry','chicken nuggets','nothing',100008641659261,'m',NULL,NULL,0),(46,'Samuel','Henry','GREENVILLE','Sam','nothing',18648845767,'s',NULL,NULL,1),(65,'Samuel','Henry','samuelhenry97','Sam','nothing',447146351102987856,'k',NULL,NULL,1),(66,'Ben','Clum ','ATLANTA','','nothing',16786288778,'s',NULL,'',0),(67,'Chicken','Gravy','MCDONOUGH','bat woman','nothing',17709147712,'s',NULL,NULL,0),(84,'Jagrit','Sabherwal','jagrit','jaggi','nothing',348527143,'t',NULL,NULL,0),(85,'Sam','Henry','18648845767@s.whatsapp.net','','nothing',18648845767,'w',NULL,'',1),(86,'Jagrit','','918699666256@s.whatsapp.net','','nothing',918699666256,'w',NULL,NULL,0),(87,'Samuel','Henry','samhenry1997','Sammy','',18648845767,'o','$2a$12$XCpzMAS/Gn2doOVOPL2qUugs3DRrc.4LG04OGgI0nMbgoxjoQp30.','smlhnry@gmail.com',1),(90,'Andrew','Henry','ahenry','dinn dinn gunga boy','nothing',0,'o','$2a$12$.GO5D5ufGrTOqAxVZ5LUJOQoNI0mKyXJymhMTHVbiI0Ajc5An.sVi','ahhenry4@juno.com',0),(91,'Benjamin','Clum','bclum032','Ben','nothing',0,'o','$2a$12$5eVHyVdH2YhSCz5c3hmQ/uBlvdpId1d0betm48wT3wbz2JjFy8rhW','benclum11@gmail.com',0),(93,'Shubhankar','Dimri','dimriXD','','nothing',0,'o','$2a$12$qxVc9ON.yY4T.oYGxXnwQuMxtItiGXjltgw5RkdCHzYDeE/tOy2Ry','dimrishubhi@gmail.com',0),(94,'Shubhankar','','dimriXD','','nothing',382467394,'t',NULL,NULL,0),(95,'Tester','Tester','testing','','nothing',0,'o','$2a$12$9rXh2PJSGqyJAlldH1H3tuRDIouZwxUFnyX.8OzZNw9DoY3vHzF7S','testing@testing.test',0),(96,'Priscilla','Henry','P_Henry1','Aliss Pickory','',17709147712,'o','$2a$12$5ysjH6rBZi8m/CAQrrSwMeuMh4PCI1ypZsEFEMIC2lzTmLFBiyyB.','drgnhnry@gmail.com',0),(97,'Zachariah','Nething','ZachariahNething','','nothing',100009792968369,'m',NULL,NULL,0);
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

-- Dump completed on 2017-08-20 15:16:50
