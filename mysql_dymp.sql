-- MySQL dump 10.13  Distrib 5.5.37, for debian-linux-gnu (x86_64)
--
-- Host: f1398afa8bfa20dbd6efefe4106a86aad5c683b2.rackspaceclouddb.com    Database: exhibia
-- ------------------------------------------------------
-- Server version	5.1.73-1

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
-- Table structure for table `account_account`
--

DROP TABLE IF EXISTS `account_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `timezone` varchar(100) NOT NULL,
  `language` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_17b5ed9e` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_account`
--

LOCK TABLES `account_account` WRITE;
/*!40000 ALTER TABLE `account_account` DISABLE KEYS */;
INSERT INTO `account_account` VALUES (11,16,'US/Eastern','en-us'),(12,17,'US/Eastern','en-us'),(13,18,'US/Eastern','en-us'),(14,19,'US/Eastern','en-us'),(15,20,'US/Eastern','en-us'),(16,21,'US/Eastern','en-us'),(17,22,'US/Eastern','en-us'),(18,23,'US/Eastern','en-us'),(19,24,'US/Eastern','en-us'),(20,25,'US/Eastern','en-us'),(21,26,'US/Eastern','en-us'),(22,27,'US/Eastern','en-us'),(23,28,'US/Eastern','en-us');
/*!40000 ALTER TABLE `account_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_passwordreset`
--

DROP TABLE IF EXISTS `account_passwordreset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_passwordreset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `temp_key` varchar(100) NOT NULL,
  `timestamp` datetime NOT NULL,
  `reset` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_passwordreset_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_c98cd813` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_passwordreset`
--

LOCK TABLES `account_passwordreset` WRITE;
/*!40000 ALTER TABLE `account_passwordreset` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_passwordreset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `announcements_announcement`
--

DROP TABLE IF EXISTS `announcements_announcement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `announcements_announcement` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `content` longtext NOT NULL,
  `creator_id` int(11) NOT NULL,
  `creation_date` datetime NOT NULL,
  `site_wide` tinyint(1) NOT NULL,
  `members_only` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `announcements_announcement_f97a5119` (`creator_id`),
  CONSTRAINT `creator_id_refs_id_1b56d8` FOREIGN KEY (`creator_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcements_announcement`
--

LOCK TABLES `announcements_announcement` WRITE;
/*!40000 ALTER TABLE `announcements_announcement` DISABLE KEYS */;
INSERT INTO `announcements_announcement` VALUES (1,'rwrwrwr','rwrwrw',16,'2014-05-13 10:42:56',1,1);
/*!40000 ALTER TABLE `announcements_announcement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auctions_auction`
--

DROP TABLE IF EXISTS `auctions_auction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auctions_auction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_id` varchar(15) NOT NULL,
  `status` varchar(2) NOT NULL,
  `amount_pleged` int(10) unsigned NOT NULL,
  `backers` int(10) unsigned NOT NULL,
  `current_offer` decimal(7,2) NOT NULL,
  `pledge_time` int(10) unsigned NOT NULL,
  `deadline_time` double NOT NULL,
  `bidding_time` smallint(5) unsigned NOT NULL,
  `last_bidder` varchar(30) NOT NULL,
  `last_bidder_member_id` int(11) DEFAULT NULL,
  `last_bid_type` varchar(1) DEFAULT NULL,
  `last_unixtime` double DEFAULT NULL,
  `ended_unixtime` double DEFAULT NULL,
  `created` datetime NOT NULL,
  `in_queue` tinyint(1) NOT NULL,
  `locked` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auctions_auction_67b70d25` (`item_id`),
  KEY `auctions_auction_c9ad71dd` (`status`),
  KEY `auctions_auction_83072cae` (`deadline_time`),
  KEY `auctions_auction_ea029401` (`last_bidder`),
  KEY `auctions_auction_99b91a78` (`last_bidder_member_id`),
  KEY `auctions_auction_7a11c85c` (`last_unixtime`),
  CONSTRAINT `item_id_refs_code_4cb721b8` FOREIGN KEY (`item_id`) REFERENCES `auctions_auctionitem` (`code`),
  CONSTRAINT `last_bidder_member_id_refs_id_21a7916c` FOREIGN KEY (`last_bidder_member_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auctions_auction`
--

LOCK TABLES `auctions_auction` WRITE;
/*!40000 ALTER TABLE `auctions_auction` DISABLE KEYS */;
INSERT INTO `auctions_auction` VALUES (104,'roland-juno-d','f',811,1,0.02,43200,6000,15,'admin',16,'n',1400758197.60408,1400758213.87324,'2014-05-21 03:36:59',0,0),(105,'sladkaya-1999','f',1332,2,0.01,43200,1400748808.13092,120,'vladimir',23,'n',1400837881.98848,1400838003.50443,'2014-05-22 04:50:28',0,0),(109,'roland-juno-d','f',1200,1,0.01,43200,1400758394.28321,20,'vladimir',23,'n',1400837872.84981,1400837894.16388,'2014-05-22 07:30:14',0,0),(110,'roland-juno-d','f',824,1,0.01,43200,1400838074.17721,20,'vladimir',23,'n',1400840171.63529,1400840193.53816,'2014-05-23 05:38:14',0,0),(111,'sladkaya-1999','p',1397,3,0.00,43200,1400838183.51614,120,'',NULL,'n',NULL,NULL,'2014-05-23 05:40:03',0,0),(112,'roland-juno-d','p',824,2,0.00,43200,1400840373.5514,20,'',NULL,'n',NULL,NULL,'2014-05-23 06:16:33',0,0),(113,'exhibia20bids','f',0,0,0.01,43200,12000,120,'admin',16,'n',1401182258.60728,1401271286.39752,'2014-05-27 04:35:19',0,0),(114,'Playstation4','f',0,0,0.01,43200,1.2e+16,120,'admin',16,'n',1401179861.51552,1401271286.43615,'2014-05-27 04:37:27',0,0),(115,'exhibia20bids','p',22,1,0.00,43200,1401271466.4219,120,'',NULL,'n',NULL,NULL,'2014-05-28 06:01:26',0,0),(116,'Playstation4','p',824,1,0.00,43200,1401271466.44581,120,'',NULL,'n',NULL,NULL,'2014-05-28 06:01:26',0,0),(117,'exhibia20bids','p',20,0,0.00,43200,1401271471.44224,120,'',NULL,'n',NULL,NULL,'2014-05-28 06:01:31',0,0);
/*!40000 ALTER TABLE `auctions_auction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auctions_auctionbid`
--

DROP TABLE IF EXISTS `auctions_auctionbid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auctions_auctionbid` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `auction_id` int(11) NOT NULL,
  `bidder_id` int(11) NOT NULL,
  `price` decimal(7,2) NOT NULL,
  `unixtime` double NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auctions_auctionbid_3e820c5c` (`auction_id`),
  KEY `auctions_auctionbid_fce62d6c` (`bidder_id`),
  CONSTRAINT `auction_id_refs_id_34789fd7` FOREIGN KEY (`auction_id`) REFERENCES `auctions_auction` (`id`),
  CONSTRAINT `bidder_id_refs_id_2c8a400b` FOREIGN KEY (`bidder_id`) REFERENCES `profiles_member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auctions_auctionbid`
--

LOCK TABLES `auctions_auctionbid` WRITE;
/*!40000 ALTER TABLE `auctions_auctionbid` DISABLE KEYS */;
INSERT INTO `auctions_auctionbid` VALUES (2,104,16,0.01,1400750538.316,'2014-05-22 05:22:18'),(11,104,23,0.02,1400758197.55911,'2014-05-22 07:29:57'),(12,109,23,0.01,1400837872.84427,'2014-05-23 05:37:52'),(13,105,23,0.01,1400837881.98258,'2014-05-23 05:38:01'),(14,110,23,0.01,1400840171.62927,'2014-05-23 06:16:11'),(15,114,16,0.01,1401179861.51017,'2014-05-27 04:37:41'),(16,113,16,0.01,1401182258.6006,'2014-05-27 05:17:38');
/*!40000 ALTER TABLE `auctions_auctionbid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auctions_auctionitem`
--

DROP TABLE IF EXISTS `auctions_auctionitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auctions_auctionitem` (
  `code` varchar(15) NOT NULL,
  `name` varchar(150) NOT NULL,
  `slug_name` varchar(200) NOT NULL,
  `price` decimal(7,2) NOT NULL,
  `amount` smallint(6) DEFAULT NULL,
  `brand_id` int(11) DEFAULT NULL,
  `pledge_time` int(10) unsigned NOT NULL,
  `showcase_time` int(10) unsigned NOT NULL,
  `bidding_time` smallint(6) NOT NULL,
  `shipping_fee` decimal(7,2) NOT NULL,
  `description` longtext NOT NULL,
  `notes` longtext,
  `last_modified` datetime NOT NULL,
  `created` datetime NOT NULL,
  `image_id` int(11) DEFAULT NULL,
  `giveaway` tinyint(1) NOT NULL,
  `lock_after` int(10) unsigned DEFAULT NULL,
  `newbie` tinyint(1) NOT NULL,
  PRIMARY KEY (`code`),
  UNIQUE KEY `slug_name` (`slug_name`),
  UNIQUE KEY `image_id` (`image_id`),
  KEY `auctions_auctionitem_74876276` (`brand_id`),
  CONSTRAINT `brand_id_refs_id_95b73470` FOREIGN KEY (`brand_id`) REFERENCES `auctions_brand` (`id`),
  CONSTRAINT `image_id_refs_id_41bb01f7` FOREIGN KEY (`image_id`) REFERENCES `auctions_auctionitemimages` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auctions_auctionitem`
--

LOCK TABLES `auctions_auctionitem` WRITE;
/*!40000 ALTER TABLE `auctions_auctionitem` DISABLE KEYS */;
INSERT INTO `auctions_auctionitem` VALUES ('exhibia20bids','ExhibIa 20 Bids','exhibia-20-bids',20.00,NULL,NULL,180,3600,120,1.00,'','','2014-05-28 06:01:31','2014-05-27 04:16:49',6,1,NULL,0),('Playstation4','Playstation4','playstation4',450.00,NULL,3,180,3600,120,10.00,'The PlayStation 4 was released on November 15, 2013.\r\nPS4 enables the greatest game developers in the world to unlock their creativity and push the boundaries of play through a platform that is tuned specifically to their needs\r\nEngage in endless personal challenges between you and your community, and share your epic moments for the world to see\r\nGamers can share their epic triumphs by hitting the \"SHARE button\" on the controller, scan through the last few minutes of gameplay, tag it and return to the game\r\nWith PS Vita, gamers will be able to seamlessly play PS4 games on the beautiful 5-inch display over Wi-Fi in a local environment','','2014-05-28 06:01:26','2014-05-27 04:23:09',7,0,NULL,0),('roland-juno-d','Roland Juno-D','roland-juno-d',800.00,NULL,2,180,3600,20,10.00,'','','2014-05-23 06:16:33','2014-05-21 03:36:39',5,0,NULL,0),('sladkaya-1999','Jazzmaster Lee Ranaldo','jazzmaster-lee-ranaldo',1200.00,NULL,1,180,3600,120,10.00,'','','2014-05-23 05:40:03','2014-05-20 12:48:12',4,0,NULL,0);
/*!40000 ALTER TABLE `auctions_auctionitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auctions_auctionitem_categories`
--

DROP TABLE IF EXISTS `auctions_auctionitem_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auctions_auctionitem_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `auctionitem_id` varchar(15) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auctionitem_id` (`auctionitem_id`,`category_id`),
  KEY `auctions_auctionitem_categories_126c621f` (`auctionitem_id`),
  KEY `auctions_auctionitem_categories_42dc49bc` (`category_id`),
  CONSTRAINT `auctionitem_id_refs_code_2dba8ae3` FOREIGN KEY (`auctionitem_id`) REFERENCES `auctions_auctionitem` (`code`),
  CONSTRAINT `category_id_refs_id_5ea8588c` FOREIGN KEY (`category_id`) REFERENCES `auctions_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auctions_auctionitem_categories`
--

LOCK TABLES `auctions_auctionitem_categories` WRITE;
/*!40000 ALTER TABLE `auctions_auctionitem_categories` DISABLE KEYS */;
INSERT INTO `auctions_auctionitem_categories` VALUES (36,'exhibia20bids',6),(38,'Playstation4',7),(34,'roland-juno-d',5),(31,'sladkaya-1999',4);
/*!40000 ALTER TABLE `auctions_auctionitem_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auctions_auctionitemimages`
--

DROP TABLE IF EXISTS `auctions_auctionitemimages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auctions_auctionitemimages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_id` varchar(15) NOT NULL,
  `img` varchar(100) NOT NULL,
  `is_default` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auctions_auctionitemimages_67b70d25` (`item_id`),
  CONSTRAINT `item_id_refs_code_2d906c51` FOREIGN KEY (`item_id`) REFERENCES `auctions_auctionitem` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auctions_auctionitemimages`
--

LOCK TABLES `auctions_auctionitemimages` WRITE;
/*!40000 ALTER TABLE `auctions_auctionitemimages` DISABLE KEYS */;
INSERT INTO `auctions_auctionitemimages` VALUES (4,'sladkaya-1999','Lee_Ranaldo_Jazzmaster_SZ9386945_1.jpg',1),(5,'roland-juno-d','top_L.jpg',1),(6,'exhibia20bids','20bids.jpg',1),(7,'Playstation4','playstation4.jpg',1);
/*!40000 ALTER TABLE `auctions_auctionitemimages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auctions_auctionplegde`
--

DROP TABLE IF EXISTS `auctions_auctionplegde`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auctions_auctionplegde` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `auction_id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  `amount` decimal(7,2) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auctions_auctionplegde_3e820c5c` (`auction_id`),
  KEY `auctions_auctionplegde_56e38b98` (`member_id`),
  CONSTRAINT `auction_id_refs_id_37abf5f8` FOREIGN KEY (`auction_id`) REFERENCES `auctions_auction` (`id`),
  CONSTRAINT `member_id_refs_id_83efa144` FOREIGN KEY (`member_id`) REFERENCES `profiles_member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auctions_auctionplegde`
--

LOCK TABLES `auctions_auctionplegde` WRITE;
/*!40000 ALTER TABLE `auctions_auctionplegde` DISABLE KEYS */;
INSERT INTO `auctions_auctionplegde` VALUES (60,105,16,224.00,'2014-05-22 04:51:15'),(61,105,16,224.00,'2014-05-22 04:51:21'),(62,105,16,224.00,'2014-05-22 04:53:02'),(63,105,16,10.00,'2014-05-22 04:53:17'),(64,105,16,10.00,'2014-05-22 04:54:51'),(65,105,16,600.00,'2014-05-22 04:57:31'),(66,105,16,55.00,'2014-05-22 04:59:00'),(67,105,16,22.00,'2014-05-22 05:03:23'),(68,105,16,112.00,'2014-05-22 05:05:12'),(69,105,16,224.00,'2014-05-22 05:05:20'),(70,105,16,600.00,'2014-05-22 05:05:51'),(71,104,16,10.00,'2014-05-22 05:07:37'),(72,104,16,112.00,'2014-05-22 05:07:44'),(73,104,16,10.00,'2014-05-22 05:07:51'),(74,104,16,22.00,'2014-05-22 05:07:56'),(75,104,16,600.00,'2014-05-22 05:08:01'),(76,104,16,10.00,'2014-05-22 05:10:04'),(77,104,16,600.00,'2014-05-22 05:10:11'),(78,104,16,600.00,'2014-05-22 05:13:07'),(79,104,16,112.00,'2014-05-22 05:13:15'),(80,104,16,55.00,'2014-05-22 05:15:41'),(81,104,16,22.00,'2014-05-22 05:15:45'),(82,104,16,22.00,'2014-05-22 05:15:50'),(92,109,16,600.00,'2014-05-22 07:38:46'),(93,109,16,600.00,'2014-05-22 07:38:50'),(94,105,23,600.00,'2014-05-22 09:56:42'),(95,105,23,55.00,'2014-05-22 09:56:52'),(96,105,23,22.00,'2014-05-22 09:58:21'),(97,105,23,55.00,'2014-05-22 09:59:08'),(98,105,16,600.00,'2014-05-22 09:59:17'),(99,110,23,224.00,'2014-05-23 06:08:33'),(100,110,23,600.00,'2014-05-23 06:09:18'),(101,112,23,224.00,'2014-05-23 07:19:43'),(102,111,23,22.00,'2014-05-23 07:19:48'),(103,111,24,10.00,'2014-05-23 07:25:05'),(104,111,23,55.00,'2014-05-23 08:15:09'),(105,111,23,55.00,'2014-05-26 04:34:43'),(106,111,16,600.00,'2014-05-27 04:40:12'),(107,111,16,600.00,'2014-05-27 04:40:29'),(108,112,16,600.00,'2014-05-27 04:43:44'),(109,111,16,55.00,'2014-05-27 05:18:01'),(110,115,16,22.00,'2014-05-28 06:13:14'),(111,116,16,224.00,'2014-05-28 06:15:37'),(112,116,16,600.00,'2014-05-28 06:15:45');
/*!40000 ALTER TABLE `auctions_auctionplegde` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auctions_brand`
--

DROP TABLE IF EXISTS `auctions_brand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auctions_brand` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `slug` varchar(250) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auctions_brand`
--

LOCK TABLES `auctions_brand` WRITE;
/*!40000 ALTER TABLE `auctions_brand` DISABLE KEYS */;
INSERT INTO `auctions_brand` VALUES (1,'Fender','fender'),(2,'Roland','roland'),(3,'Sony','sony');
/*!40000 ALTER TABLE `auctions_brand` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auctions_category`
--

DROP TABLE IF EXISTS `auctions_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auctions_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `slug` varchar(250) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auctions_category`
--

LOCK TABLES `auctions_category` WRITE;
/*!40000 ALTER TABLE `auctions_category` DISABLE KEYS */;
INSERT INTO `auctions_category` VALUES (4,'Electric Guitars','electric-guitars'),(5,'Synthetizers','synthetizers'),(6,'Giftcards','Giftcards'),(7,'Gaming','Gaming');
/*!40000 ALTER TABLE `auctions_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_bda51c3c` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_a7792de1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auth_message_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_9af0b65a` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=189 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add message',5,'add_message'),(14,'Can change message',5,'change_message'),(15,'Can delete message',5,'delete_message'),(16,'Can add banned ip address',6,'add_bannedipaddress'),(17,'Can change banned ip address',6,'change_bannedipaddress'),(18,'Can delete banned ip address',6,'delete_bannedipaddress'),(19,'Can add content type',7,'add_contenttype'),(20,'Can change content type',7,'change_contenttype'),(21,'Can delete content type',7,'delete_contenttype'),(22,'Can add session',8,'add_session'),(23,'Can change session',8,'change_session'),(24,'Can delete session',8,'delete_session'),(25,'Can add site',9,'add_site'),(26,'Can change site',9,'change_site'),(27,'Can delete site',9,'delete_site'),(28,'Can add flat page',10,'add_flatpage'),(29,'Can change flat page',10,'change_flatpage'),(30,'Can delete flat page',10,'delete_flatpage'),(31,'Can add notice type',11,'add_noticetype'),(32,'Can change notice type',11,'change_noticetype'),(33,'Can delete notice type',11,'delete_noticetype'),(34,'Can add notice setting',12,'add_noticesetting'),(35,'Can change notice setting',12,'change_noticesetting'),(36,'Can delete notice setting',12,'delete_noticesetting'),(37,'Can add notice',13,'add_notice'),(38,'Can change notice',13,'change_notice'),(39,'Can delete notice',13,'delete_notice'),(40,'Can add notice queue batch',14,'add_noticequeuebatch'),(41,'Can change notice queue batch',14,'change_noticequeuebatch'),(42,'Can delete notice queue batch',14,'delete_noticequeuebatch'),(43,'Can add observed item',15,'add_observeditem'),(44,'Can change observed item',15,'change_observeditem'),(45,'Can delete observed item',15,'delete_observeditem'),(46,'Can add message',16,'add_message'),(47,'Can change message',16,'change_message'),(48,'Can delete message',16,'delete_message'),(49,'Can add don\'t send entry',17,'add_dontsendentry'),(50,'Can change don\'t send entry',17,'change_dontsendentry'),(51,'Can delete don\'t send entry',17,'delete_dontsendentry'),(52,'Can add message log',18,'add_messagelog'),(53,'Can change message log',18,'change_messagelog'),(54,'Can delete message log',18,'delete_messagelog'),(55,'Can add email address',19,'add_emailaddress'),(56,'Can change email address',19,'change_emailaddress'),(57,'Can delete email address',19,'delete_emailaddress'),(58,'Can add email confirmation',20,'add_emailconfirmation'),(59,'Can change email confirmation',20,'change_emailconfirmation'),(60,'Can delete email confirmation',20,'delete_emailconfirmation'),(61,'Can add announcement',21,'add_announcement'),(62,'Can change announcement',21,'change_announcement'),(63,'Can delete announcement',21,'delete_announcement'),(64,'Can add migration history',22,'add_migrationhistory'),(65,'Can change migration history',22,'change_migrationhistory'),(66,'Can delete migration history',22,'delete_migrationhistory'),(67,'Can add user social auth',23,'add_usersocialauth'),(68,'Can change user social auth',23,'change_usersocialauth'),(69,'Can delete user social auth',23,'delete_usersocialauth'),(70,'Can add nonce',24,'add_nonce'),(71,'Can change nonce',24,'change_nonce'),(72,'Can delete nonce',24,'delete_nonce'),(73,'Can add association',25,'add_association'),(74,'Can change association',25,'change_association'),(75,'Can delete association',25,'delete_association'),(76,'Can add account',26,'add_account'),(77,'Can change account',26,'change_account'),(78,'Can delete account',26,'delete_account'),(79,'Can add password reset',27,'add_passwordreset'),(80,'Can change password reset',27,'change_passwordreset'),(81,'Can delete password reset',27,'delete_passwordreset'),(82,'Can add signup code',28,'add_signupcode'),(83,'Can change signup code',28,'change_signupcode'),(84,'Can delete signup code',28,'delete_signupcode'),(85,'Can add signup code result',29,'add_signupcoderesult'),(86,'Can change signup code result',29,'change_signupcoderesult'),(87,'Can delete signup code result',29,'delete_signupcoderesult'),(88,'Can add setting',30,'add_setting'),(89,'Can change setting',30,'change_setting'),(90,'Can delete setting',30,'delete_setting'),(91,'Can add member',31,'add_member'),(92,'Can change member',31,'change_member'),(93,'Can delete member',31,'delete_member'),(94,'Can edit member settings',31,'can_edit_member_settings'),(95,'Can add billing address',32,'add_billingaddress'),(96,'Can change billing address',32,'change_billingaddress'),(97,'Can delete billing address',32,'delete_billingaddress'),(98,'Can add ip address',33,'add_ipaddress'),(99,'Can change ip address',33,'change_ipaddress'),(100,'Can delete ip address',33,'delete_ipaddress'),(101,'Can add brand',34,'add_brand'),(102,'Can change brand',34,'change_brand'),(103,'Can delete brand',34,'delete_brand'),(104,'Can add Category',35,'add_category'),(105,'Can change Category',35,'change_category'),(106,'Can delete Category',35,'delete_category'),(107,'Can add auction item',36,'add_auctionitem'),(108,'Can change auction item',36,'change_auctionitem'),(109,'Can delete auction item',36,'delete_auctionitem'),(110,'Can add auction',37,'add_auction'),(111,'Can change auction',37,'change_auction'),(112,'Can delete auction',37,'delete_auction'),(113,'Can add auction bid',38,'add_auctionbid'),(114,'Can change auction bid',38,'change_auctionbid'),(115,'Can delete auction bid',38,'delete_auctionbid'),(116,'Can add auction item image',39,'add_auctionitemimages'),(117,'Can change auction item image',39,'change_auctionitemimages'),(118,'Can delete auction item image',39,'delete_auctionitemimages'),(119,'Can add auction plegde',40,'add_auctionplegde'),(120,'Can change auction plegde',40,'change_auctionplegde'),(121,'Can delete auction plegde',40,'delete_auctionplegde'),(122,'Can add video',41,'add_video'),(123,'Can change video',41,'change_video'),(124,'Can delete video',41,'delete_video'),(125,'Can add auction item',42,'add_auctionitem'),(126,'Can change auction item',42,'change_auctionitem'),(127,'Can delete auction item',42,'delete_auctionitem'),(128,'Can add auction item images',43,'add_auctionitemimages'),(129,'Can change auction item images',43,'change_auctionitemimages'),(130,'Can delete auction item images',43,'delete_auctionitemimages'),(131,'Can add payment notification',44,'add_paymentnotification'),(132,'Can change payment notification',44,'change_paymentnotification'),(133,'Can delete payment notification',44,'delete_paymentnotification'),(134,'Can add credit package order',45,'add_creditpackageorder'),(135,'Can change credit package order',45,'change_creditpackageorder'),(136,'Can delete credit package order',45,'delete_creditpackageorder'),(137,'Can add auction order',46,'add_auctionorder'),(138,'Can change auction order',46,'change_auctionorder'),(139,'Can delete auction order',46,'delete_auctionorder'),(140,'Can add card',47,'add_card'),(141,'Can change card',47,'change_card'),(142,'Can delete card',47,'delete_card'),(143,'Can add shipping address',48,'add_shippingaddress'),(144,'Can change shipping address',48,'change_shippingaddress'),(145,'Can delete shipping address',48,'delete_shippingaddress'),(146,'Can add shipping fee',49,'add_shippingfee'),(147,'Can change shipping fee',49,'change_shippingfee'),(148,'Can delete shipping fee',49,'delete_shippingfee'),(149,'Can add shipping request',50,'add_shippingrequest'),(150,'Can change shipping request',50,'change_shippingrequest'),(151,'Can delete shipping request',50,'delete_shippingrequest'),(152,'Can add order',51,'add_order'),(153,'Can change order',51,'change_order'),(154,'Can delete order',51,'delete_order'),(155,'Can add like item',52,'add_likeitem'),(156,'Can change like item',52,'change_likeitem'),(157,'Can delete like item',52,'delete_likeitem'),(158,'Can add invitation',53,'add_invitation'),(159,'Can change invitation',53,'change_invitation'),(160,'Can delete invitation',53,'delete_invitation'),(161,'Can add referral link',54,'add_referrallink'),(162,'Can change referral link',54,'change_referrallink'),(163,'Can delete referral link',54,'delete_referrallink'),(164,'Can add store item',55,'add_storeitem'),(165,'Can change store item',55,'change_storeitem'),(166,'Can delete store item',55,'delete_storeitem'),(167,'Can add bought item',56,'add_boughtitem'),(168,'Can change bought item',56,'change_boughtitem'),(169,'Can delete bought item',56,'delete_boughtitem'),(170,'Can add nonce',57,'add_nonce'),(171,'Can change nonce',57,'change_nonce'),(172,'Can delete nonce',57,'delete_nonce'),(173,'Can add association',58,'add_association'),(174,'Can change association',58,'change_association'),(175,'Can delete association',58,'delete_association'),(176,'Can add user openid association',59,'add_useropenidassociation'),(177,'Can change user openid association',59,'change_useropenidassociation'),(178,'Can delete user openid association',59,'delete_useropenidassociation'),(179,'Can add source',60,'add_source'),(180,'Can change source',60,'change_source'),(181,'Can delete source',60,'delete_source'),(182,'Can add thumbnail',61,'add_thumbnail'),(183,'Can change thumbnail',61,'change_thumbnail'),(184,'Can delete thumbnail',61,'delete_thumbnail'),(185,'Can add Redis Server',62,'add_redisserver'),(186,'Can change Redis Server',62,'change_redisserver'),(187,'Can delete Redis Server',62,'delete_redisserver'),(188,'Can inspect redis servers',62,'can_inspect');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (16,'admin','Anthony','Poddubny','anthony.poddubny@gmail.com','sha1$b40d7$f7127e3999be99fdff19964b759ae1f377debdc5',1,1,1,'2014-05-28 05:58:10','2014-05-12 11:55:58'),(17,'user','','','u@u.com','sha1$30aa0$c0f7cf8d1ef3532e0b56310532ff6edb8d04e0c3',0,1,1,'2014-05-16 08:12:48','2014-05-13 08:06:42'),(18,'user1','','','u1@u1.com','sha1$51bfb$6976cdd112caa7cef046770b31996deeceee97b0',1,1,1,'2014-05-19 09:28:15','2014-05-14 09:40:39'),(19,'user2','','','u2@u2.com','sha1$eaa60$661eb0af8e372f622a5b1090eb8b99c726b6ac92',1,1,1,'2014-05-28 06:11:56','2014-05-14 09:40:56'),(20,'user3','','','u3@u3.com','sha1$faefc$a6340643a6376458e07647545684cccdc5b0d4e3',1,1,1,'2014-05-14 09:41:18','2014-05-14 09:41:18'),(21,'user4','','','u4@u4.com','sha1$8d662$30ec79c2d450873c3165e056027bf152ba37512e',1,1,1,'2014-05-14 09:41:38','2014-05-14 09:41:38'),(22,'user10','','','u10@u10.com','sha1$5720f$56bb419d8b4edc863425b7faa12057c6c8e30109',1,1,1,'2014-05-15 04:41:35','2014-05-15 03:58:02'),(23,'vladimir','','','v@abclosute.com','sha1$83e27$faca1e7e50fd5b03268c43b433b2d97ac635453c',1,1,1,'2014-05-26 04:34:09','2014-05-22 05:23:38'),(24,'АртемДавыдов','Артем','Давыдов','a@abcsolute.com','!',0,1,0,'2014-05-23 07:24:25','2014-05-23 07:24:25'),(25,'iuriy.budnikov','Iuriy','Budnikov','spek91@mail.ru','!',0,1,0,'2014-05-23 07:46:00','2014-05-23 07:46:00'),(26,'artiom.davydov','Артем','Давыдов','artiom.davydov@gmail.com','!',0,1,0,'2014-05-27 06:03:17','2014-05-26 08:22:17'),(27,'nicoexhibia','Nico','Nicco','nicoexhibia@gmail.com','!',0,1,0,'2014-05-27 06:05:27','2014-05-27 06:05:27'),(28,'AnthonyPoddubny','Anthony','Poddubny','anthony.poddubny@gmail.com','!',0,1,0,'2014-05-27 08:36:44','2014-05-27 08:36:44');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_fbfc09f1` (`user_id`),
  KEY `auth_user_groups_bda51c3c` (`group_id`),
  CONSTRAINT `group_id_refs_id_f0ee9890` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_831107f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_fbfc09f1` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_f2045483` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bidin_auctionitem`
--

DROP TABLE IF EXISTS `bidin_auctionitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bidin_auctionitem` (
  `code` varchar(15) NOT NULL,
  `price` double NOT NULL,
  `name` varchar(150) NOT NULL,
  `name_slug` varchar(200) NOT NULL,
  `cashback1` smallint(5) unsigned DEFAULT NULL,
  `cashback2` smallint(5) unsigned DEFAULT NULL,
  `bidding_time` smallint(5) unsigned NOT NULL,
  `description` longtext NOT NULL,
  `amount` smallint(5) unsigned NOT NULL,
  `shipping_fee` double NOT NULL,
  `notes` longtext,
  `meta_title` varchar(300) NOT NULL,
  `meta_description` varchar(300) NOT NULL,
  `buyitnow` tinyint(1) NOT NULL,
  `last_modified` datetime NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`code`),
  UNIQUE KEY `name_slug` (`name_slug`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bidin_auctionitem`
--

LOCK TABLES `bidin_auctionitem` WRITE;
/*!40000 ALTER TABLE `bidin_auctionitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `bidin_auctionitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bidin_auctionitemimages`
--

DROP TABLE IF EXISTS `bidin_auctionitemimages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bidin_auctionitemimages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_id` varchar(15) NOT NULL,
  `img` varchar(100) NOT NULL,
  `is_default` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bidin_auctionitemimages_67b70d25` (`item_id`),
  CONSTRAINT `item_id_refs_code_29d95651` FOREIGN KEY (`item_id`) REFERENCES `bidin_auctionitem` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bidin_auctionitemimages`
--

LOCK TABLES `bidin_auctionitemimages` WRITE;
/*!40000 ALTER TABLE `bidin_auctionitemimages` DISABLE KEYS */;
/*!40000 ALTER TABLE `bidin_auctionitemimages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `checkout_order`
--

DROP TABLE IF EXISTS `checkout_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `checkout_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `auction_id` int(11) NOT NULL,
  `card_id` int(11) NOT NULL,
  `tracking_number` varchar(25) DEFAULT NULL,
  `shipping_company` varchar(5) NOT NULL,
  `shipping_fee_id` int(11) NOT NULL,
  `status` varchar(2) NOT NULL,
  `shipping_first_name` varchar(50) NOT NULL,
  `shipping_last_name` varchar(50) NOT NULL,
  `shipping_address1` varchar(100) NOT NULL,
  `shipping_address2` varchar(100) NOT NULL,
  `shipping_city` varchar(100) NOT NULL,
  `shipping_state` varchar(30) NOT NULL,
  `shipping_country` varchar(2) NOT NULL,
  `shipping_zip_code` varchar(10) NOT NULL,
  `shipping_phone` varchar(30) NOT NULL,
  `billing_first_name` varchar(50) NOT NULL,
  `billing_last_name` varchar(50) NOT NULL,
  `billing_address1` varchar(100) NOT NULL,
  `billing_address2` varchar(100) NOT NULL,
  `billing_city` varchar(100) NOT NULL,
  `billing_state` varchar(30) NOT NULL,
  `billing_country` varchar(2) NOT NULL,
  `billing_zip_code` varchar(10) NOT NULL,
  `billing_phone` varchar(30) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `checkout_order_user_id_30afad675b123fa2_uniq` (`user_id`,`auction_id`),
  KEY `checkout_order_fbfc09f1` (`user_id`),
  KEY `checkout_order_3e820c5c` (`auction_id`),
  KEY `checkout_order_bbe27cfa` (`card_id`),
  KEY `checkout_order_2826514d` (`shipping_fee_id`),
  CONSTRAINT `auction_id_refs_id_2e7a3c68ac1c3798` FOREIGN KEY (`auction_id`) REFERENCES `auctions_auction` (`id`),
  CONSTRAINT `card_id_refs_id_5d0573ced1d74b7b` FOREIGN KEY (`card_id`) REFERENCES `payments_card` (`id`),
  CONSTRAINT `shipping_fee_id_refs_id_a8666b094b78057` FOREIGN KEY (`shipping_fee_id`) REFERENCES `shipping_shippingfee` (`id`),
  CONSTRAINT `user_id_refs_id_6abbfa5fa34ddcf1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `checkout_order`
--

LOCK TABLES `checkout_order` WRITE;
/*!40000 ALTER TABLE `checkout_order` DISABLE KEYS */;
INSERT INTO `checkout_order` VALUES (1,23,117,4,NULL,'True',5,'op','Anthony','Poddubny','Kharkiv','fsfs','Kharkiv','AL','UA','61045','063-897-4469','Anthony','Poddubny','Kharkiv','Kharkiv','Kharkiv','AL','UA','61045','063-897-4469','2014-05-27 05:41:11'),(2,23,119,4,NULL,'True',6,'op','Anthony','Poddubny','Kharkiv','fsfs','Kharkiv','AL','UA','61045','063-897-4469','Anthony','Poddubny','Kharkiv','Kharkiv','Kharkiv','AL','UA','61045','063-897-4469','2014-05-27 05:41:30'),(3,16,119,3,NULL,'True',5,'op','Vladimir','Tsyupko','Kremenchuk','','Poltava','AK','AX','61009','063-897-4469','Anthony','Poddubny','Kharkiv','Kharkiv','Kharkiv','AL','UA','61045','063-897-4469','2014-05-27 05:41:50');
/*!40000 ALTER TABLE `checkout_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dbsettings_setting`
--

DROP TABLE IF EXISTS `dbsettings_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbsettings_setting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `site_id` int(11) NOT NULL,
  `module_name` varchar(255) NOT NULL,
  `class_name` varchar(255) NOT NULL,
  `attribute_name` varchar(255) NOT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `dbsettings_setting_6223029` (`site_id`),
  CONSTRAINT `site_id_refs_id_fbf3c6e7` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dbsettings_setting`
--

LOCK TABLES `dbsettings_setting` WRITE;
/*!40000 ALTER TABLE `dbsettings_setting` DISABLE KEYS */;
/*!40000 ALTER TABLE `dbsettings_setting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_fbfc09f1` (`user_id`),
  KEY `django_admin_log_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=237 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2014-05-12 11:56:44',16,35,'1','gjgjgjg',1,''),(2,'2014-05-12 11:56:55',16,36,'5353535','dgdg g',1,''),(3,'2014-05-12 11:57:17',16,37,'1','dgdg g',1,''),(4,'2014-05-12 12:23:35',16,36,'3535','sfsfs',1,''),(5,'2014-05-12 12:24:30',16,37,'3','dgdg g',1,''),(6,'2014-05-12 12:24:54',16,37,'4','sfsfs',1,''),(7,'2014-05-13 03:20:55',16,37,'1','dgdg g',2,'Changed in_queue.'),(8,'2014-05-13 03:23:23',16,37,'4','sfsfs',2,'Changed in_queue.'),(9,'2014-05-13 03:23:26',16,37,'1','dgdg g',2,'Changed in_queue.'),(10,'2014-05-13 03:50:49',16,37,'4','sfsfs',2,'Changed status.'),(11,'2014-05-13 04:04:56',16,37,'3','dgdg g',2,'Changed status.'),(12,'2014-05-13 04:05:42',16,36,'adsadad-ad','addadad',1,''),(13,'2014-05-13 04:05:53',16,37,'5','addadad',1,''),(14,'2014-05-13 04:06:27',16,37,'3','dgdg g',2,'Changed status.'),(15,'2014-05-13 04:52:21',16,37,'5','addadad',2,'Changed status and amount_pleged.'),(16,'2014-05-13 04:52:39',16,37,'4','sfsfs',2,'Changed status and amount_pleged.'),(17,'2014-05-13 05:15:13',16,37,'5','addadad',3,''),(18,'2014-05-13 05:15:13',16,37,'4','sfsfs',3,''),(19,'2014-05-13 05:15:13',16,37,'3','dgdg g',3,''),(20,'2014-05-13 05:15:13',16,37,'2','sfsfs',3,''),(21,'2014-05-13 05:15:13',16,37,'1','dgdg g',3,''),(22,'2014-05-13 05:16:45',16,36,'5353535','dgdg g',2,'Changed giveaway.'),(23,'2014-05-13 05:17:07',16,36,'3535','sfsfs',2,'Changed bidding_time.'),(24,'2014-05-13 05:18:24',16,37,'7','dgdg g',2,'Changed bidding_time and last_bidder.'),(25,'2014-05-13 05:18:48',16,37,'7','dgdg g',2,'Changed bidding_time.'),(26,'2014-05-13 05:19:58',16,37,'8','addadad',1,''),(27,'2014-05-13 06:06:24',16,37,'8','addadad',2,'Changed last_unixtime and ended_unixtime.'),(28,'2014-05-13 06:29:39',16,62,'1','chat (localhost:6379)',1,''),(29,'2014-05-13 06:44:23',16,37,'6','sfsfs',2,'Changed bidding_time and last_bidder.'),(30,'2014-05-13 07:56:17',16,37,'15','sfsfs',3,''),(31,'2014-05-13 07:56:17',16,37,'14','addadad',3,''),(32,'2014-05-13 07:56:17',16,37,'13','dgdg g',3,''),(33,'2014-05-13 07:56:17',16,37,'12','addadad',3,''),(34,'2014-05-13 07:56:17',16,37,'11','dgdg g',3,''),(35,'2014-05-13 07:56:17',16,37,'10','addadad',3,''),(36,'2014-05-13 07:56:17',16,37,'9','addadad',3,''),(37,'2014-05-13 07:56:17',16,37,'8','addadad',3,''),(38,'2014-05-13 07:56:17',16,37,'7','dgdg g',3,''),(39,'2014-05-13 07:56:17',16,37,'6','sfsfs',3,''),(40,'2014-05-13 07:56:57',16,36,'adsadad-ad','1 item',2,'Changed name.'),(41,'2014-05-13 07:57:10',16,36,'5353535','item 2',2,'Changed name and amount.'),(42,'2014-05-13 07:57:23',16,36,'3535','3 item ',2,'Changed name and giveaway.'),(43,'2014-05-13 08:01:01',16,37,'17','1 item',1,''),(44,'2014-05-13 08:02:15',16,37,'17','1 item',3,''),(45,'2014-05-13 08:02:49',16,37,'18','1 item',1,''),(46,'2014-05-13 08:25:54',16,37,'22','1 item',3,''),(47,'2014-05-13 08:25:54',16,37,'21','item 2',3,''),(48,'2014-05-13 08:25:54',16,37,'20','item 2',3,''),(49,'2014-05-13 08:25:54',16,37,'19','1 item',3,''),(50,'2014-05-13 08:25:54',16,37,'18','1 item',3,''),(51,'2014-05-13 08:25:54',16,37,'16','item 2',3,''),(52,'2014-05-13 08:28:47',16,37,'23','item 2',2,'Changed bidding_time.'),(53,'2014-05-13 09:00:44',16,36,'adsadad-ad','1 item',2,'Changed giveaway.'),(54,'2014-05-13 09:00:44',16,36,'3535','3 item ',2,'Changed giveaway.'),(55,'2014-05-13 09:00:59',16,36,'3535','3 item ',2,'Changed giveaway.'),(56,'2014-05-13 09:04:46',16,37,'23','item 2',2,'Changed status and ended_unixtime.'),(57,'2014-05-13 09:31:16',16,36,'563456','464',1,''),(58,'2014-05-13 09:50:09',16,36,'456363','fsfsfsfsfsf',1,''),(59,'2014-05-13 09:51:39',16,36,'456363','2fsfsfsfsfsf222',2,'Changed name and slug_name.'),(60,'2014-05-13 09:54:35',16,36,'ARARARARR','ARARARARAR!!!!!',1,''),(61,'2014-05-13 09:56:18',16,36,'1321','EEEEEEE',1,''),(62,'2014-05-13 09:57:10',16,36,'YYYYYYYYYY','YYYYYYYYYYY',1,''),(63,'2014-05-13 10:02:09',16,36,'7878798798','Djaga-Djaga',1,''),(64,'2014-05-13 10:28:44',16,37,'24','1 item',2,'Changed status.'),(65,'2014-05-13 10:42:57',16,21,'1','rwrwrwr',1,''),(66,'2014-05-14 03:19:21',16,6,'1','127.0.0.1',1,''),(67,'2014-05-14 03:19:49',16,6,'1','127.0.0.1',3,''),(68,'2014-05-14 04:57:17',16,23,'1','admin - Facebook',1,''),(69,'2014-05-14 04:57:36',16,23,'2','user - Twitter',1,''),(70,'2014-05-14 04:57:52',16,23,'3','user - Facebook',1,''),(71,'2014-05-14 04:58:08',16,23,'4','admin - Twitter',1,''),(72,'2014-05-14 04:58:28',16,23,'1','admin - Facebook',2,'Changed uid.'),(73,'2014-05-14 08:41:02',16,36,'YYYYYYYYYY','YYYYYYYYYYY',2,'Changed lock_after.'),(74,'2014-05-14 09:01:20',16,36,'YYYYYYYYYY','YYYYYYYYYYY',2,'Changed description and giveaway.'),(75,'2014-05-14 09:01:25',16,36,'ARARARARR','ARARARARAR!!!!!',2,'Changed giveaway.'),(76,'2014-05-14 09:01:30',16,36,'7878798798','Djaga-Djaga',2,'Changed giveaway.'),(77,'2014-05-14 09:01:38',16,36,'456363','2fsfsfsfsfsf222',2,'Changed giveaway.'),(78,'2014-05-14 09:39:55',16,37,'27','Djaga-Djaga',2,'Changed bidding_time and locked.'),(79,'2014-05-14 09:44:41',16,36,'7878798798','Djaga-Djaga',2,'Changed lock_after.'),(80,'2014-05-14 09:47:30',16,37,'27','Djaga-Djaga',2,'Changed locked.'),(81,'2014-05-15 03:38:02',16,36,'7878798798','Djaga-Djaga',2,'Changed newbie.'),(82,'2014-05-15 11:31:39',16,37,'23','item 2',3,''),(83,'2014-05-16 03:44:55',16,4,'17','user',2,'Changed is_staff. Changed is_banned for member \"user\".'),(84,'2014-05-16 03:46:04',16,4,'17','user',2,'Changed is_banned for member \"user\".'),(85,'2014-05-16 05:35:50',16,4,'17','user',2,'Changed is_banned for member \"user\".'),(86,'2014-05-16 08:00:20',16,4,'17','user',2,'No fields changed.'),(87,'2014-05-16 09:00:28',16,55,'1','1 lasts - 244, cost - 4646',1,''),(88,'2014-05-16 09:00:47',16,56,'1','user10 - 1 lasts - 244, cost - 4646',1,''),(89,'2014-05-16 11:29:45',16,35,'2','fgdgdg',1,''),(90,'2014-05-16 11:29:57',16,35,'3','dgdgfdg!!!!!!!!!!!1',1,''),(91,'2014-05-19 03:14:10',16,37,'59','YYYYYYYYYYY',2,'Changed status.'),(92,'2014-05-19 03:29:59',16,36,'7878798798','Djaga-Djaga',2,'Added auction item image \"191798v4-max-250x250_1.jpg\".'),(93,'2014-05-19 03:31:36',16,36,'ARARARARR','ARARARARAR!!!!!',2,'Added auction item image \"001.png\".'),(94,'2014-05-19 03:38:50',16,36,'7878798798','Djaga-Djaga',2,'Changed bidding_time.'),(95,'2014-05-19 03:40:20',16,38,'109','Djaga-Djaga : admin ',1,''),(96,'2014-05-19 08:41:55',16,37,'62','2fsfsfsfsfsf222',2,'Changed last_unixtime.'),(97,'2014-05-19 09:00:13',16,36,'456363','2fsfsfsfsfsf222',2,'Changed categories.'),(98,'2014-05-19 09:00:17',16,36,'5353535','item 2',2,'Changed categories.'),(99,'2014-05-19 09:00:21',16,36,'ARARARARR','ARARARARAR!!!!!',2,'Changed categories.'),(100,'2014-05-19 09:27:25',16,37,'68','ARARARARAR!!!!!',2,'Changed status.'),(101,'2014-05-19 11:25:34',16,37,'88','1 item',3,''),(102,'2014-05-19 11:25:34',16,37,'87','1 item',3,''),(103,'2014-05-19 11:25:34',16,37,'86','item 2',3,''),(104,'2014-05-19 11:25:34',16,37,'85','2fsfsfsfsfsf222',3,''),(105,'2014-05-19 11:25:34',16,37,'84','2fsfsfsfsfsf222',3,''),(106,'2014-05-19 11:25:34',16,37,'83','item 2',3,''),(107,'2014-05-19 11:25:35',16,37,'82','ARARARARAR!!!!!',3,''),(108,'2014-05-19 11:25:35',16,37,'81','ARARARARAR!!!!!',3,''),(109,'2014-05-19 11:25:35',16,37,'80','ARARARARAR!!!!!',3,''),(110,'2014-05-19 11:25:35',16,37,'79','ARARARARAR!!!!!',3,''),(111,'2014-05-19 11:25:35',16,37,'78','item 2',3,''),(112,'2014-05-19 11:25:35',16,37,'77','2fsfsfsfsfsf222',3,''),(113,'2014-05-19 11:25:35',16,37,'76','ARARARARAR!!!!!',3,''),(114,'2014-05-19 11:25:35',16,37,'75','Djaga-Djaga',3,''),(115,'2014-05-19 11:25:35',16,37,'74','1 item',3,''),(116,'2014-05-19 11:25:35',16,37,'73','ARARARARAR!!!!!',3,''),(117,'2014-05-19 11:25:35',16,37,'72','2fsfsfsfsfsf222',3,''),(118,'2014-05-19 11:25:35',16,37,'71','YYYYYYYYYYY',3,''),(119,'2014-05-19 11:25:35',16,37,'70','1 item',3,''),(120,'2014-05-19 11:25:35',16,37,'69','Djaga-Djaga',3,''),(121,'2014-05-19 11:25:36',16,37,'68','ARARARARAR!!!!!',3,''),(122,'2014-05-19 11:25:36',16,37,'67','item 2',3,''),(123,'2014-05-19 11:25:36',16,37,'66','2fsfsfsfsfsf222',3,''),(124,'2014-05-19 11:25:36',16,37,'65','Djaga-Djaga',3,''),(125,'2014-05-19 11:25:36',16,37,'64','ARARARARAR!!!!!',3,''),(126,'2014-05-19 11:25:36',16,37,'63','Djaga-Djaga',3,''),(127,'2014-05-19 11:25:36',16,37,'62','2fsfsfsfsfsf222',3,''),(128,'2014-05-19 11:25:36',16,37,'61','2fsfsfsfsfsf222',3,''),(129,'2014-05-19 11:25:36',16,37,'60','YYYYYYYYYYY',3,''),(130,'2014-05-19 11:25:36',16,37,'59','YYYYYYYYYYY',3,''),(131,'2014-05-19 11:25:36',16,37,'58','1 item',3,''),(132,'2014-05-19 11:25:36',16,37,'57','1 item',3,''),(133,'2014-05-19 11:25:36',16,37,'56','ARARARARAR!!!!!',3,''),(134,'2014-05-19 11:25:36',16,37,'55','YYYYYYYYYYY',3,''),(135,'2014-05-19 11:25:36',16,37,'54','2fsfsfsfsfsf222',3,''),(136,'2014-05-19 11:25:36',16,37,'53','2fsfsfsfsfsf222',3,''),(137,'2014-05-19 11:25:36',16,37,'52','ARARARARAR!!!!!',3,''),(138,'2014-05-19 11:25:36',16,37,'51','1 item',3,''),(139,'2014-05-19 11:25:36',16,37,'50','YYYYYYYYYYY',3,''),(140,'2014-05-19 11:25:37',16,37,'49','2fsfsfsfsfsf222',3,''),(141,'2014-05-19 11:25:37',16,37,'48','2fsfsfsfsfsf222',3,''),(142,'2014-05-19 11:25:37',16,37,'47','ARARARARAR!!!!!',3,''),(143,'2014-05-19 11:25:37',16,37,'46','ARARARARAR!!!!!',3,''),(144,'2014-05-19 11:25:37',16,37,'45','Djaga-Djaga',3,''),(145,'2014-05-19 11:25:37',16,37,'44','Djaga-Djaga',3,''),(146,'2014-05-19 11:25:37',16,37,'43','1 item',3,''),(147,'2014-05-19 11:25:37',16,37,'42','1 item',3,''),(148,'2014-05-19 11:25:37',16,37,'41','Djaga-Djaga',3,''),(149,'2014-05-19 11:25:37',16,37,'40','1 item',3,''),(150,'2014-05-19 11:25:37',16,37,'39','Djaga-Djaga',3,''),(151,'2014-05-19 11:25:37',16,37,'38','2fsfsfsfsfsf222',3,''),(152,'2014-05-19 11:25:37',16,37,'37','YYYYYYYYYYY',3,''),(153,'2014-05-19 11:25:37',16,37,'36','ARARARARAR!!!!!',3,''),(154,'2014-05-19 11:25:37',16,37,'35','Djaga-Djaga',3,''),(155,'2014-05-19 11:25:37',16,37,'34','1 item',3,''),(156,'2014-05-19 11:25:37',16,37,'33','2fsfsfsfsfsf222',3,''),(157,'2014-05-19 11:25:38',16,37,'32','Djaga-Djaga',3,''),(158,'2014-05-19 11:25:38',16,37,'31','ARARARARAR!!!!!',3,''),(159,'2014-05-19 11:25:38',16,37,'30','YYYYYYYYYYY',3,''),(160,'2014-05-19 11:25:38',16,37,'29','YYYYYYYYYYY',3,''),(161,'2014-05-19 11:25:38',16,37,'28','1 item',3,''),(162,'2014-05-19 11:25:38',16,37,'27','Djaga-Djaga',3,''),(163,'2014-05-19 11:25:38',16,37,'26','YYYYYYYYYYY',3,''),(164,'2014-05-19 11:25:38',16,37,'25','item 2',3,''),(165,'2014-05-19 11:25:38',16,37,'24','1 item',3,''),(166,'2014-05-19 11:38:00',16,36,'olkolololololo','SUPER PRODUCT',1,''),(167,'2014-05-19 11:38:40',16,36,'olkolololololo','SUPER PRODUCT',2,'No fields changed.'),(168,'2014-05-19 11:39:22',16,37,'94','SUPER PRODUCT',2,'No fields changed.'),(169,'2014-05-19 11:39:33',16,37,'95','SUPER PRODUCT',2,'No fields changed.'),(170,'2014-05-19 11:39:47',16,36,'olkolololololo','SUPER PRODUCT',2,'No fields changed.'),(171,'2014-05-19 11:40:14',16,37,'96','SUPER PRODUCT',3,''),(172,'2014-05-19 11:40:14',16,37,'95','SUPER PRODUCT',3,''),(173,'2014-05-19 11:55:15',16,37,'97','2fsfsfsfsfsf222',1,''),(174,'2014-05-19 11:55:36',16,37,'98','ARARARARAR!!!!!',1,''),(175,'2014-05-19 11:56:31',16,37,'99','Djaga-Djaga',1,''),(176,'2014-05-19 12:01:02',16,37,'100','SUPER PRODUCT',1,''),(177,'2014-05-19 12:01:21',16,37,'101','Djaga-Djaga',1,''),(178,'2014-05-19 12:01:38',16,37,'102','3 item ',1,''),(179,'2014-05-20 12:42:18',16,35,'4','Musical Instruments',1,''),(180,'2014-05-20 12:48:06',16,34,'1','Fender',1,''),(181,'2014-05-20 12:48:12',16,36,'sladkaya-1999','Jazzmaster Lee Ranaldo',1,''),(182,'2014-05-21 03:21:45',16,36,'sladkaya-1999','Jazzmaster Lee Ranaldo',2,'Added auction item image \"Lee_Ranaldo_Jazzmaster_SZ9386945_1.jpg\".'),(183,'2014-05-21 03:26:28',16,37,'103','Jazzmaster Lee Ranaldo',1,''),(184,'2014-05-21 03:32:06',16,37,'102','3 item ',3,''),(185,'2014-05-21 03:32:06',16,37,'101','Djaga-Djaga',3,''),(186,'2014-05-21 03:32:06',16,37,'100','SUPER PRODUCT',3,''),(187,'2014-05-21 03:32:06',16,37,'99','Djaga-Djaga',3,''),(188,'2014-05-21 03:32:06',16,37,'98','ARARARARAR!!!!!',3,''),(189,'2014-05-21 03:32:06',16,37,'97','2fsfsfsfsfsf222',3,''),(190,'2014-05-21 03:32:06',16,37,'94','SUPER PRODUCT',3,''),(191,'2014-05-21 03:32:06',16,37,'93','YYYYYYYYYYY',3,''),(192,'2014-05-21 03:32:06',16,37,'92','2fsfsfsfsfsf222',3,''),(193,'2014-05-21 03:32:07',16,37,'91','1 item',3,''),(194,'2014-05-21 03:32:07',16,37,'90','item 2',3,''),(195,'2014-05-21 03:32:07',16,37,'89','Djaga-Djaga',3,''),(196,'2014-05-21 03:32:32',16,35,'3','dgdgfdg!!!!!!!!!!!1',3,''),(197,'2014-05-21 03:32:32',16,35,'2','fgdgdg',3,''),(198,'2014-05-21 03:32:32',16,35,'1','gjgjgjg',3,''),(199,'2014-05-21 03:32:56',16,35,'4','Electric Guitars',2,'Changed name and slug.'),(200,'2014-05-21 03:33:15',16,35,'5','Synthetizers',1,''),(201,'2014-05-21 03:33:45',16,36,'YYYYYYYYYY','YYYYYYYYYYY',3,''),(202,'2014-05-21 03:33:46',16,36,'olkolololololo','SUPER PRODUCT',3,''),(203,'2014-05-21 03:33:46',16,36,'ARARARARR','ARARARARAR!!!!!',3,''),(204,'2014-05-21 03:33:46',16,36,'adsadad-ad','1 item',3,''),(205,'2014-05-21 03:33:46',16,36,'7878798798','Djaga-Djaga',3,''),(206,'2014-05-21 03:33:46',16,36,'5353535','item 2',3,''),(207,'2014-05-21 03:33:46',16,36,'456363','2fsfsfsfsfsf222',3,''),(208,'2014-05-21 03:33:46',16,36,'3535','3 item ',3,''),(209,'2014-05-21 03:36:31',16,34,'2','Roland',1,''),(210,'2014-05-21 03:36:39',16,36,'roland-juno-d','Roland Juno-D',1,''),(211,'2014-05-21 03:36:59',16,37,'104','Roland Juno-D',1,''),(212,'2014-05-21 03:37:33',16,36,'roland-juno-d','Roland Juno-D',2,'Added auction item image \"top_L.jpg\".'),(213,'2014-05-21 03:44:27',16,36,'roland-juno-d','Roland Juno-D',2,'No fields changed.'),(214,'2014-05-22 05:02:40',16,37,'103','Jazzmaster Lee Ranaldo',3,''),(215,'2014-05-22 06:57:49',16,37,'108','Roland Juno-D',3,''),(216,'2014-05-22 06:57:49',16,37,'107','Roland Juno-D',3,''),(217,'2014-05-22 06:57:49',16,37,'106','Roland Juno-D',3,''),(218,'2014-05-27 04:08:15',16,35,'6','Giftcards',1,''),(219,'2014-05-27 04:16:51',16,36,'exhibia20bids','ExhibIa 20 Bids',1,''),(220,'2014-05-27 04:17:35',16,36,'exhibia20bids','ExhibIa 20 Bids',2,'Changed is_default for auction item image \"20bids.jpg\".'),(221,'2014-05-27 04:21:00',16,35,'7','Gaming',1,''),(222,'2014-05-27 04:21:16',16,34,'3','Sony',1,''),(223,'2014-05-27 04:23:09',16,36,'Playstation4','Playstation4',1,''),(224,'2014-05-27 04:23:56',16,36,'Playstation4','Playstation4',2,'Changed is_default for auction item image \"playstation4.jpg\".'),(225,'2014-05-27 04:35:19',16,37,'113','ExhibIa 20 Bids',1,''),(226,'2014-05-27 04:36:31',16,37,'113','ExhibIa 20 Bids',2,'Changed status.'),(227,'2014-05-27 04:37:27',16,37,'114','Playstation4',1,''),(228,'2014-05-27 08:30:33',16,23,'1','admin - Facebook',3,''),(229,'2014-05-27 08:31:58',16,4,'16','admin',2,'Changed email.'),(230,'2014-05-27 08:34:19',16,23,'10','admin - Facebook',3,''),(231,'2014-05-27 08:36:11',16,4,'16','admin',2,'Changed first_name, last_name and email.'),(232,'2014-05-27 08:36:11',16,4,'16','admin',2,'No fields changed.'),(233,'2014-05-28 06:16:45',16,49,'1','Jazzmaster Lee Ranaldo - SS - 10',1,''),(234,'2014-05-28 06:17:04',16,49,'2','Roland Juno-D - SSD - 35',1,''),(235,'2014-05-28 06:17:22',16,49,'3','Playstation4 - SS - 20',1,''),(236,'2014-05-28 06:17:44',16,49,'4','ExhibIa 20 Bids - SE - 18',1,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'message','auth','message'),(6,'banned ip address','auth','bannedipaddress'),(7,'content type','contenttypes','contenttype'),(8,'session','sessions','session'),(9,'site','sites','site'),(10,'flat page','flatpages','flatpage'),(11,'notice type','notification','noticetype'),(12,'notice setting','notification','noticesetting'),(13,'notice','notification','notice'),(14,'notice queue batch','notification','noticequeuebatch'),(15,'observed item','notification','observeditem'),(16,'message','mailer','message'),(17,'don\'t send entry','mailer','dontsendentry'),(18,'message log','mailer','messagelog'),(19,'email address','emailconfirmation','emailaddress'),(20,'email confirmation','emailconfirmation','emailconfirmation'),(21,'announcement','announcements','announcement'),(22,'migration history','south','migrationhistory'),(23,'user social auth','social_auth','usersocialauth'),(24,'nonce','social_auth','nonce'),(25,'association','social_auth','association'),(26,'account','account','account'),(27,'password reset','account','passwordreset'),(28,'signup code','signup_codes','signupcode'),(29,'signup code result','signup_codes','signupcoderesult'),(30,'setting','dbsettings','setting'),(31,'member','profiles','member'),(32,'billing address','profiles','billingaddress'),(33,'ip address','profiles','ipaddress'),(34,'brand','auctions','brand'),(35,'Category','auctions','category'),(36,'auction item','auctions','auctionitem'),(37,'auction','auctions','auction'),(38,'auction bid','auctions','auctionbid'),(39,'auction item image','auctions','auctionitemimages'),(40,'auction plegde','auctions','auctionplegde'),(41,'video','testimonials','video'),(42,'auction item','bidin','auctionitem'),(43,'auction item images','bidin','auctionitemimages'),(44,'payment notification','payments','paymentnotification'),(45,'credit package order','payments','creditpackageorder'),(46,'auction order','payments','auctionorder'),(47,'card','payments','card'),(48,'shipping address','shipping','shippingaddress'),(49,'shipping fee','shipping','shippingfee'),(50,'shipping request','shipping','shippingrequest'),(51,'order','checkout','order'),(52,'like item','socials','likeitem'),(53,'invitation','socials','invitation'),(54,'referral link','referrals','referrallink'),(55,'store item','points_store','storeitem'),(56,'bought item','points_store','boughtitem'),(57,'nonce','django_openid','nonce'),(58,'association','django_openid','association'),(59,'user openid association','django_openid','useropenidassociation'),(60,'source','easy_thumbnails','source'),(61,'thumbnail','easy_thumbnails','thumbnail'),(62,'Redis Server','redisboard','redisserver');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_flatpage`
--

DROP TABLE IF EXISTS `django_flatpage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_flatpage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(100) NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `enable_comments` tinyint(1) NOT NULL,
  `template_name` varchar(70) NOT NULL,
  `registration_required` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_flatpage_a4b49ab` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_flatpage`
--

LOCK TABLES `django_flatpage` WRITE;
/*!40000 ALTER TABLE `django_flatpage` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_flatpage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_flatpage_sites`
--

DROP TABLE IF EXISTS `django_flatpage_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_flatpage_sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `flatpage_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `flatpage_id` (`flatpage_id`,`site_id`),
  KEY `django_flatpage_sites_dedefef8` (`flatpage_id`),
  KEY `django_flatpage_sites_6223029` (`site_id`),
  CONSTRAINT `flatpage_id_refs_id_c0e84f5a` FOREIGN KEY (`flatpage_id`) REFERENCES `django_flatpage` (`id`),
  CONSTRAINT `site_id_refs_id_4e3eeb57` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_flatpage_sites`
--

LOCK TABLES `django_flatpage_sites` WRITE;
/*!40000 ALTER TABLE `django_flatpage_sites` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_flatpage_sites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_openid_association`
--

DROP TABLE IF EXISTS `django_openid_association`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_openid_association` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_url` longtext NOT NULL,
  `handle` varchar(255) NOT NULL,
  `secret` longtext NOT NULL,
  `issued` int(11) NOT NULL,
  `lifetime` int(11) NOT NULL,
  `assoc_type` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_openid_association`
--

LOCK TABLES `django_openid_association` WRITE;
/*!40000 ALTER TABLE `django_openid_association` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_openid_association` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_openid_nonce`
--

DROP TABLE IF EXISTS `django_openid_nonce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_openid_nonce` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) NOT NULL,
  `timestamp` int(11) NOT NULL,
  `salt` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_openid_nonce`
--

LOCK TABLES `django_openid_nonce` WRITE;
/*!40000 ALTER TABLE `django_openid_nonce` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_openid_nonce` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_openid_useropenidassociation`
--

DROP TABLE IF EXISTS `django_openid_useropenidassociation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_openid_useropenidassociation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `openid` varchar(255) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_openid_useropenidassociation_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_7b6741ee` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_openid_useropenidassociation`
--

LOCK TABLES `django_openid_useropenidassociation` WRITE;
/*!40000 ALTER TABLE `django_openid_useropenidassociation` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_openid_useropenidassociation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_c25c2c28` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('015edb09be02a904138ea60cf0d589e5','MDQ5Nzg4MGFiMTllYzhiNGM0ZDc2OWE0MjFhYjhiYjY3YmQwYTA5ZjqAAn1xAVUDcmVmVQ93d3cu\nZXhoaWJpYS5jb21xAnMu\n','2014-11-24 05:43:28'),('03faff55eaedd1ccb515361507256942','YTkzNzIwZTg1ZmU4ZGQ3MmQyNDMyMTkwZDRmNjg0MWI1NDZlOGQ4MzqAAn1xAShVD19zZXNzaW9u\nX2V4cGlyeXECSwBVCV9tZXNzYWdlc3EDXXEEY2RqYW5nby5jb250cmliLm1lc3NhZ2VzLnN0b3Jh\nZ2UuYmFzZQpNZXNzYWdlCnEFKYFxBn1xByhVCmV4dHJhX3RhZ3NxCFgAAAAAVQdtZXNzYWdlcQlY\nJwAAANCj0YHQv9C10YjQvdC+INCy0L7RiNC70Lgg0LrQsNC6IHVzZXIxLlUFbGV2ZWxxCksZdWJh\nVQNyZWZVDjEyNy4wLjAuMTo4MDAwcQtVEl9hdXRoX3VzZXJfYmFja2VuZHEMVSlkamFuZ28uY29u\ndHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHENVQ1fYXV0aF91c2VyX2lkcQ6KARJ1Lg==\n','2014-11-10 09:41:54'),('04a653c8b98b12cf3859578b40565598','Y2E5MTcyODZkZTE0NzRhNTNiY2U4NDE0ZWMwZDBmNWE1NzAwN2Y0NTqAAn1xAVUTZ29vZ2xlLW9h\ndXRoMl9zdGF0ZVUgMmswYjgxT2lRd0pxUnRqcUhheDRQRlMza3pUdzZUZmRzLg==\n','2014-11-21 14:47:59'),('07a83dc4f13e8c10898d3edba663f11a','NmI2OTExMTJhOGFlMmY0NDI0NDE5MWNlYWE2OTI3YzU1M2VhNmEyYTqAAn1xAVUDcmVmcQJVC2V4\naGliaWEuY29tcQNzLg==\n','2014-11-21 04:28:52'),('091e51f73a312f8462749fd64b136e21','YjdlNjA5MjY1ZGUzM2UwNmYyNmRkNTFkYTk2MWI2NDEzOTgxN2JmMzqAAn1xAVUDcmVmcQJVEjE4\nYjc1ZDM4Lm5ncm9rLmNvbXEDcy4=\n','2014-11-16 04:33:11'),('0a38d11e4c490968f47a08033dce6fa3','ZDRlMDM3NjM2NDQ3NDkyZTk0NTVhMTM3OWI2MzU3NjA3YjFkZmE2ODqAAn1xAShVD19zZXNzaW9u\nX2V4cGlyeXECSoCvGwBVCV9tZXNzYWdlc3EDXXEEY2RqYW5nby5jb250cmliLm1lc3NhZ2VzLnN0\nb3JhZ2UuYmFzZQpNZXNzYWdlCnEFKYFxBn1xByhVCmV4dHJhX3RhZ3NxCFgAAAAAVQdtZXNzYWdl\ncQlYJgAAANCj0YHQv9C10YjQvdC+INCy0L7RiNC70Lgg0LrQsNC6IHVzZXIuVQVsZXZlbHEKSxl1\nYmFVA3JlZlUOMTI3LjAuMC4xOjgwMDBxC1USX2F1dGhfdXNlcl9iYWNrZW5kcQxVKWRqYW5nby5j\nb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kcQ1VDV9hdXRoX3VzZXJfaWRxDooBEXUu\n','2014-06-04 08:52:10'),('0c0e1a7fa4007387016c2868e6ea5a57','YjQ5MmJkYTZiZTZjODQ1MjhiMWE0NmE2MzFmNGFjN2M5MTY3NDBjYTqAAn1xAVUDcmVmcQJVDjEy\nNy4wLjAuMTo4MDAwcQNzLg==\n','2014-11-10 10:42:53'),('0c334b508d5e144633e7bc692fa6df89','NGIxOTg0OGMxNDIzNmNmZTAyNDU3NzE0M2Y0NDMwYWRlNDRhMTA1MDqAAn1xAVUDcmVmVQtleGhp\nYmlhLmNvbXECcy4=\n','2014-11-20 19:42:39'),('0c4c4b3bb2c969bc46ee84eb7971f298','MWI4MWRjZGNlMmE1OGFmMmQ1MjU5YTFiM2U0ODdhNWE2N2ZlYTdiYjqAAn1xAShVD19zZXNzaW9u\nX2V4cGlyeXECSwBVCV9tZXNzYWdlc3EDXXEEY2RqYW5nby5jb250cmliLm1lc3NhZ2VzLnN0b3Jh\nZ2UuYmFzZQpNZXNzYWdlCnEFKYFxBn1xByhVCmV4dHJhX3RhZ3NxCFgAAAAAVQdtZXNzYWdlcQlY\nJgAAANCj0YHQv9C10YjQvdC+INCy0L7RiNC70Lgg0LrQsNC6IHVzZXIuVQVsZXZlbHEKSxl1YmFV\nA3JlZlUOMTI3LjAuMC4xOjgwMDBxC1USX2F1dGhfdXNlcl9iYWNrZW5kcQxVKWRqYW5nby5jb250\ncmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kcQ1VDV9hdXRoX3VzZXJfaWRxDooBEXUu\n','2014-11-10 09:12:58'),('0c5b26b76ff24adf4658c5511fd7bd35','NDE3MjIxMzMzYzJkNWEwZWRjMjdlODMwMThlZjNiODk0ZGZlYjU4MDqAAn1xAVUDcmVmcQJVD3d3\ndy5leGhpYmlhLmNvbXEDcy4=\n','2014-11-24 04:08:38'),('0d06dacb065f025d442796a2bc33e556','YjdlNjA5MjY1ZGUzM2UwNmYyNmRkNTFkYTk2MWI2NDEzOTgxN2JmMzqAAn1xAVUDcmVmcQJVEjE4\nYjc1ZDM4Lm5ncm9rLmNvbXEDcy4=\n','2014-11-16 04:33:11'),('0da1edbccd4be6ac27cfdc494651e614','NGIxOTg0OGMxNDIzNmNmZTAyNDU3NzE0M2Y0NDMwYWRlNDRhMTA1MDqAAn1xAVUDcmVmVQtleGhp\nYmlhLmNvbXECcy4=\n','2014-11-23 04:52:58'),('15332cd0c4aed2afac692393b773c694','NDRiMmU0MTAxNzI5ZDljNTJhNmFlMzU3NWE0MGJhZDlhZWU3YWQwNjqAAn1xAS4=\n','2014-11-23 23:23:57'),('15ccb5110ef0e1abe21a11f9bba59738','MDE4MWM4YjdlM2NmYzdjOWZjMTA3NjM4Y2EzZmYwMDMzYzNiZGIyNTqAAn1xAVUDcmVmcQJVDmxv\nY2FsaG9zdDo4MDAwcQNzLg==\n','2014-11-18 05:22:38'),('175bf49d850886b52a8b8390dd0a2b12','MDE4MWM4YjdlM2NmYzdjOWZjMTA3NjM4Y2EzZmYwMDMzYzNiZGIyNTqAAn1xAVUDcmVmcQJVDmxv\nY2FsaG9zdDo4MDAwcQNzLg==\n','2014-11-18 05:22:38'),('19312cdd99c7be03dfb65c0af9e9349b','NDRiMmU0MTAxNzI5ZDljNTJhNmFlMzU3NWE0MGJhZDlhZWU3YWQwNjqAAn1xAS4=\n','2014-11-22 09:40:56'),('1aae512b1ce7f0f3e76cdbdf53f9d61e','YTRhYjM1NjczMDUyYWQyZjE0ZjkwNjUwNGM1Yzk2ZjIzNzIwMjcyNTqAAn1xAVUDcmVmcQJVDnd3\ndy5nb29nbGUuY29tcQNzLg==\n','2014-11-22 16:36:50'),('1b3e450360115ffaf5129f4f6ec86fa7','YjY4NTJkMjhiMDlhNzk0Y2NkMWQ4NTFhYTZkMTdhMjBlMmJlNTI3ZTqAAn1xAVUedHdpdHRlcnVu\nYXV0aG9yaXplZF90b2tlbl9uYW1lXXECVZJvYXV0aF90b2tlbl9zZWNyZXQ9TXppWmxVY1lONFJl\nZElCWDFDYVowUlhJWnlvekZFalZ1VmxUekZMYncmb2F1dGhfdG9rZW49NHFMbEdKemp5aDM4cU9Z\nWlhvMzZDNFBRcldKdkVBM3FEQ1NlNm5LeXRKWSZvYXV0aF9jYWxsYmFja19jb25maXJtZWQ9dHJ1\nZXEDYXMu\n','2014-11-21 14:47:48'),('1c8188cd914116723da1ff58dbf1579a','MDE4MWM4YjdlM2NmYzdjOWZjMTA3NjM4Y2EzZmYwMDMzYzNiZGIyNTqAAn1xAVUDcmVmcQJVDmxv\nY2FsaG9zdDo4MDAwcQNzLg==\n','2014-11-18 05:22:37'),('1f428a2c67675544039282c1f92db4c8','YmFiYTMxZGMwYWE3OTY0YTAwYWUwNmU5NDdkMmYxNTg3MjdjMTY2MzqAAn1xAShVDV9hdXRoX3Vz\nZXJfaWRxAooBGFUOZmFjZWJvb2tfc3RhdGVVIExzaEE4TmdqTGRCTkg5SFpxbFQ2V1AwdnJvVHdV\nR0hYVRJfYXV0aF91c2VyX2JhY2tlbmRxA1Utc29jaWFsX2F1dGguYmFja2VuZHMuZmFjZWJvb2su\nRmFjZWJvb2tCYWNrZW5kcQRVHnNvY2lhbF9hdXRoX2xhc3RfbG9naW5fYmFja2VuZHEFVQhmYWNl\nYm9va3EGVQ9fc2Vzc2lvbl9leHBpcnlxB2NkYXRldGltZQpkYXRldGltZQpxCFUKB94HFgcYGAtn\nioVScQlVA3JlZlULZXhoaWJpYS5jb211Lg==\n','2014-07-22 07:24:24'),('2054bc28bbb28bbb01f2d177e8cdd67c','NDRiMmU0MTAxNzI5ZDljNTJhNmFlMzU3NWE0MGJhZDlhZWU3YWQwNjqAAn1xAS4=\n','2014-11-23 11:07:18'),('244b2d81d9e8d187de39f90cb268adaf','MDQ5Nzg4MGFiMTllYzhiNGM0ZDc2OWE0MjFhYjhiYjY3YmQwYTA5ZjqAAn1xAVUDcmVmVQ93d3cu\nZXhoaWJpYS5jb21xAnMu\n','2014-11-23 01:37:19'),('28604b7c4df48c147feaf5fa66c0e0e5','YjdlNjA5MjY1ZGUzM2UwNmYyNmRkNTFkYTk2MWI2NDEzOTgxN2JmMzqAAn1xAVUDcmVmcQJVEjE4\nYjc1ZDM4Lm5ncm9rLmNvbXEDcy4=\n','2014-11-16 04:33:12'),('295e83a4f8ebc8b2eb08d0bfecfe0d50','NGIxOTg0OGMxNDIzNmNmZTAyNDU3NzE0M2Y0NDMwYWRlNDRhMTA1MDqAAn1xAVUDcmVmVQtleGhp\nYmlhLmNvbXECcy4=\n','2014-11-21 04:36:12'),('2b64e33f78e468963d47b1b278b956c7','NDE3MjIxMzMzYzJkNWEwZWRjMjdlODMwMThlZjNiODk0ZGZlYjU4MDqAAn1xAVUDcmVmcQJVD3d3\ndy5leGhpYmlhLmNvbXEDcy4=\n','2014-11-22 23:15:46'),('2c9e5110571697f2a48e229795e1a711','MDQ5Nzg4MGFiMTllYzhiNGM0ZDc2OWE0MjFhYjhiYjY3YmQwYTA5ZjqAAn1xAVUDcmVmVQ93d3cu\nZXhoaWJpYS5jb21xAnMu\n','2014-11-23 08:27:16'),('2fb8b6e881b9f90fd143d3b3bd93bf98','ZTVhYjZmYjI4ZTBiZjdkMzdiOTBkZjhkZDE3ZGQzMDI1NWZkZTg1ZDqAAn1xAShVE2dvb2dsZS1v\nYXV0aDJfc3RhdGVVIDhWQllpT0NWeUhFT1ZPYkkxWFhQa3p6U1Z1c2xVcThUVQ1fYXV0aF91c2Vy\nX2lkcQKKARtVHnNvY2lhbF9hdXRoX2xhc3RfbG9naW5fYmFja2VuZHEDVQ1nb29nbGUtb2F1dGgy\ncQRVEl9hdXRoX3VzZXJfYmFja2VuZHEFVS9zb2NpYWxfYXV0aC5iYWNrZW5kcy5nb29nbGUuR29v\nZ2xlT0F1dGgyQmFja2VuZHEGVQ9fc2Vzc2lvbl9leHBpcnlxB2NkYXRldGltZQpkYXRldGltZQpx\nCFUKB94FGwcFGg0KBoVScQlVA3JlZlUPd3d3LmV4aGliaWEuY29tdS4=\n','2014-05-27 07:05:26'),('318590ae3965ce1fc237c06fef1df689','NmI2OTExMTJhOGFlMmY0NDI0NDE5MWNlYWE2OTI3YzU1M2VhNmEyYTqAAn1xAVUDcmVmcQJVC2V4\naGliaWEuY29tcQNzLg==\n','2014-11-19 11:43:31'),('33d2dba423fc0bd838f0cc4990bef3ce','NDRiMmU0MTAxNzI5ZDljNTJhNmFlMzU3NWE0MGJhZDlhZWU3YWQwNjqAAn1xAS4=\n','2014-11-11 03:59:52'),('3647daa5fa3ad38ada2d1bd4d3b5d3ea','YjdlNjA5MjY1ZGUzM2UwNmYyNmRkNTFkYTk2MWI2NDEzOTgxN2JmMzqAAn1xAVUDcmVmcQJVEjE4\nYjc1ZDM4Lm5ncm9rLmNvbXEDcy4=\n','2014-11-16 04:49:10'),('385eee9a560b6bd718fdca97066837ba','YjQ5MmJkYTZiZTZjODQ1MjhiMWE0NmE2MzFmNGFjN2M5MTY3NDBjYTqAAn1xAVUDcmVmcQJVDjEy\nNy4wLjAuMTo4MDAwcQNzLg==\n','2014-11-15 05:54:42'),('3c1c3e95e4326ab0025dcb22ede35968','YzVjNzk1YmU1N2U1Mzk4YTk1Zjc2MWQ1MDc4NTdmOGQ0NzAzYmIzYzqAAn1xAShVE2dvb2dsZS1v\nYXV0aDJfc3RhdGVVIEJLRlJuWjBuVGlvNWV1WHJvakZaamgzNzhXYWpZZUtnVR50d2l0dGVydW5h\ndXRob3JpemVkX3Rva2VuX25hbWVdcQJVk29hdXRoX3Rva2VuX3NlY3JldD1wRWk0TTI1ZnF2Y3E5\nRDFtZkZJSWRQMHlldlB4ZEp2cVFwemd4ZHN3SkUmb2F1dGhfdG9rZW49Y0VBTlBUQzZxb2FJakZK\nR2V3YVhnbGY0NmltN1QzNUg5aDhoWUNhMUFjZyZvYXV0aF9jYWxsYmFja19jb25maXJtZWQ9dHJ1\nZXEDYVUNX2F1dGhfdXNlcl9pZIoBEFUOZmFjZWJvb2tfc3RhdGVVIFdDdHNybldrNjY4ZXZsTVpm\nbnFvMzNXZVhad2tSUHhzVRJfYXV0aF91c2VyX2JhY2tlbmRVKWRqYW5nby5jb250cmliLmF1dGgu\nYmFja2VuZHMuTW9kZWxCYWNrZW5kVQNyZWZVDjEyNy4wLjAuMTo4MDAwdS4=\n','2014-11-15 12:01:39'),('3e6964f6d6e18c4d37f1b17b638fb9e9','MDQ5Nzg4MGFiMTllYzhiNGM0ZDc2OWE0MjFhYjhiYjY3YmQwYTA5ZjqAAn1xAVUDcmVmVQ93d3cu\nZXhoaWJpYS5jb21xAnMu\n','2014-11-24 03:38:21'),('3f5dbaf4a8c06a0944f1629c28740985','MGNkNTBlMDFkMDgyYWM1ZDM3OGE5MjRiZWUzMjA5MmJhODM0NTViZTqAAn1xAShVE2dvb2dsZS1v\nYXV0aDJfc3RhdGVVIHRvSkxzR0pyZUUwYlJRMGE1d1RWcU5FN1dQcE5CM25lVQ1fYXV0aF91c2Vy\nX2lkigEQVQ5mYWNlYm9va19zdGF0ZVUgVExldU9BdlhiYVdXd2ozZ3Y0TEE4RjkwRUdlcnFJNUVV\nEl9hdXRoX3VzZXJfYmFja2VuZFUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJh\nY2tlbmRVA3JlZlUObG9jYWxob3N0OjgwMDB1Lg==\n','2014-11-18 06:57:53'),('40cccd6f7631bfce6bf83d6969c0534a','ZmQ4MDljYzI4MTNhOGIyMTNkZjZmZGFkNDU5MTc4ZjE3N2JjZTMyMjqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2014-11-10 11:13:09'),('42127274e5ca3f0aeaf83fee86b6243f','NDE3MjIxMzMzYzJkNWEwZWRjMjdlODMwMThlZjNiODk0ZGZlYjU4MDqAAn1xAVUDcmVmcQJVD3d3\ndy5leGhpYmlhLmNvbXEDcy4=\n','2014-11-23 07:54:33'),('42ceea90737c88031287e651ea8528d8','YjQ5MmJkYTZiZTZjODQ1MjhiMWE0NmE2MzFmNGFjN2M5MTY3NDBjYTqAAn1xAVUDcmVmcQJVDjEy\nNy4wLjAuMTo4MDAwcQNzLg==\n','2014-11-15 05:54:42'),('47158af9f25a42187aff6649e327a1a2','NDE3MjIxMzMzYzJkNWEwZWRjMjdlODMwMThlZjNiODk0ZGZlYjU4MDqAAn1xAVUDcmVmcQJVD3d3\ndy5leGhpYmlhLmNvbXEDcy4=\n','2014-11-23 13:09:06'),('484eef2f185aff87803bd3e19ba1169c','MDE4MWM4YjdlM2NmYzdjOWZjMTA3NjM4Y2EzZmYwMDMzYzNiZGIyNTqAAn1xAVUDcmVmcQJVDmxv\nY2FsaG9zdDo4MDAwcQNzLg==\n','2014-11-18 05:22:38'),('48997dec8f92e434821c53d680f3f660','NDE3MjIxMzMzYzJkNWEwZWRjMjdlODMwMThlZjNiODk0ZGZlYjU4MDqAAn1xAVUDcmVmcQJVD3d3\ndy5leGhpYmlhLmNvbXEDcy4=\n','2014-11-23 07:46:26'),('48df40019864371b026c129a260853f1','N2ZhM2M0NjBkMzIxYTQwYjE2OTAwM2I1YmE4N2NkYzIwMzFlNDQ2NDqAAn1xAVUDcmVmcQJVFXdo\nb2lzLmRvbWFpbnRvb2xzLmNvbXEDcy4=\n','2014-11-21 00:13:54'),('4cc06d5b330cf7edbc2e5c977405ce58','ZmI1OWZjOWI3MGVkM2U5NzgwZDAwNmE4YmYzYmMwMzQwZDIyMWEyMzqAAn1xAShVE2dvb2dsZS1v\nYXV0aDJfc3RhdGVVIE41R1NUUFZaUU96ZlNBd2N0cEF4dklFOXFiS1UwSnE1VQ1fYXV0aF91c2Vy\nX2lkigEQVR5zb2NpYWxfYXV0aF9sYXN0X2xvZ2luX2JhY2tlbmRYDQAAAGdvb2dsZS1vYXV0aDJV\nEl9hdXRoX3VzZXJfYmFja2VuZFUvc29jaWFsX2F1dGguYmFja2VuZHMuZ29vZ2xlLkdvb2dsZU9B\ndXRoMkJhY2tlbmRVD19zZXNzaW9uX2V4cGlyeWNkYXRldGltZQpkYXRldGltZQpxAlUKB94FHAY5\nHQK5EYVScQNVA3JlZlUPd3d3LmV4aGliaWEuY29tdS4=\n','2014-05-28 06:57:29'),('513dd1eaeb38a0fe8a0834e1a2e6f366','ZDc3ZjI0NGUzNTBjYTQyZGY3MjY5NTI0YjliNjlkYzU5OTIyNWFlNDqAAn1xAVUDcmVmcQJVCXdt\nYWlkLmNvbXEDcy4=\n','2014-11-21 06:00:24'),('56bb7f8be5ff18a4c0f9819717eb315a','YjdlNjA5MjY1ZGUzM2UwNmYyNmRkNTFkYTk2MWI2NDEzOTgxN2JmMzqAAn1xAVUDcmVmcQJVEjE4\nYjc1ZDM4Lm5ncm9rLmNvbXEDcy4=\n','2014-11-16 04:33:11'),('56e1a35707f1b69704796ad2b07742fe','YjdlNjA5MjY1ZGUzM2UwNmYyNmRkNTFkYTk2MWI2NDEzOTgxN2JmMzqAAn1xAVUDcmVmcQJVEjE4\nYjc1ZDM4Lm5ncm9rLmNvbXEDcy4=\n','2014-11-16 04:49:10'),('575b93cca1313dbf920fcc622f3e9171','NmI2OTExMTJhOGFlMmY0NDI0NDE5MWNlYWE2OTI3YzU1M2VhNmEyYTqAAn1xAVUDcmVmcQJVC2V4\naGliaWEuY29tcQNzLg==\n','2014-11-22 03:52:20'),('58b70bffa4759703368f79b912f814b7','YjQ5MmJkYTZiZTZjODQ1MjhiMWE0NmE2MzFmNGFjN2M5MTY3NDBjYTqAAn1xAVUDcmVmcQJVDjEy\nNy4wLjAuMTo4MDAwcQNzLg==\n','2014-11-15 05:54:42'),('58eef81f5b1729fa8f9374c767281054','YjdlNjA5MjY1ZGUzM2UwNmYyNmRkNTFkYTk2MWI2NDEzOTgxN2JmMzqAAn1xAVUDcmVmcQJVEjE4\nYjc1ZDM4Lm5ncm9rLmNvbXEDcy4=\n','2014-11-16 04:33:12'),('59bcb9d6ae7b90be5c99d520739814c0','MDQ5Nzg4MGFiMTllYzhiNGM0ZDc2OWE0MjFhYjhiYjY3YmQwYTA5ZjqAAn1xAVUDcmVmVQ93d3cu\nZXhoaWJpYS5jb21xAnMu\n','2014-11-23 01:37:17'),('5ae1c93a89ce4dc047e363cf315af720','YTRhYjM1NjczMDUyYWQyZjE0ZjkwNjUwNGM1Yzk2ZjIzNzIwMjcyNTqAAn1xAVUDcmVmcQJVDnd3\ndy5nb29nbGUuY29tcQNzLg==\n','2014-11-22 16:36:50'),('5b518a3513c53d0941c284c1ef1eed5b','ZTAxYWIwYWM0YmY4N2E2ZTlkMzBhNTliNjAxM2Q4OTUyN2VkMDg1YTqAAn1xAShVD19zZXNzaW9u\nX2V4cGlyeXECSoCvGwBVCV9tZXNzYWdlc3EDXXEEY2RqYW5nby5jb250cmliLm1lc3NhZ2VzLnN0\nb3JhZ2UuYmFzZQpNZXNzYWdlCnEFKYFxBn1xByhVCmV4dHJhX3RhZ3NxCFgAAAAAVQdtZXNzYWdl\ncQlYKAAAANCj0YHQv9C10YjQvdC+INCy0L7RiNC70Lgg0LrQsNC6IHVzZXIxMC5VBWxldmVscQpL\nGXViYVUDcmVmVQ4xMjcuMC4wLjE6ODAwMHELVRJfYXV0aF91c2VyX2JhY2tlbmRxDFUpZGphbmdv\nLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmRxDVUNX2F1dGhfdXNlcl9pZHEOigEW\ndS4=\n','2014-06-05 04:41:36'),('5facf7e6ee0d6708abb54a5c1fc7bddd','NDRiMmU0MTAxNzI5ZDljNTJhNmFlMzU3NWE0MGJhZDlhZWU3YWQwNjqAAn1xAS4=\n','2014-11-22 02:52:34'),('5fd22a2ae6b6a005bfed32ca756c5f01','MDE4MWM4YjdlM2NmYzdjOWZjMTA3NjM4Y2EzZmYwMDMzYzNiZGIyNTqAAn1xAVUDcmVmcQJVDmxv\nY2FsaG9zdDo4MDAwcQNzLg==\n','2014-11-18 05:22:37'),('60d2e107383e95c163b449eb3467d8f7','ZjcyZjMwOTQxZThhMzJmYWI2ZjQzNzE1ZTYwNmM2ZTEwYTJhMTY1OTqAAn1xAVUTZ29vZ2xlLW9h\ndXRoMl9zdGF0ZVUgaUg5Uzh1b0J2REw2T2xyYU1mYW12aEhLU1dCSEdHRXdzLg==\n','2014-11-20 20:58:03'),('61b3234063bc6a35edac4a5a33ac5178','YjQ5MmJkYTZiZTZjODQ1MjhiMWE0NmE2MzFmNGFjN2M5MTY3NDBjYTqAAn1xAVUDcmVmcQJVDjEy\nNy4wLjAuMTo4MDAwcQNzLg==\n','2014-11-15 05:54:42'),('62a017206a378e1e53d82b2a9e6dc06c','MDQ5Nzg4MGFiMTllYzhiNGM0ZDc2OWE0MjFhYjhiYjY3YmQwYTA5ZjqAAn1xAVUDcmVmVQ93d3cu\nZXhoaWJpYS5jb21xAnMu\n','2014-11-23 15:05:15'),('6aac608e58951bd3d7f0bd40457510ae','NGQ4N2M1MjNiNzE1NGEwMjM0ZGU5ZWNlMjQwZDM3Y2I2OTk0NTU4ODqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZFUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmRVA3Jl\nZlUPd3d3LmV4aGliaWEuY29tVQ1fYXV0aF91c2VyX2lkigEQdS4=\n','2014-11-23 04:37:28'),('6acb18af2e66f5dc82e1544f89135288','YWYxMmZhODAyNmI2YjVlYzA5ODhhNmQ0NmUzYzQ1MWI2MjVjYTU4YzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKARJ1Lg==\n','2014-11-15 09:28:16'),('6e11f5a19468bbcdf7c0fc857ac7d35c','MDQ5Nzg4MGFiMTllYzhiNGM0ZDc2OWE0MjFhYjhiYjY3YmQwYTA5ZjqAAn1xAVUDcmVmVQ93d3cu\nZXhoaWJpYS5jb21xAnMu\n','2014-11-24 04:21:34'),('77603e9bad670dcb592cfb8c8a811d90','YTQ5OTg1MDhiMDcwOGI4ZTJlM2ExOTE1ZTVjMGEyOGMzZGY0MTI4YTqAAn1xAShVA3JlZnECVQtl\neGhpYmlhLmNvbXEDVRJfYXV0aF91c2VyX2JhY2tlbmRxBFUpZGphbmdvLmNvbnRyaWIuYXV0aC5i\nYWNrZW5kcy5Nb2RlbEJhY2tlbmRxBVUNX2F1dGhfdXNlcl9pZHEGigEQdS4=\n','2014-11-23 04:24:22'),('77cb740a870984336ed41efd291c53a5','MDE4MWM4YjdlM2NmYzdjOWZjMTA3NjM4Y2EzZmYwMDMzYzNiZGIyNTqAAn1xAVUDcmVmcQJVDmxv\nY2FsaG9zdDo4MDAwcQNzLg==\n','2014-11-18 05:22:37'),('77e115a0932d265420ad45f498118d74','YjQ5MmJkYTZiZTZjODQ1MjhiMWE0NmE2MzFmNGFjN2M5MTY3NDBjYTqAAn1xAVUDcmVmcQJVDjEy\nNy4wLjAuMTo4MDAwcQNzLg==\n','2014-11-15 05:54:42'),('780911f40bb05efa5bc45d4eade93a72','YjQ5MmJkYTZiZTZjODQ1MjhiMWE0NmE2MzFmNGFjN2M5MTY3NDBjYTqAAn1xAVUDcmVmcQJVDjEy\nNy4wLjAuMTo4MDAwcQNzLg==\n','2014-11-15 05:54:41'),('7cc1f0c1c32c8a46b8846b05945237f8','NDRiMmU0MTAxNzI5ZDljNTJhNmFlMzU3NWE0MGJhZDlhZWU3YWQwNjqAAn1xAS4=\n','2014-11-19 02:47:41'),('82dc839e31681bc7d657af662064f6bc','MDllMmU3NTI4OGU5MzQ0NGIyMDM3ZjQ5ZWE0NzcwYWZkNzAzMmQyYzqAAn1xAVUDcmVmVQ4xMjcu\nMC4wLjE6ODAwMHECcy4=\n','2014-11-10 11:01:45'),('82e93db43ee545f77d7528452b9f6603','MDE4MWM4YjdlM2NmYzdjOWZjMTA3NjM4Y2EzZmYwMDMzYzNiZGIyNTqAAn1xAVUDcmVmcQJVDmxv\nY2FsaG9zdDo4MDAwcQNzLg==\n','2014-11-18 05:22:38'),('83379d48ca3173135661bb0f15fccf14','ZjM5MWYwYzRiOGU2YTE3ZWE2NTI2ZGE2ZWZlMDMzZjFkNzE0MGUzMzqAAn1xAVUDcmVmcQJVDXd3\ndy5iYWlkdS5jb21xA3Mu\n','2014-11-22 14:14:40'),('8341cbf243ec3c42273acd7fcca32862','NGIxOTg0OGMxNDIzNmNmZTAyNDU3NzE0M2Y0NDMwYWRlNDRhMTA1MDqAAn1xAVUDcmVmVQtleGhp\nYmlhLmNvbXECcy4=\n','2014-11-22 09:23:11'),('87bcd4337ef95f059a7bf226070a89ec','YWFhNGJjZjliZmUyMTMyYzJmNWE2ZmU0MjRmZWQ3Zjg3YmUxMzJkNTqAAn1xAShVDmZhY2Vib29r\nX3N0YXRlVSBSWms4Z1dyTTlrTTUxMGNGTldBZEJwRWhnOTJCdmswQ1USX2F1dGhfdXNlcl9iYWNr\nZW5kVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZFUDcmVmVQ4xMjcu\nMC4wLjE6ODAwMFUNX2F1dGhfdXNlcl9pZIoBEHUu\n','2014-11-10 09:47:31'),('8896142d7884e6eba003ccaf8db76e7e','NzQxNTEyMjE3ZDU5YjllNjE2OWUwMmU4ZDNjMGY4NGNlYTA1MmU1ZDqAAn1xAVUDcmVmcQJVEHd3\ndy5mYWNlYm9vay5jb21xA3Mu\n','2014-11-21 02:02:30'),('88dcbf112afd3b3b46c112e588261207','ZTAxYWIwYWM0YmY4N2E2ZTlkMzBhNTliNjAxM2Q4OTUyN2VkMDg1YTqAAn1xAShVD19zZXNzaW9u\nX2V4cGlyeXECSoCvGwBVCV9tZXNzYWdlc3EDXXEEY2RqYW5nby5jb250cmliLm1lc3NhZ2VzLnN0\nb3JhZ2UuYmFzZQpNZXNzYWdlCnEFKYFxBn1xByhVCmV4dHJhX3RhZ3NxCFgAAAAAVQdtZXNzYWdl\ncQlYKAAAANCj0YHQv9C10YjQvdC+INCy0L7RiNC70Lgg0LrQsNC6IHVzZXIxMC5VBWxldmVscQpL\nGXViYVUDcmVmVQ4xMjcuMC4wLjE6ODAwMHELVRJfYXV0aF91c2VyX2JhY2tlbmRxDFUpZGphbmdv\nLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmRxDVUNX2F1dGhfdXNlcl9pZHEOigEW\ndS4=\n','2014-06-05 03:59:48'),('8b2c493dc585ec863f532cc9c74579e2','YjdlNjA5MjY1ZGUzM2UwNmYyNmRkNTFkYTk2MWI2NDEzOTgxN2JmMzqAAn1xAVUDcmVmcQJVEjE4\nYjc1ZDM4Lm5ncm9rLmNvbXEDcy4=\n','2014-11-16 04:33:10'),('8c24bf3927760f67b6a04bb1753492ba','NGIxOTg0OGMxNDIzNmNmZTAyNDU3NzE0M2Y0NDMwYWRlNDRhMTA1MDqAAn1xAVUDcmVmVQtleGhp\nYmlhLmNvbXECcy4=\n','2014-11-23 03:46:23'),('8cf02a951d7865ca339978217a706e93','MDQ5Nzg4MGFiMTllYzhiNGM0ZDc2OWE0MjFhYjhiYjY3YmQwYTA5ZjqAAn1xAVUDcmVmVQ93d3cu\nZXhoaWJpYS5jb21xAnMu\n','2014-11-23 01:37:19'),('8d7858ee42643aeec9e76b9df75fcf59','NjZlYzJjMjY3MmNlM2NjZTZiOWQyY2Q2YTU0MGZjNjQzMTY5MzQ5YTqAAn1xAShVD19zZXNzaW9u\nX2V4cGlyeXECSwBVCV9tZXNzYWdlc3EDXXEEY2RqYW5nby5jb250cmliLm1lc3NhZ2VzLnN0b3Jh\nZ2UuYmFzZQpNZXNzYWdlCnEFKYFxBn1xByhVCmV4dHJhX3RhZ3NxCFgAAAAAVQdtZXNzYWdlcQlY\nIwAAAFN1Y2Nlc3NmdWxseSBsb2dnZWQgaW4gYXMgdmxhZGltaXIuVQVsZXZlbHEKSxl1YmFVA3Jl\nZlULZXhoaWJpYS5jb21xC1USX2F1dGhfdXNlcl9iYWNrZW5kcQxVKWRqYW5nby5jb250cmliLmF1\ndGguYmFja2VuZHMuTW9kZWxCYWNrZW5kcQ1VDV9hdXRoX3VzZXJfaWRxDooBF3Uu\n','2014-11-22 04:34:09'),('8fa4a0ab159fcba8d43d633747096053','YjQ5MmJkYTZiZTZjODQ1MjhiMWE0NmE2MzFmNGFjN2M5MTY3NDBjYTqAAn1xAVUDcmVmcQJVDjEy\nNy4wLjAuMTo4MDAwcQNzLg==\n','2014-11-15 05:54:41'),('931d2d75b67a33defd9e10149876f6a6','YjQ5MmJkYTZiZTZjODQ1MjhiMWE0NmE2MzFmNGFjN2M5MTY3NDBjYTqAAn1xAVUDcmVmcQJVDjEy\nNy4wLjAuMTo4MDAwcQNzLg==\n','2014-11-15 05:54:42'),('9402a5e1d91ce1ef506708c37d4d8fef','NGIxOTg0OGMxNDIzNmNmZTAyNDU3NzE0M2Y0NDMwYWRlNDRhMTA1MDqAAn1xAVUDcmVmVQtleGhp\nYmlhLmNvbXECcy4=\n','2014-11-20 01:33:14'),('95d50587c6aa46ce18324c1944e3b51f','MDE4MWM4YjdlM2NmYzdjOWZjMTA3NjM4Y2EzZmYwMDMzYzNiZGIyNTqAAn1xAVUDcmVmcQJVDmxv\nY2FsaG9zdDo4MDAwcQNzLg==\n','2014-11-18 05:22:38'),('9636cc79111d4af6e0ff0f18e767c708','MDQ5Nzg4MGFiMTllYzhiNGM0ZDc2OWE0MjFhYjhiYjY3YmQwYTA5ZjqAAn1xAVUDcmVmVQ93d3cu\nZXhoaWJpYS5jb21xAnMu\n','2014-11-23 01:37:18'),('97d86112452e12462498a8a1b0cf8d4b','MDllMmU3NTI4OGU5MzQ0NGIyMDM3ZjQ5ZWE0NzcwYWZkNzAzMmQyYzqAAn1xAVUDcmVmVQ4xMjcu\nMC4wLjE6ODAwMHECcy4=\n','2014-11-11 04:10:17'),('983d245d6679286be5daaeb834d61de6','Y2UxNmUzZTNjMDM5N2VmMjBkMDFiM2E3MDRjZjBmMDVmZmNlZmZjOTqAAn1xAShVDmZhY2Vib29r\nX3N0YXRlVSBsNndkcllKcU10WmFqblBlN0tkbXpvZzZNWmNwZ1VDU1UDcmVmVQ93d3cuZXhoaWJp\nYS5jb21xAnUu\n','2014-11-23 23:25:40'),('98d0cfa6bdbc8c860f565435a12a4927','YjQ5MmJkYTZiZTZjODQ1MjhiMWE0NmE2MzFmNGFjN2M5MTY3NDBjYTqAAn1xAVUDcmVmcQJVDjEy\nNy4wLjAuMTo4MDAwcQNzLg==\n','2014-11-10 10:53:40'),('9b8e467862c4bd4cd32252c33391c866','N2RkMmVlMWExNGQ0YTI0NjI2ODVhNDA1ODQ1YTE3NjQ4NDkxYWJhMTqAAn1xAShVCnRlc3Rjb29r\naWVVBndvcmtlZFUDcmVmVRIxOGI3NWQzOC5uZ3Jvay5jb21xAnUu\n','2014-11-16 04:52:38'),('9e22fb38c2d9e0197913879c128429ec','YjMxMDI4Mjc3YTA4ZTIwNzM5ZWQ5OWMxMTdmZmQ5ZjgwYjk4YWU4YjqAAn1xAShVA3JlZnECVQ93\nd3cuZXhoaWJpYS5jb21xA1USX2F1dGhfdXNlcl9iYWNrZW5kcQRVKWRqYW5nby5jb250cmliLmF1\ndGguYmFja2VuZHMuTW9kZWxCYWNrZW5kcQVVDV9hdXRoX3VzZXJfaWRxBooBE3Uu\n','2014-11-24 06:11:56'),('a0beb8fcc6449452cdc446c65977377d','MjE0NTlhMDAyZmQyZGQ5YThlMmRkYzcwZTk2MmJhOTM3NjBlZWY4YTqAAn1xAShVD19zZXNzaW9u\nX2V4cGlyeXECSwBVCV9tZXNzYWdlc3EDXXEEY2RqYW5nby5jb250cmliLm1lc3NhZ2VzLnN0b3Jh\nZ2UuYmFzZQpNZXNzYWdlCnEFKYFxBn1xByhVCmV4dHJhX3RhZ3NxCFgAAAAAVQdtZXNzYWdlcQlY\nKgAAANCj0YHQv9C10YjQvdC+INCy0L7RiNC70Lgg0LrQsNC6IHZsYWRpbWlyLlUFbGV2ZWxxCksZ\ndWJhVQNyZWZVC2V4aGliaWEuY29tcQtVEl9hdXRoX3VzZXJfYmFja2VuZHEMVSlkamFuZ28uY29u\ndHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHENVQ1fYXV0aF91c2VyX2lkcQ6KARd1Lg==\n','2014-11-19 05:26:25'),('a140bbe1419fb5520d9fee431a60c5ad','MmY3MWU5Y2UxZmE4NzJhOTc1ZjliMjAzZmM3YjFmYmMyMDQ1N2ViNTqAAn1xAVUDcmVmcQJVDXd3\ndy5nb29nbGUuZnJxA3Mu\n','2014-11-23 05:19:43'),('a3b12869b887d1f29e26505e244d7448','NDRiMmU0MTAxNzI5ZDljNTJhNmFlMzU3NWE0MGJhZDlhZWU3YWQwNjqAAn1xAS4=\n','2014-11-23 11:19:35'),('a5bafb97ce39acdc0c364ad516f98f29','MDQ5Nzg4MGFiMTllYzhiNGM0ZDc2OWE0MjFhYjhiYjY3YmQwYTA5ZjqAAn1xAVUDcmVmVQ93d3cu\nZXhoaWJpYS5jb21xAnMu\n','2014-11-23 09:17:34'),('ac8b198f52dd7f0989502804438dbc61','YjdlNjA5MjY1ZGUzM2UwNmYyNmRkNTFkYTk2MWI2NDEzOTgxN2JmMzqAAn1xAVUDcmVmcQJVEjE4\nYjc1ZDM4Lm5ncm9rLmNvbXEDcy4=\n','2014-11-16 04:33:11'),('ad9e0070a36ebe49452314905c47441f','ZGRlM2E1ODkyNDgxY2QwNTRmOTMxZGIzYjIzNmI5YWM0YWFiZjU5YjqAAn1xAShVE2dvb2dsZS1v\nYXV0aDJfc3RhdGVVIDBBcU41WTlHY2lRZUU2Vk1qOTZrbkZPbU5CblplY1VCVQ1fYXV0aF91c2Vy\nX2lkcQKKARpVHnNvY2lhbF9hdXRoX2xhc3RfbG9naW5fYmFja2VuZHEDVQ1nb29nbGUtb2F1dGgy\ncQRVEl9hdXRoX3VzZXJfYmFja2VuZHEFVS9zb2NpYWxfYXV0aC5iYWNrZW5kcy5nb29nbGUuR29v\nZ2xlT0F1dGgyQmFja2VuZHEGVQ9fc2Vzc2lvbl9leHBpcnlxB2NkYXRldGltZQpkYXRldGltZQpx\nCFUKB94FGgkWEgFAt4VScQlVA3JlZlUPd3d3LmV4aGliaWEuY29tdS4=\n','2014-05-26 09:22:18'),('b16bd77e663634975ab89dd69c1f1f3c','MTYzYjc5YzVmMDA4YjY2MDkyNzU3Y2MzZjBlYzZiYjRkNzRmODRiZDqAAn1xAShVHnR3aXR0ZXJ1\nbmF1dGhvcml6ZWRfdG9rZW5fbmFtZV1xAlWUb2F1dGhfdG9rZW5fc2VjcmV0PXY3UWhGZnk5NkRC\nTG1FM0JXWkV1RkVTZzNITFEzOWc0TndOWGIyaE5DQmsmb2F1dGhfdG9rZW49bllXRjNWOFpnQVBG\namZmczlzY09KNW45ZkloT0FVNHZDQUhwMU9QNThYayZvYXV0aF9jYWxsYmFja19jb25maXJtZWQ9\ndHJ1ZXEDYVUNX2F1dGhfdXNlcl9pZHEEigEQVQ5mYWNlYm9va19zdGF0ZVUga1hBRW9ZbHAzd1RO\nWHRBdlBlQXNpMThiNDA4MzU2M1FVEl9hdXRoX3VzZXJfYmFja2VuZHEFVS1zb2NpYWxfYXV0aC5i\nYWNrZW5kcy5mYWNlYm9vay5GYWNlYm9va0JhY2tlbmRxBlUec29jaWFsX2F1dGhfbGFzdF9sb2dp\nbl9iYWNrZW5kcQdYCAAAAGZhY2Vib29rcQhVD19zZXNzaW9uX2V4cGlyeXEJY2RhdGV0aW1lCmRh\ndGV0aW1lCnEKVQoH3gcVCgIiCFGJhVJxC1UDcmVmVQtleGhpYmlhLmNvbXEMdS4=\n','2014-07-21 10:02:34'),('b32f923098aaad6476d676a51c53f76e','NDE3MjIxMzMzYzJkNWEwZWRjMjdlODMwMThlZjNiODk0ZGZlYjU4MDqAAn1xAVUDcmVmcQJVD3d3\ndy5leGhpYmlhLmNvbXEDcy4=\n','2014-11-23 01:36:07'),('b3c6aab2deb092cba4949328025834fc','OWIwZmUwZGE5MWZkN2IzZWMzM2Q3MjgzNDZjZTYwOGUwN2M4Y2RhNDqAAn1xAShVE2dvb2dsZS1v\nYXV0aDJfc3RhdGVVIGRXY3l1M1JBajhTcGJTQnV5RWtlejl6YjA5bHNxTnBDVQ1fYXV0aF91c2Vy\nX2lkcQKKARpVHnNvY2lhbF9hdXRoX2xhc3RfbG9naW5fYmFja2VuZHEDWA0AAABnb29nbGUtb2F1\ndGgycQRVEl9hdXRoX3VzZXJfYmFja2VuZHEFVS9zb2NpYWxfYXV0aC5iYWNrZW5kcy5nb29nbGUu\nR29vZ2xlT0F1dGgyQmFja2VuZHEGVQ9fc2Vzc2lvbl9leHBpcnlxB2NkYXRldGltZQpkYXRldGlt\nZQpxCFUKB94FGwcDEAohB4VScQlVA3JlZlUPd3d3LmV4aGliaWEuY29tcQp1Lg==\n','2014-05-27 07:03:16'),('b5d5c4b38172273e487f317bf9f6d6c0','YjdlNjA5MjY1ZGUzM2UwNmYyNmRkNTFkYTk2MWI2NDEzOTgxN2JmMzqAAn1xAVUDcmVmcQJVEjE4\nYjc1ZDM4Lm5ncm9rLmNvbXEDcy4=\n','2014-11-16 04:49:10'),('b7ab69dc9cd22a13746e326e2a6c00b6','MDQ5Nzg4MGFiMTllYzhiNGM0ZDc2OWE0MjFhYjhiYjY3YmQwYTA5ZjqAAn1xAVUDcmVmVQ93d3cu\nZXhoaWJpYS5jb21xAnMu\n','2014-11-23 08:11:56'),('b9b32b2bc1fab4fad412a92d64a36e01','MDQ5Nzg4MGFiMTllYzhiNGM0ZDc2OWE0MjFhYjhiYjY3YmQwYTA5ZjqAAn1xAVUDcmVmVQ93d3cu\nZXhoaWJpYS5jb21xAnMu\n','2014-11-20 08:20:46'),('bc2352c6442944c4d9e15d89103e3c1f','YmJmN2YyNWIyODczNTMzZTk2YjMwNmM0NDA1YjliYzYwMzZkN2M1MDqAAn1xAShVCV9tZXNzYWdl\nc3ECXXEDY2RqYW5nby5jb250cmliLm1lc3NhZ2VzLnN0b3JhZ2UuYmFzZQpNZXNzYWdlCnEEKYFx\nBX1xBihVCmV4dHJhX3RhZ3NxB1gAAAAAVQdtZXNzYWdlcQhYKgAAANCj0YHQv9C10YjQvdC+INCy\n0L7RiNC70Lgg0LrQsNC6IHZsYWRpbWlyLlUFbGV2ZWxxCUsZdWJhVQ1fYXV0aF91c2VyX2lkcQqK\nARdVDmZhY2Vib29rX3N0YXRlVSBqM29Ga1EwWEd2dU00aEhKQnRMOXJUNTY4bmxENzNvT1USX2F1\ndGhfdXNlcl9iYWNrZW5kcQtVKWRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNr\nZW5kcQxVD19zZXNzaW9uX2V4cGlyeXENSwBVA3JlZlUObG9jYWxob3N0OjgwMDBxDnUu\n','2014-11-18 05:23:53'),('be49312f308fa7f0dfd201294b6cc4d9','YjdlNjA5MjY1ZGUzM2UwNmYyNmRkNTFkYTk2MWI2NDEzOTgxN2JmMzqAAn1xAVUDcmVmcQJVEjE4\nYjc1ZDM4Lm5ncm9rLmNvbXEDcy4=\n','2014-11-16 04:49:10'),('c24cd86d6145e1a54b9b4a9b96b960c3','NDRiMmU0MTAxNzI5ZDljNTJhNmFlMzU3NWE0MGJhZDlhZWU3YWQwNjqAAn1xAS4=\n','2014-11-11 03:59:50'),('c3eedbe07da16b9bb7480733460f599a','ZWYyZjExNzIzYjg4M2FkZWNiNGM0NDU4YTYxYmUwM2Q2NzlmZWY5YTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZFUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmRVA3Jl\nZlUOMTI3LjAuMC4xOjgwMDBVDV9hdXRoX3VzZXJfaWSKARB1Lg==\n','2014-11-09 03:23:28'),('c99db6e87f5dfe8df3056bbf475e36fe','MTkxMzUxODBkMmM1NTIzYTJjNjIwNzU4NmNjNDVjN2E4NDhhY2ZjZTqAAn1xAShVDmZhY2Vib29r\nX3N0YXRlVSBtT3dQcUwyV3pNWjgyZWhpVTRVc0xBOTY1MXJMQTV1cVUDcmVmVQtleGhpYmlhLmNv\nbXECdS4=\n','2014-11-19 15:56:43'),('cea625a690c1dfc67560d6d005e66b0f','NDE3MjIxMzMzYzJkNWEwZWRjMjdlODMwMThlZjNiODk0ZGZlYjU4MDqAAn1xAVUDcmVmcQJVD3d3\ndy5leGhpYmlhLmNvbXEDcy4=\n','2014-11-23 16:32:29'),('d19284f8ed7e95cb1a23a51e3b2da121','ZTQ2MDQ5ZDExNTk4Y2UwZTY3NjZkY2JkNjQ0M2I1MTE5ZmI3ZWUyMTqAAn1xAVUDcmVmVQlpbmxv\nYWQuaW5xAnMu\n','2014-11-23 03:27:58'),('d3b2e875ddff786c4a8af9235be55fcf','YjQ5MmJkYTZiZTZjODQ1MjhiMWE0NmE2MzFmNGFjN2M5MTY3NDBjYTqAAn1xAVUDcmVmcQJVDjEy\nNy4wLjAuMTo4MDAwcQNzLg==\n','2014-11-15 05:54:42'),('d4f0492191e5e94d03ea7414fb680148','YjdlNjA5MjY1ZGUzM2UwNmYyNmRkNTFkYTk2MWI2NDEzOTgxN2JmMzqAAn1xAVUDcmVmcQJVEjE4\nYjc1ZDM4Lm5ncm9rLmNvbXEDcy4=\n','2014-11-16 04:49:10'),('d54f914ae55749a1eaca9fffa2f89ff8','ZjM5MWYwYzRiOGU2YTE3ZWE2NTI2ZGE2ZWZlMDMzZjFkNzE0MGUzMzqAAn1xAVUDcmVmcQJVDXd3\ndy5iYWlkdS5jb21xA3Mu\n','2014-11-23 08:40:12'),('d5fdccdea7efc345777294f62d2c6c8a','MTkwMGM3MWM1MmMzMTQwMDFlMmNkY2JkYjhlNmJlMWQ2NDg2OWZjMjqAAn1xAVUDcmVmVRIxOGI3\nNWQzOC5uZ3Jvay5jb21xAnMu\n','2014-11-16 05:06:34'),('d70bf10912eba16b0324150e8a894a5f','YjdlNjA5MjY1ZGUzM2UwNmYyNmRkNTFkYTk2MWI2NDEzOTgxN2JmMzqAAn1xAVUDcmVmcQJVEjE4\nYjc1ZDM4Lm5ncm9rLmNvbXEDcy4=\n','2014-11-16 04:49:09'),('d8235e4b1196a362579e953e5932153b','MDllMmU3NTI4OGU5MzQ0NGIyMDM3ZjQ5ZWE0NzcwYWZkNzAzMmQyYzqAAn1xAVUDcmVmVQ4xMjcu\nMC4wLjE6ODAwMHECcy4=\n','2014-11-15 05:54:43'),('db405ae0ddc6df0814d2f395e63bec81','YjdlNjA5MjY1ZGUzM2UwNmYyNmRkNTFkYTk2MWI2NDEzOTgxN2JmMzqAAn1xAVUDcmVmcQJVEjE4\nYjc1ZDM4Lm5ncm9rLmNvbXEDcy4=\n','2014-11-16 04:49:10'),('dbd4f19fd531c1811a4501393d7b533c','YjdlNjA5MjY1ZGUzM2UwNmYyNmRkNTFkYTk2MWI2NDEzOTgxN2JmMzqAAn1xAVUDcmVmcQJVEjE4\nYjc1ZDM4Lm5ncm9rLmNvbXEDcy4=\n','2014-11-16 04:49:10'),('deef2ef45ed9f165d037766a11d892f3','MDQ5Nzg4MGFiMTllYzhiNGM0ZDc2OWE0MjFhYjhiYjY3YmQwYTA5ZjqAAn1xAVUDcmVmVQ93d3cu\nZXhoaWJpYS5jb21xAnMu\n','2014-11-23 01:37:18'),('e47cefcdca9a93d3253019db3aa97560','MDllMmU3NTI4OGU5MzQ0NGIyMDM3ZjQ5ZWE0NzcwYWZkNzAzMmQyYzqAAn1xAVUDcmVmVQ4xMjcu\nMC4wLjE6ODAwMHECcy4=\n','2014-11-12 03:45:10'),('eb5101286e3d94841e6f8e4c6d92922b','YjdlNjA5MjY1ZGUzM2UwNmYyNmRkNTFkYTk2MWI2NDEzOTgxN2JmMzqAAn1xAVUDcmVmcQJVEjE4\nYjc1ZDM4Lm5ncm9rLmNvbXEDcy4=\n','2014-11-16 04:33:11'),('f1661c4e3ccfd97a97d177da8cecf6f0','MTA5NGI0ZDYxNjgyYzdkZGU3ZGRjZDk1ODA3Y2E1ZGRkNzZiMDVhZjqAAn1xAShVDV9hdXRoX3Vz\nZXJfaWRxAooBGVUOZmFjZWJvb2tfc3RhdGVVIEJuTWRHRnI3dUtBNEhjdHNoeWZaS1p3U21QUkRv\nbmxiVRJfYXV0aF91c2VyX2JhY2tlbmRxA1Utc29jaWFsX2F1dGguYmFja2VuZHMuZmFjZWJvb2su\nRmFjZWJvb2tCYWNrZW5kcQRVHnNvY2lhbF9hdXRoX2xhc3RfbG9naW5fYmFja2VuZHEFVQhmYWNl\nYm9va3EGVQ9fc2Vzc2lvbl9leHBpcnlxB2NkYXRldGltZQpkYXRldGltZQpxCFUKB94HFgcuAAj9\n6oVScQlVA3JlZlULZXhoaWJpYS5jb21xCnUu\n','2014-07-22 07:46:00'),('f2086eef1621060b1aee1834dbcada7a','MDQ5Nzg4MGFiMTllYzhiNGM0ZDc2OWE0MjFhYjhiYjY3YmQwYTA5ZjqAAn1xAVUDcmVmVQ93d3cu\nZXhoaWJpYS5jb21xAnMu\n','2014-11-23 14:31:55'),('f27ff5d99644ec88e3b291b999e37430','NDE3MjIxMzMzYzJkNWEwZWRjMjdlODMwMThlZjNiODk0ZGZlYjU4MDqAAn1xAVUDcmVmcQJVD3d3\ndy5leGhpYmlhLmNvbXEDcy4=\n','2014-11-23 13:09:07'),('f65b33739bbc1f9f85f801f161d45f8c','MDQ5Nzg4MGFiMTllYzhiNGM0ZDc2OWE0MjFhYjhiYjY3YmQwYTA5ZjqAAn1xAVUDcmVmVQ93d3cu\nZXhoaWJpYS5jb21xAnMu\n','2014-11-19 18:27:21'),('f907376c7c45fbb3b68536b8355718d9','NmI2OTExMTJhOGFlMmY0NDI0NDE5MWNlYWE2OTI3YzU1M2VhNmEyYTqAAn1xAVUDcmVmcQJVC2V4\naGliaWEuY29tcQNzLg==\n','2014-11-23 04:52:47'),('f95aecbb9e2f4c534e41278cebfaa81d','OTUyNWU1NDRiZDNmNWJkOWNhZjg3YjJjZjRkMzc3Zjg2NjAzYmU0MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZFUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmRVDV9h\ndXRoX3VzZXJfaWSKARBVA3JlZlUOMTI3LjAuMC4xOjgwMDBVD19zZXNzaW9uX2V4cGlyeUqArxsA\ndS4=\n','2014-06-03 08:28:47'),('fa2c04ed62b88d705a84df19b94713cd','NDE3MjIxMzMzYzJkNWEwZWRjMjdlODMwMThlZjNiODk0ZGZlYjU4MDqAAn1xAVUDcmVmcQJVD3d3\ndy5leGhpYmlhLmNvbXEDcy4=\n','2014-11-21 09:14:17'),('fb313ae51d2c6d19042a848dbb6527b4','MDQ5Nzg4MGFiMTllYzhiNGM0ZDc2OWE0MjFhYjhiYjY3YmQwYTA5ZjqAAn1xAVUDcmVmVQ93d3cu\nZXhoaWJpYS5jb21xAnMu\n','2014-11-19 05:43:21'),('fc83360f44d167fbd74c289bc288002e','MDQ5Nzg4MGFiMTllYzhiNGM0ZDc2OWE0MjFhYjhiYjY3YmQwYTA5ZjqAAn1xAVUDcmVmVQ93d3cu\nZXhoaWJpYS5jb21xAnMu\n','2014-11-23 01:37:19');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'glacial-depths-3204.herokuapp.com','Exhibia');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `easy_thumbnails_source`
--

DROP TABLE IF EXISTS `easy_thumbnails_source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `easy_thumbnails_source` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `modified` datetime NOT NULL,
  `storage_hash` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `easy_thumbnails_source_name_7549c98cc6dd6969_uniq` (`name`,`storage_hash`),
  KEY `easy_thumbnails_source_52094d6e` (`name`),
  KEY `easy_thumbnails_source_3a997c55` (`storage_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `easy_thumbnails_source`
--

LOCK TABLES `easy_thumbnails_source` WRITE;
/*!40000 ALTER TABLE `easy_thumbnails_source` DISABLE KEYS */;
/*!40000 ALTER TABLE `easy_thumbnails_source` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `easy_thumbnails_thumbnail`
--

DROP TABLE IF EXISTS `easy_thumbnails_thumbnail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `easy_thumbnails_thumbnail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `modified` datetime NOT NULL,
  `source_id` int(11) NOT NULL,
  `storage_hash` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `easy_thumbnails_thumbnail_source_id_1f50d53db8191480_uniq` (`source_id`,`name`,`storage_hash`),
  KEY `easy_thumbnails_thumbnail_89f89e85` (`source_id`),
  KEY `easy_thumbnails_thumbnail_52094d6e` (`name`),
  KEY `easy_thumbnails_thumbnail_3a997c55` (`storage_hash`),
  CONSTRAINT `source_id_refs_id_38c628a45bffe8f5` FOREIGN KEY (`source_id`) REFERENCES `easy_thumbnails_source` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `easy_thumbnails_thumbnail`
--

LOCK TABLES `easy_thumbnails_thumbnail` WRITE;
/*!40000 ALTER TABLE `easy_thumbnails_thumbnail` DISABLE KEYS */;
/*!40000 ALTER TABLE `easy_thumbnails_thumbnail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emailconfirmation_emailaddress`
--

DROP TABLE IF EXISTS `emailconfirmation_emailaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emailconfirmation_emailaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `email` varchar(75) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`email`),
  KEY `emailconfirmation_emailaddress_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_f6e307c0` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emailconfirmation_emailaddress`
--

LOCK TABLES `emailconfirmation_emailaddress` WRITE;
/*!40000 ALTER TABLE `emailconfirmation_emailaddress` DISABLE KEYS */;
INSERT INTO `emailconfirmation_emailaddress` VALUES (1,16,'a@a.com',1,1),(2,17,'u@u.com',1,1),(3,18,'u1@u1.com',1,1),(4,19,'u2@u2.com',1,1),(5,20,'u3@u3.com',1,1),(6,21,'u4@u4.com',1,1),(7,22,'u10@u10.com',1,1),(8,23,'v@abclosute.com',1,1);
/*!40000 ALTER TABLE `emailconfirmation_emailaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emailconfirmation_emailconfirmation`
--

DROP TABLE IF EXISTS `emailconfirmation_emailconfirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emailconfirmation_emailconfirmation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email_address_id` int(11) NOT NULL,
  `sent` datetime NOT NULL,
  `confirmation_key` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `emailconfirmation_emailconfirmation_1df9fea4` (`email_address_id`),
  CONSTRAINT `email_address_id_refs_id_344d8787` FOREIGN KEY (`email_address_id`) REFERENCES `emailconfirmation_emailaddress` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emailconfirmation_emailconfirmation`
--

LOCK TABLES `emailconfirmation_emailconfirmation` WRITE;
/*!40000 ALTER TABLE `emailconfirmation_emailconfirmation` DISABLE KEYS */;
/*!40000 ALTER TABLE `emailconfirmation_emailconfirmation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mailer_dontsendentry`
--

DROP TABLE IF EXISTS `mailer_dontsendentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mailer_dontsendentry` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `to_address` varchar(50) NOT NULL,
  `when_added` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mailer_dontsendentry`
--

LOCK TABLES `mailer_dontsendentry` WRITE;
/*!40000 ALTER TABLE `mailer_dontsendentry` DISABLE KEYS */;
/*!40000 ALTER TABLE `mailer_dontsendentry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mailer_message`
--

DROP TABLE IF EXISTS `mailer_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mailer_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `to_address` varchar(50) NOT NULL,
  `from_address` varchar(50) NOT NULL,
  `subject` varchar(100) NOT NULL,
  `message_body` longtext NOT NULL,
  `when_added` datetime NOT NULL,
  `priority` varchar(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mailer_message`
--

LOCK TABLES `mailer_message` WRITE;
/*!40000 ALTER TABLE `mailer_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `mailer_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mailer_messagelog`
--

DROP TABLE IF EXISTS `mailer_messagelog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mailer_messagelog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `to_address` varchar(50) NOT NULL,
  `from_address` varchar(50) NOT NULL,
  `subject` varchar(100) NOT NULL,
  `message_body` longtext NOT NULL,
  `when_added` datetime NOT NULL,
  `priority` varchar(1) NOT NULL,
  `when_attempted` datetime NOT NULL,
  `result` varchar(1) NOT NULL,
  `log_message` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mailer_messagelog`
--

LOCK TABLES `mailer_messagelog` WRITE;
/*!40000 ALTER TABLE `mailer_messagelog` DISABLE KEYS */;
/*!40000 ALTER TABLE `mailer_messagelog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification_notice`
--

DROP TABLE IF EXISTS `notification_notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notification_notice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `recipient_id` int(11) NOT NULL,
  `sender_id` int(11) DEFAULT NULL,
  `message` longtext NOT NULL,
  `notice_type_id` int(11) NOT NULL,
  `added` datetime NOT NULL,
  `unseen` tinyint(1) NOT NULL,
  `archived` tinyint(1) NOT NULL,
  `on_site` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notification_notice_fcd09624` (`recipient_id`),
  KEY `notification_notice_901f59e9` (`sender_id`),
  KEY `notification_notice_f28cbfcc` (`notice_type_id`),
  CONSTRAINT `notice_type_id_refs_id_ded2a8d9` FOREIGN KEY (`notice_type_id`) REFERENCES `notification_noticetype` (`id`),
  CONSTRAINT `recipient_id_refs_id_96f3ba2f` FOREIGN KEY (`recipient_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `sender_id_refs_id_96f3ba2f` FOREIGN KEY (`sender_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification_notice`
--

LOCK TABLES `notification_notice` WRITE;
/*!40000 ALTER TABLE `notification_notice` DISABLE KEYS */;
/*!40000 ALTER TABLE `notification_notice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification_noticequeuebatch`
--

DROP TABLE IF EXISTS `notification_noticequeuebatch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notification_noticequeuebatch` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pickled_data` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification_noticequeuebatch`
--

LOCK TABLES `notification_noticequeuebatch` WRITE;
/*!40000 ALTER TABLE `notification_noticequeuebatch` DISABLE KEYS */;
INSERT INTO `notification_noticequeuebatch` VALUES (1,'KGxwMQooTDE2TApTJ2Fubm91bmNlbWVudCcKcDIKKGRwMwpnMgpjZGphbmdvLmRiLm1vZGVscy5i\nYXNlCm1vZGVsX3VucGlja2xlCnA0CihjYW5ub3VuY2VtZW50cy5tb2RlbHMKQW5ub3VuY2VtZW50\nCnA1CihsY2RqYW5nby5kYi5tb2RlbHMuYmFzZQpzaW1wbGVfY2xhc3NfZmFjdG9yeQpwNgp0UnA3\nCihkcDgKUyd0aXRsZScKcDkKVnJ3cndyd3IKcDEwCnNTJ3NpdGVfd2lkZScKcDExCkkwMQpzUydf\nc3RhdGUnCnAxMgpjY29weV9yZWcKX3JlY29uc3RydWN0b3IKcDEzCihjZGphbmdvLmRiLm1vZGVs\ncy5iYXNlCk1vZGVsU3RhdGUKcDE0CmNfX2J1aWx0aW5fXwpvYmplY3QKcDE1Ck50UnAxNgooZHAx\nNwpTJ2FkZGluZycKcDE4CkkwMQpzUydkYicKcDE5Ck5zYnNTJ2NyZWF0aW9uX2RhdGUnCnAyMApj\nZGF0ZXRpbWUKZGF0ZXRpbWUKcDIxCihTJ1x4MDdceGRlXHgwNVxyXG4qOFx4MGJceGRiIicKdFJw\nMjIKc1MnY29udGVudCcKcDIzClZyd3J3cncKcDI0CnNTJ2NyZWF0b3JfaWQnCnAyNQpOc1MnbWVt\nYmVyc19vbmx5JwpwMjYKSTAxCnNTJ2lkJwpwMjcKTnNic0kwMApOdHAyOAphKEwxN0wKZzIKZzMK\nSTAwCk50cDI5CmEu\n');
/*!40000 ALTER TABLE `notification_noticequeuebatch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification_noticesetting`
--

DROP TABLE IF EXISTS `notification_noticesetting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notification_noticesetting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `notice_type_id` int(11) NOT NULL,
  `medium` varchar(1) NOT NULL,
  `send` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`notice_type_id`,`medium`),
  KEY `notification_noticesetting_fbfc09f1` (`user_id`),
  KEY `notification_noticesetting_f28cbfcc` (`notice_type_id`),
  CONSTRAINT `notice_type_id_refs_id_1024de5c` FOREIGN KEY (`notice_type_id`) REFERENCES `notification_noticetype` (`id`),
  CONSTRAINT `user_id_refs_id_f73ac69a` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification_noticesetting`
--

LOCK TABLES `notification_noticesetting` WRITE;
/*!40000 ALTER TABLE `notification_noticesetting` DISABLE KEYS */;
/*!40000 ALTER TABLE `notification_noticesetting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification_noticetype`
--

DROP TABLE IF EXISTS `notification_noticetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notification_noticetype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label` varchar(40) NOT NULL,
  `display` varchar(50) NOT NULL,
  `description` varchar(100) NOT NULL,
  `default` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification_noticetype`
--

LOCK TABLES `notification_noticetype` WRITE;
/*!40000 ALTER TABLE `notification_noticetype` DISABLE KEYS */;
INSERT INTO `notification_noticetype` VALUES (1,'announcement','Announcement','you have received an announcement',2);
/*!40000 ALTER TABLE `notification_noticetype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification_observeditem`
--

DROP TABLE IF EXISTS `notification_observeditem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notification_observeditem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `object_id` int(10) unsigned NOT NULL,
  `notice_type_id` int(11) NOT NULL,
  `added` datetime NOT NULL,
  `signal` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notification_observeditem_fbfc09f1` (`user_id`),
  KEY `notification_observeditem_e4470c6e` (`content_type_id`),
  KEY `notification_observeditem_f28cbfcc` (`notice_type_id`),
  CONSTRAINT `content_type_id_refs_id_93de09d8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `notice_type_id_refs_id_b4f670c2` FOREIGN KEY (`notice_type_id`) REFERENCES `notification_noticetype` (`id`),
  CONSTRAINT `user_id_refs_id_8aaa082c` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification_observeditem`
--

LOCK TABLES `notification_observeditem` WRITE;
/*!40000 ALTER TABLE `notification_observeditem` DISABLE KEYS */;
/*!40000 ALTER TABLE `notification_observeditem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_auctionorder`
--

DROP TABLE IF EXISTS `payments_auctionorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payments_auctionorder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `auction_id` int(11) NOT NULL,
  `winner_id` int(11) NOT NULL,
  `amount_paid` decimal(7,2) NOT NULL,
  `method` varchar(3) NOT NULL,
  `status` varchar(3) NOT NULL,
  `pn_id` int(11) DEFAULT NULL,
  `extra_info` varchar(255) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payments_auctionorder_3e820c5c` (`auction_id`),
  KEY `payments_auctionorder_a703c31d` (`winner_id`),
  KEY `payments_auctionorder_edd00aa4` (`pn_id`),
  CONSTRAINT `auction_id_refs_id_a86b1967` FOREIGN KEY (`auction_id`) REFERENCES `auctions_auction` (`id`),
  CONSTRAINT `pn_id_refs_id_e05f6dbe` FOREIGN KEY (`pn_id`) REFERENCES `payments_paymentnotification` (`id`),
  CONSTRAINT `winner_id_refs_id_acd2ada0` FOREIGN KEY (`winner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_auctionorder`
--

LOCK TABLES `payments_auctionorder` WRITE;
/*!40000 ALTER TABLE `payments_auctionorder` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_auctionorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_card`
--

DROP TABLE IF EXISTS `payments_card`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payments_card` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `number` varchar(30) NOT NULL,
  `holder_name` varchar(70) NOT NULL,
  `expiration_month` smallint(5) unsigned NOT NULL,
  `expiration_year` smallint(5) unsigned NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payments_card_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_80d130a7` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_card`
--

LOCK TABLES `payments_card` WRITE;
/*!40000 ALTER TABLE `payments_card` DISABLE KEYS */;
INSERT INTO `payments_card` VALUES (2,16,'1234567890','fdfdfd',9,3423,1,'2014-05-22 08:06:31');
/*!40000 ALTER TABLE `payments_card` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_creditpackageorder`
--

DROP TABLE IF EXISTS `payments_creditpackageorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payments_creditpackageorder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `buyer_id` int(11) NOT NULL,
  `item_id` varchar(15) DEFAULT NULL,
  `amount_paid` decimal(7,2) NOT NULL,
  `pn_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payments_creditpackageorder_e99ab0` (`buyer_id`),
  KEY `payments_creditpackageorder_67b70d25` (`item_id`),
  KEY `payments_creditpackageorder_edd00aa4` (`pn_id`),
  CONSTRAINT `buyer_id_refs_id_7d83364c` FOREIGN KEY (`buyer_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `item_id_refs_code_8d1e3298` FOREIGN KEY (`item_id`) REFERENCES `auctions_auctionitem` (`code`),
  CONSTRAINT `pn_id_refs_id_980dabfe` FOREIGN KEY (`pn_id`) REFERENCES `payments_paymentnotification` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_creditpackageorder`
--

LOCK TABLES `payments_creditpackageorder` WRITE;
/*!40000 ALTER TABLE `payments_creditpackageorder` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_creditpackageorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_paymentnotification`
--

DROP TABLE IF EXISTS `payments_paymentnotification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payments_paymentnotification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(255) NOT NULL,
  `type` varchar(25) NOT NULL,
  `status` varchar(25) NOT NULL,
  `item_name` varchar(50) NOT NULL,
  `item_number` varchar(15) NOT NULL,
  `quantity` smallint(6) DEFAULT NULL,
  `shipping` decimal(7,2) DEFAULT NULL,
  `payer_email` varchar(150) NOT NULL,
  `mc_gross` decimal(7,2) DEFAULT NULL,
  `custom1` varchar(20) DEFAULT NULL,
  `custom2` varchar(20) DEFAULT NULL,
  `request_log` longtext NOT NULL,
  `data` longtext NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_paymentnotification`
--

LOCK TABLES `payments_paymentnotification` WRITE;
/*!40000 ALTER TABLE `payments_paymentnotification` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_paymentnotification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `points_store_boughtitem`
--

DROP TABLE IF EXISTS `points_store_boughtitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `points_store_boughtitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `bought_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `points_store_boughtitem_fbfc09f1` (`user_id`),
  KEY `points_store_boughtitem_67b70d25` (`item_id`),
  CONSTRAINT `item_id_refs_id_94934db0` FOREIGN KEY (`item_id`) REFERENCES `points_store_storeitem` (`id`),
  CONSTRAINT `user_id_refs_id_f2504a7b` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `points_store_boughtitem`
--

LOCK TABLES `points_store_boughtitem` WRITE;
/*!40000 ALTER TABLE `points_store_boughtitem` DISABLE KEYS */;
INSERT INTO `points_store_boughtitem` VALUES (1,22,1,'2014-05-16 09:00:47');
/*!40000 ALTER TABLE `points_store_boughtitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `points_store_storeitem`
--

DROP TABLE IF EXISTS `points_store_storeitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `points_store_storeitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_type` smallint(5) unsigned NOT NULL,
  `cost` smallint(5) unsigned NOT NULL,
  `duration` int(10) unsigned NOT NULL,
  `description` longtext NOT NULL,
  `image` varchar(100) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `points_store_storeitem`
--

LOCK TABLES `points_store_storeitem` WRITE;
/*!40000 ALTER TABLE `points_store_storeitem` DISABLE KEYS */;
INSERT INTO `points_store_storeitem` VALUES (1,1,4646,244,'store Item\r\nпокупаня типа?','/var/www/Competitive-Social-Shopping-Django/exhibia/images/super-man-icon.png',1);
/*!40000 ALTER TABLE `points_store_storeitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profiles_bannedipaddress`
--

DROP TABLE IF EXISTS `profiles_bannedipaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `profiles_bannedipaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `IPAddress` char(15) NOT NULL,
  `created_at` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profiles_bannedipaddress`
--

LOCK TABLES `profiles_bannedipaddress` WRITE;
/*!40000 ALTER TABLE `profiles_bannedipaddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `profiles_bannedipaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profiles_billingaddress`
--

DROP TABLE IF EXISTS `profiles_billingaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `profiles_billingaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `address1` varchar(100) NOT NULL,
  `address2` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(30) NOT NULL,
  `country` varchar(2) NOT NULL,
  `zip_code` varchar(10) NOT NULL,
  `phone` varchar(30) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `profiles_billingaddress_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_9d44825f` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profiles_billingaddress`
--

LOCK TABLES `profiles_billingaddress` WRITE;
/*!40000 ALTER TABLE `profiles_billingaddress` DISABLE KEYS */;
INSERT INTO `profiles_billingaddress` VALUES (1,16,'Anthony','Poddubny','Kharkiv','Kharkiv','Kharkiv','AL','UA','61045','063-897-4469',0,'2014-05-22 08:08:19');
/*!40000 ALTER TABLE `profiles_billingaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profiles_ipaddress`
--

DROP TABLE IF EXISTS `profiles_ipaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `profiles_ipaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `IPAddress` char(15) NOT NULL,
  `last_login` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`IPAddress`),
  KEY `profiles_ipaddress_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_6ea9aa38` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profiles_ipaddress`
--

LOCK TABLES `profiles_ipaddress` WRITE;
/*!40000 ALTER TABLE `profiles_ipaddress` DISABLE KEYS */;
INSERT INTO `profiles_ipaddress` VALUES (1,16,'127.0.0.1','2014-05-28'),(2,17,'127.0.0.1','2014-05-16'),(3,18,'127.0.0.1','2014-05-19'),(4,22,'127.0.0.1','2014-05-15'),(5,23,'127.0.0.1','2014-05-26'),(6,24,'127.0.0.1','2014-05-23'),(7,25,'127.0.0.1','2014-05-23'),(8,26,'127.0.0.1','2014-05-27'),(9,27,'127.0.0.1','2014-05-27'),(10,28,'127.0.0.1','2014-05-27'),(11,19,'127.0.0.1','2014-05-28');
/*!40000 ALTER TABLE `profiles_ipaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profiles_member`
--

DROP TABLE IF EXISTS `profiles_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `profiles_member` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `about` longtext,
  `location` varchar(40) DEFAULT NULL,
  `website` varchar(200) DEFAULT NULL,
  `credits` int(10) unsigned NOT NULL,
  `address1` varchar(100) NOT NULL,
  `address2` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `zip_code` varchar(10) NOT NULL,
  `state` varchar(30) DEFAULT NULL,
  `phone` varchar(30) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `referer` varchar(100) DEFAULT NULL,
  `referral_url_id` int(11) DEFAULT NULL,
  `is_banned` tinyint(1) NOT NULL,
  `points_amount` int(10) unsigned NOT NULL,
  `verified` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `profiles_member_4e9306a1` (`referral_url_id`),
  CONSTRAINT `referral_url_id_refs_id_e4fdcbc9` FOREIGN KEY (`referral_url_id`) REFERENCES `referrals_referrallink` (`id`),
  CONSTRAINT `user_id_refs_id_c2f55de0` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profiles_member`
--

LOCK TABLES `profiles_member` WRITE;
/*!40000 ALTER TABLE `profiles_member` DISABLE KEYS */;
INSERT INTO `profiles_member` VALUES (16,16,NULL,NULL,NULL,49772,'','','','',NULL,NULL,NULL,NULL,NULL,0,263,0),(17,17,'','','',8537,'','','','','','',NULL,'',NULL,1,66,0),(18,18,NULL,NULL,NULL,5,'','','','',NULL,NULL,NULL,NULL,NULL,0,20,0),(19,19,NULL,NULL,NULL,3,'','','','',NULL,NULL,NULL,NULL,NULL,0,0,0),(20,20,NULL,NULL,NULL,3,'','','','',NULL,NULL,NULL,NULL,NULL,0,0,0),(21,21,NULL,NULL,NULL,3,'','','','',NULL,NULL,NULL,NULL,NULL,0,0,0),(22,22,NULL,NULL,NULL,2,'','','','',NULL,NULL,NULL,NULL,NULL,0,1,0),(23,23,NULL,NULL,NULL,2850,'','','','',NULL,NULL,NULL,NULL,NULL,0,24,0),(24,24,NULL,NULL,NULL,13,'','','','',NULL,NULL,NULL,NULL,NULL,0,2,1),(25,25,NULL,NULL,NULL,3,'','','','',NULL,NULL,NULL,NULL,NULL,0,1,1),(26,26,NULL,NULL,NULL,3,'','','','',NULL,NULL,NULL,NULL,NULL,0,0,0),(27,27,NULL,NULL,NULL,3,'','','','',NULL,NULL,NULL,NULL,NULL,0,0,0),(28,28,NULL,NULL,NULL,3,'','','','',NULL,NULL,NULL,NULL,NULL,0,1,1);
/*!40000 ALTER TABLE `profiles_member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `redisboard_redisserver`
--

DROP TABLE IF EXISTS `redisboard_redisserver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `redisboard_redisserver` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(250) NOT NULL,
  `port` int(11) DEFAULT NULL,
  `password` varchar(250) DEFAULT NULL,
  `sampling_threshold` int(11) NOT NULL,
  `sampling_size` int(11) NOT NULL,
  `label` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `redisboard_redisserver_hostname_7832dbdbfa8f6a20_uniq` (`hostname`,`port`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `redisboard_redisserver`
--

LOCK TABLES `redisboard_redisserver` WRITE;
/*!40000 ALTER TABLE `redisboard_redisserver` DISABLE KEYS */;
INSERT INTO `redisboard_redisserver` VALUES (1,'localhost',6379,'',1000,200,'chat');
/*!40000 ALTER TABLE `redisboard_redisserver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `referrals_referrallink`
--

DROP TABLE IF EXISTS `referrals_referrallink`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `referrals_referrallink` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `redirect_to` varchar(500) NOT NULL,
  `visit_count` int(10) unsigned NOT NULL,
  `is_blocked` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `referrals_referrallink_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_f8f90004` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `referrals_referrallink`
--

LOCK TABLES `referrals_referrallink` WRITE;
/*!40000 ALTER TABLE `referrals_referrallink` DISABLE KEYS */;
INSERT INTO `referrals_referrallink` VALUES (1,16,'/',0,0,'2014-05-12 11:55:58'),(2,17,'/',0,0,'2014-05-13 08:06:42'),(3,18,'/',0,0,'2014-05-14 09:40:39'),(4,19,'/',0,0,'2014-05-14 09:40:57'),(5,20,'/',0,0,'2014-05-14 09:41:18'),(6,21,'/',0,0,'2014-05-14 09:41:38'),(7,22,'/',0,0,'2014-05-15 03:58:02'),(8,23,'/',0,0,'2014-05-22 05:23:38'),(9,24,'/',0,0,'2014-05-23 07:24:25'),(10,25,'/',0,0,'2014-05-23 07:46:00'),(11,26,'/',0,0,'2014-05-26 08:22:17'),(12,27,'/',0,0,'2014-05-27 06:05:27'),(13,28,'/',0,0,'2014-05-27 08:36:44');
/*!40000 ALTER TABLE `referrals_referrallink` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shipping_shippingaddress`
--

DROP TABLE IF EXISTS `shipping_shippingaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shipping_shippingaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `address1` varchar(100) NOT NULL,
  `address2` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(30) NOT NULL,
  `country` varchar(2) NOT NULL,
  `zip_code` varchar(10) NOT NULL,
  `phone` varchar(30) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `shipping_shippingaddress_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_a124a987` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shipping_shippingaddress`
--

LOCK TABLES `shipping_shippingaddress` WRITE;
/*!40000 ALTER TABLE `shipping_shippingaddress` DISABLE KEYS */;
INSERT INTO `shipping_shippingaddress` VALUES (1,16,'Anthony','Poddubny','Kharkiv','','Kharkiv','AL','UA','61045','063-897-4469',1,'2014-05-22 08:08:19');
/*!40000 ALTER TABLE `shipping_shippingaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shipping_shippingfee`
--

DROP TABLE IF EXISTS `shipping_shippingfee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shipping_shippingfee` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_id` varchar(15) NOT NULL,
  `country` varchar(2) NOT NULL,
  `shipping` varchar(3) NOT NULL,
  `price` decimal(7,2) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `shipping_shippingfee_67b70d25` (`item_id`),
  CONSTRAINT `item_id_refs_code_4dca9d29` FOREIGN KEY (`item_id`) REFERENCES `auctions_auctionitem` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shipping_shippingfee`
--

LOCK TABLES `shipping_shippingfee` WRITE;
/*!40000 ALTER TABLE `shipping_shippingfee` DISABLE KEYS */;
INSERT INTO `shipping_shippingfee` VALUES (1,'sladkaya-1999','US','SS',10.00,'2014-05-28 06:16:45'),(2,'roland-juno-d','US','SSD',35.00,'2014-05-28 06:17:04'),(3,'Playstation4','US','SS',20.00,'2014-05-28 06:17:22'),(4,'exhibia20bids','US','SE',18.00,'2014-05-28 06:17:44');
/*!40000 ALTER TABLE `shipping_shippingfee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shipping_shippingrequest`
--

DROP TABLE IF EXISTS `shipping_shippingrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shipping_shippingrequest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `auction_id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `address1` varchar(100) NOT NULL,
  `address2` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(30) NOT NULL,
  `country` varchar(2) NOT NULL,
  `zip_code` varchar(10) NOT NULL,
  `phone` varchar(30) NOT NULL,
  `waiting` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `shipping_shippingrequest_user_id_6bf5500e2ffdf033_uniq` (`user_id`,`auction_id`),
  KEY `shipping_shippingrequest_fbfc09f1` (`user_id`),
  KEY `shipping_shippingrequest_3e820c5c` (`auction_id`),
  CONSTRAINT `auction_id_refs_id_3fb5164982de7493` FOREIGN KEY (`auction_id`) REFERENCES `auctions_auction` (`id`),
  CONSTRAINT `user_id_refs_id_333e7ddf77a5d6b2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shipping_shippingrequest`
--

LOCK TABLES `shipping_shippingrequest` WRITE;
/*!40000 ALTER TABLE `shipping_shippingrequest` DISABLE KEYS */;
INSERT INTO `shipping_shippingrequest` VALUES (9,23,117,'Anthony','Poddubny','Kharkiv','fsfs','Kharkiv','AL','UA','61045','063-897-4469',1,'2014-05-27 05:41:11'),(10,23,119,'Anthony','Poddubny','Kharkiv','fsfs','Kharkiv','AL','UA','61045','063-897-4469',1,'2014-05-27 05:41:30'),(11,16,119,'Vladimir','Tsyupko','Kremenchuk','','Poltava','AK','AX','61009','063-897-4469',1,'2014-05-27 05:41:50');
/*!40000 ALTER TABLE `shipping_shippingrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `signup_codes_signupcode`
--

DROP TABLE IF EXISTS `signup_codes_signupcode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `signup_codes_signupcode` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(40) NOT NULL,
  `max_uses` int(10) unsigned NOT NULL,
  `expiry` datetime DEFAULT NULL,
  `inviter_id` int(11) DEFAULT NULL,
  `email` varchar(75) NOT NULL,
  `notes` longtext NOT NULL,
  `sent` datetime DEFAULT NULL,
  `created` datetime NOT NULL,
  `use_count` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `signup_codes_signupcode_74fccd78` (`inviter_id`),
  CONSTRAINT `inviter_id_refs_id_f2c7bcc6` FOREIGN KEY (`inviter_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `signup_codes_signupcode`
--

LOCK TABLES `signup_codes_signupcode` WRITE;
/*!40000 ALTER TABLE `signup_codes_signupcode` DISABLE KEYS */;
/*!40000 ALTER TABLE `signup_codes_signupcode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `signup_codes_signupcoderesult`
--

DROP TABLE IF EXISTS `signup_codes_signupcoderesult`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `signup_codes_signupcoderesult` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `signup_code_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `signup_codes_signupcoderesult_16afc873` (`signup_code_id`),
  KEY `signup_codes_signupcoderesult_fbfc09f1` (`user_id`),
  CONSTRAINT `signup_code_id_refs_id_414a75ea` FOREIGN KEY (`signup_code_id`) REFERENCES `signup_codes_signupcode` (`id`),
  CONSTRAINT `user_id_refs_id_13a21fc7` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `signup_codes_signupcoderesult`
--

LOCK TABLES `signup_codes_signupcoderesult` WRITE;
/*!40000 ALTER TABLE `signup_codes_signupcoderesult` DISABLE KEYS */;
/*!40000 ALTER TABLE `signup_codes_signupcoderesult` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_association`
--

DROP TABLE IF EXISTS `social_auth_association`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_association` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) NOT NULL,
  `handle` varchar(255) NOT NULL,
  `secret` varchar(255) NOT NULL,
  `issued` int(11) NOT NULL,
  `lifetime` int(11) NOT NULL,
  `assoc_type` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `server_url` (`server_url`,`handle`),
  KEY `social_auth_association_5a32b972` (`issued`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_association`
--

LOCK TABLES `social_auth_association` WRITE;
/*!40000 ALTER TABLE `social_auth_association` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_association` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_nonce`
--

DROP TABLE IF EXISTS `social_auth_nonce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_nonce` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) NOT NULL,
  `timestamp` int(11) NOT NULL,
  `salt` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `server_url` (`server_url`,`timestamp`,`salt`),
  KEY `social_auth_nonce_67f1b7ce` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_nonce`
--

LOCK TABLES `social_auth_nonce` WRITE;
/*!40000 ALTER TABLE `social_auth_nonce` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_nonce` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_usersocialauth`
--

DROP TABLE IF EXISTS `social_auth_usersocialauth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_usersocialauth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `provider` varchar(32) NOT NULL,
  `uid` varchar(255) NOT NULL,
  `extra_data` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `provider` (`provider`,`uid`),
  KEY `social_auth_usersocialauth_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_60fa311b` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_usersocialauth`
--

LOCK TABLES `social_auth_usersocialauth` WRITE;
/*!40000 ALTER TABLE `social_auth_usersocialauth` DISABLE KEYS */;
INSERT INTO `social_auth_usersocialauth` VALUES (2,17,'twitter','55353','{}'),(3,17,'facebook','342424','{}'),(4,16,'twitter','gdgdgdgdg','{}'),(5,24,'facebook','100001920326669','{\"access_token\": \"CAAB1mPIXcrsBACHQxITOK1XdrjVv07DiQCM5kXMCb8BQ74ZAE3O96HsGRN4rCPfbeWmSUcUqsIGFlSLevgGFCOGvEGPsDJ5Gcquj4TwtVRHRZApcK7nKbQXhpXP7TigSKDB9EseufIVhjv26n7RgTwcvlZBhSTsbCR6qI0P3etZBgDUjC8iwlBEZAH2YUfnUZD\", \"expires\": \"5183999\", \"id\": \"100001920326669\"}'),(6,25,'facebook','100000890760954','{\"access_token\": \"CAAB1mPIXcrsBAMACnRqBC5oumQDlfSGHdmLZAnVZC4aOlLTZCiCCky4oGkLz69nWDIoETATTHbFhx6nDB0AlmftLqAHsyRJzsxodqJgD5DO1anTKMcm48Cle8pxk5sxYdoO8FS6GHNxglTpuZADAqwBfnyaXbd2z8uyGs2CmyjenDd4zkIMhrsKIFBdenB8ZD\", \"expires\": \"5184000\", \"id\": \"100000890760954\"}'),(7,26,'google-oauth2','artiom.davydov@gmail.com','{\"token_type\": \"Bearer\", \"access_token\": \"ya29.IwDSP4QL7Be9FSAAAAAiu6Nol_oONjybXfIWtqi7Gh_tFtcaUX2ksY8Uw9ONoQ\", \"expires\": 3599}'),(8,27,'google-oauth2','nicoexhibia@gmail.com','{\"access_token\": \"ya29.IwAzI8_zfP6PoxwAAACL7LlADv8fJNj2N2RoIpOVCjVwR-z9wYKQwmt3OWJzdA\", \"token_type\": \"Bearer\", \"expires\": 3599}'),(9,16,'google-oauth2','anthony.poddubny@gmail.com','{\"token_type\": \"Bearer\", \"access_token\": \"ya29.JADdrwDwvUnkxxsAAAAOVMNOr5JctFsrQQRXM3ETgpdDcy2Rf_-6AYCgNq_Rng\", \"expires\": 3599}'),(11,28,'facebook','100006409656118','{\"access_token\": \"CAAB1mPIXcrsBAIAZBwfYDGZAO1Iz41WGHvnt6UhAZBnoUst3DsFQRI1PuaeZARE1zF9jLaR3sGvbmbBsCV9MRwZBLSlugOaX8sOBoZAsMuyJ03wW3qiTm0Y27X1XNd9GXMzqDZABifu9WJ68J2u6LabLqHZBtNagm8wQX8UoNitZC0qgfqLKOhMRo\", \"expires\": \"5170554\", \"id\": \"100006409656118\"}');
/*!40000 ALTER TABLE `social_auth_usersocialauth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socials_invitation`
--

DROP TABLE IF EXISTS `socials_invitation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socials_invitation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `external_id` varchar(250) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `socials_invitation_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_c16ab958` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socials_invitation`
--

LOCK TABLES `socials_invitation` WRITE;
/*!40000 ALTER TABLE `socials_invitation` DISABLE KEYS */;
/*!40000 ALTER TABLE `socials_invitation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socials_likeitem`
--

DROP TABLE IF EXISTS `socials_likeitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socials_likeitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_id` varchar(15) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `type` varchar(1) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `socials_likeitem_67b70d25` (`item_id`),
  KEY `socials_likeitem_fbfc09f1` (`user_id`),
  CONSTRAINT `item_id_refs_code_637345bd` FOREIGN KEY (`item_id`) REFERENCES `auctions_auctionitem` (`code`),
  CONSTRAINT `user_id_refs_id_4782a489` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socials_likeitem`
--

LOCK TABLES `socials_likeitem` WRITE;
/*!40000 ALTER TABLE `socials_likeitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `socials_likeitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `south_migrationhistory`
--

DROP TABLE IF EXISTS `south_migrationhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `south_migrationhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(255) NOT NULL,
  `migration` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `south_migrationhistory`
--

LOCK TABLES `south_migrationhistory` WRITE;
/*!40000 ALTER TABLE `south_migrationhistory` DISABLE KEYS */;
INSERT INTO `south_migrationhistory` VALUES (1,'easy_thumbnails','0001_initial','2014-05-12 15:51:16'),(2,'easy_thumbnails','0002_filename_indexes','2014-05-12 15:51:17'),(3,'easy_thumbnails','0003_auto__add_storagenew','2014-05-12 15:51:17'),(4,'easy_thumbnails','0004_auto__add_field_source_storage_new__add_field_thumbnail_storage_new','2014-05-12 15:51:19'),(5,'easy_thumbnails','0005_storage_fks_null','2014-05-12 15:51:21'),(6,'easy_thumbnails','0006_copy_storage','2014-05-12 15:51:21'),(7,'easy_thumbnails','0007_storagenew_fks_not_null','2014-05-12 15:51:22'),(8,'easy_thumbnails','0008_auto__del_field_source_storage__del_field_thumbnail_storage','2014-05-12 15:51:23'),(9,'easy_thumbnails','0009_auto__del_storage','2014-05-12 15:51:23'),(10,'easy_thumbnails','0010_rename_storage','2014-05-12 15:51:26'),(11,'easy_thumbnails','0011_auto__add_field_source_storage_hash__add_field_thumbnail_storage_hash','2014-05-12 15:51:27'),(12,'easy_thumbnails','0012_build_storage_hashes','2014-05-12 15:51:27'),(13,'easy_thumbnails','0013_auto__del_storage__del_field_source_storage__del_field_thumbnail_stora','2014-05-12 15:51:29'),(14,'easy_thumbnails','0014_auto__add_unique_source_name_storage_hash__add_unique_thumbnail_name_s','2014-05-12 15:51:29'),(15,'easy_thumbnails','0015_auto__del_unique_thumbnail_name_storage_hash__add_unique_thumbnail_sou','2014-05-12 15:51:29'),(16,'redisboard','0001_initial','2014-05-13 10:27:51'),(17,'redisboard','0002_auto__add_unique_redisserver_hostname_port','2014-05-13 10:27:51'),(18,'redisboard','0003_auto__chg_field_redisserver_port','2014-05-13 10:27:51'),(19,'redisboard','0004_auto__add_field_redisserver_sampling_threshold__add_field_redisserver_','2014-05-13 10:27:52'),(20,'redisboard','0005_auto__add_field_redisserver_label','2014-05-13 10:27:52'),(21,'redisboard','0006_auto__chg_field_redisserver_label','2014-05-13 10:27:53'),(22,'auctions','0001_ffh','2014-05-14 12:35:52'),(23,'auctions','0002_auto__del_field_auctionitem_lock_after','2014-05-14 12:36:30'),(24,'auctions','0003_auto__add_field_auctionitem_lock_after','2014-05-14 12:37:01'),(25,'auctions','0004_auto__add_field_auctionitem_locked','2014-05-14 12:58:14'),(26,'auctions','0005_auto__del_field_auctionitem_locked__add_field_auction_locked','2014-05-14 13:34:55'),(27,'auctions','0006_auto__add_field_auctionitem_newbie','2014-05-14 14:27:11');
/*!40000 ALTER TABLE `south_migrationhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `testimonials_video`
--

DROP TABLE IF EXISTS `testimonials_video`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `testimonials_video` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `member_id` int(11) NOT NULL,
  `auction_id` int(11) NOT NULL,
  `title` varchar(500) DEFAULT NULL,
  `review` longtext,
  `rated` smallint(6) NOT NULL,
  `file` varchar(100) NOT NULL,
  `youtube_url` varchar(200) NOT NULL,
  `facebook_video_id` varchar(500) DEFAULT NULL,
  `facebook_video_info` longtext,
  `facebook_page_video_id` varchar(500) DEFAULT NULL,
  `facebook_page_video_info` longtext,
  `share_on_facebook` tinyint(1) NOT NULL,
  `share_on_twitter` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auction_id` (`auction_id`),
  UNIQUE KEY `member_id` (`member_id`,`auction_id`),
  KEY `testimonials_video_56e38b98` (`member_id`),
  CONSTRAINT `auction_id_refs_id_d8e10a1d` FOREIGN KEY (`auction_id`) REFERENCES `auctions_auction` (`id`),
  CONSTRAINT `member_id_refs_id_fb38712f` FOREIGN KEY (`member_id`) REFERENCES `profiles_member` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `testimonials_video`
--

LOCK TABLES `testimonials_video` WRITE;
/*!40000 ALTER TABLE `testimonials_video` DISABLE KEYS */;
/*!40000 ALTER TABLE `testimonials_video` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-05-28  7:50:16
