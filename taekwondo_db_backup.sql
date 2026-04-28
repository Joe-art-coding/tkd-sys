-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: taekwondo_db
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `attendance_attendance`
--

DROP TABLE IF EXISTS `attendance_attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_attendance` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `check_in_time` time(6) DEFAULT NULL,
  `class_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `instructor` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_present` tinyint(1) NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `attendance_attendance_student_id_date_167892e4_uniq` (`student_id`,`date`),
  CONSTRAINT `attendance_attendance_student_id_94863613_fk_students_student_id` FOREIGN KEY (`student_id`) REFERENCES `students_student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_attendance`
--

LOCK TABLES `attendance_attendance` WRITE;
/*!40000 ALTER TABLE `attendance_attendance` DISABLE KEYS */;
/*!40000 ALTER TABLE `attendance_attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (3,'Assistant Coach'),(1,'Club Admin'),(2,'Coach');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (9,1,13),(10,1,14),(11,1,15),(12,1,16),(1,1,41),(2,1,42),(3,1,43),(4,1,44),(5,1,49),(6,1,50),(7,1,51),(8,1,52),(13,2,44),(15,3,40),(17,3,60),(14,3,64),(16,3,68);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add Token',7,'add_token'),(26,'Can change Token',7,'change_token'),(27,'Can delete Token',7,'delete_token'),(28,'Can view Token',7,'view_token'),(29,'Can add Token',8,'add_tokenproxy'),(30,'Can change Token',8,'change_tokenproxy'),(31,'Can delete Token',8,'delete_tokenproxy'),(32,'Can view Token',8,'view_tokenproxy'),(33,'Can add club',10,'add_club'),(34,'Can change club',10,'change_club'),(35,'Can delete club',10,'delete_club'),(36,'Can view club',10,'view_club'),(37,'Can add contact info',11,'add_contactinfo'),(38,'Can change contact info',11,'change_contactinfo'),(39,'Can delete contact info',11,'delete_contactinfo'),(40,'Can view contact info',11,'view_contactinfo'),(41,'Can add school',12,'add_school'),(42,'Can change school',12,'change_school'),(43,'Can delete school',12,'delete_school'),(44,'Can view school',12,'view_school'),(45,'Can add class schedule',9,'add_classschedule'),(46,'Can change class schedule',9,'change_classschedule'),(47,'Can delete class schedule',9,'delete_classschedule'),(48,'Can view class schedule',9,'view_classschedule'),(49,'Can add user profile',13,'add_userprofile'),(50,'Can change user profile',13,'change_userprofile'),(51,'Can delete user profile',13,'delete_userprofile'),(52,'Can view user profile',13,'view_userprofile'),(53,'Can add student',14,'add_student'),(54,'Can change student',14,'change_student'),(55,'Can delete student',14,'delete_student'),(56,'Can view student',14,'view_student'),(57,'Can add parent',17,'add_parent'),(58,'Can change parent',17,'change_parent'),(59,'Can delete parent',17,'delete_parent'),(60,'Can view parent',17,'view_parent'),(61,'Can add fee',15,'add_fee'),(62,'Can change fee',15,'change_fee'),(63,'Can delete fee',15,'delete_fee'),(64,'Can view fee',15,'view_fee'),(65,'Can add attendance',16,'add_attendance'),(66,'Can change attendance',16,'change_attendance'),(67,'Can delete attendance',16,'delete_attendance'),(68,'Can view attendance',16,'view_attendance');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1200000$rete8JGG7mU7uaubdbUcqi$g6Gtm93Hy22IRn4u5ZNzL7UXCdBhw0kbJFpQnwly+OY=','2026-04-09 07:07:47.418489',1,'joe','','','amyrul@msn.com',1,1,'2026-04-07 13:16:14.089087'),(2,'pbkdf2_sha256$1200000$QAcOgkWDcnSyCap1TcMzqx$Vc6Nvggic2hqFzvCu7Xxh1r+8jId+R38gwaftKVQhM4=','2026-04-08 12:12:04.208822',0,'amirul','Amirul','Abdullah','amyrul@msn.com',1,1,'2026-04-07 13:20:02.180186'),(3,'pbkdf2_sha256$1200000$AsAoFqRadZETmuEzUqXRLv$YOZ/qoqwMU+1GPdu1QGF0OFPsqw/P6eE5vOA6X8X15U=','2026-04-08 12:13:36.655971',0,'azizah','Azizah','Ismail','azizah@msn.com',1,1,'2026-04-07 13:21:04.474762'),(4,'pbkdf2_sha256$1200000$LvftXjwaC5uEbZEOvYqWYz$MrsF2Up0GmewwydkAXAtJ0+CuJTrgs190I1A7q9ffus=','2026-04-09 06:41:09.059587',0,'ayie','ayie','simonm','ayie@msn.com',1,1,'2026-04-07 13:30:01.000000'),(5,'pbkdf2_sha256$1200000$fXiDUmf3QJ2aFXkR8tBSGE$WxERqhJ+ON1k6Go7YRkh+pCnV80tuqx+wcoZ6gGVWEY=',NULL,0,'raintown_admin','RainTown','Admin','admin@raintown.com',1,1,'2026-04-07 13:54:48.854679'),(6,'pbkdf2_sha256$1200000$tdP3ZK2hDGMU4vjYMIUuJL$UOEJPhOjoEti4UfCokw/AlG7XLPYDffWlkkYLReL6dE=',NULL,0,'coach_rt_ali','Ali','Bin Ahmad','coach_rt_ali@raintown.com',1,1,'2026-04-07 13:54:49.008913'),(7,'pbkdf2_sha256$1200000$RalUrrLdJPUVmEb7eZ5BC0$/8Q0L4hl/QB3SsFKHc3xiwCyQ2NY+Txd1tXnRlexT1c=',NULL,0,'coach_rt_siti','Siti','Bt Abdullah','coach_rt_siti@raintown.com',1,1,'2026-04-07 13:54:50.718245'),(8,'pbkdf2_sha256$1200000$Jq4pyFly64ii7mwqlxv5eU$4QwD2V+UEKMp4xialwElBQ+H0ma7uvoeQERQRX57zVo=',NULL,0,'coach_rt_ahmad','Ahmad','Bin Hassan','coach_rt_ahmad@raintown.com',1,1,'2026-04-07 13:54:52.389326'),(9,'pbkdf2_sha256$1200000$6qsNkeUZfKAgBErBE835u8$KVhct2h3cqYkBacqiaA7MRuBczSewIi4IQF2+sI2r6o=',NULL,0,'parent_rtc_800101141234','','','parent_rtc_800101141234@example.com',0,1,'2026-04-07 13:54:54.164790'),(10,'pbkdf2_sha256$1200000$HdhvmmIm9XBvntWfZ6Gqqc$NsWy8EOusu08aUPmTJCCVgYVbUv9CvJY9XhWi3d5aeU=',NULL,0,'parent_rtc_800202145678','','','parent_rtc_800202145678@example.com',0,1,'2026-04-07 13:54:55.806772'),(11,'pbkdf2_sha256$1200000$h1LiyH3zf3qeDqQsO41KK4$K16ZWwASA8RtxPizvBpEsuSRhOSfMzpsVmByEtBXmhA=',NULL,0,'parent_rtc_800303149012','','','parent_rtc_800303149012@example.com',0,1,'2026-04-07 13:54:57.479144'),(12,'pbkdf2_sha256$1200000$9RjbN4kGnL6JsVKk6kYBtL$OpC/LnUp4lxbAj+OGU7UUttmu1xgiIg/07ijBBFP4lQ=',NULL,0,'parent_rtc_810404143456','','','parent_rtc_810404143456@example.com',0,1,'2026-04-07 13:54:59.173432'),(13,'pbkdf2_sha256$1200000$gt3eYH24TlgokwiOUCVnAa$YsBEMUGnSpBKeklY64Ih4hAJOP6lfEmNwTGxSvWe6s0=',NULL,0,'parent_rtc_810505147890','','','parent_rtc_810505147890@example.com',0,1,'2026-04-07 13:55:00.821434'),(14,'pbkdf2_sha256$1200000$81TyTFkXjKNZvrGN8B8vgM$w348tCUj2SmYnaVv76ip74REffIG3nbw1+MCAIrABv8=',NULL,0,'parent_rtc_820606141234','','','parent_rtc_820606141234@example.com',0,1,'2026-04-07 13:55:02.503535'),(15,'pbkdf2_sha256$1200000$luewhJZ57ymQkF5i4V9qk1$C9w07TE5te1ijArIqMU7Gi2Jc4Xj1/YRFm0NTVFi0jY=',NULL,0,'parent_800101141234','','','parent_800101141234@example.com',0,1,'2026-04-07 13:55:04.178262'),(16,'pbkdf2_sha256$1200000$zeHKS1MO1nHRI00hqBmx9e$RC/CR42Q+fOUCYIApxOQNI3OYYrYuFbSdFpquYYhK5k=',NULL,0,'parent_800202145678','','','parent_800202145678@example.com',0,1,'2026-04-07 13:55:05.855074'),(17,'pbkdf2_sha256$1200000$ehx6Mmkm1svvG4xGWOewgA$2VYx7gcT09mAx7xkh4Xnm/rPBfjS0/5XbWPKP6bbcFc=',NULL,0,'parent_800303149012','','','parent_800303149012@example.com',0,1,'2026-04-07 13:55:07.529101'),(18,'pbkdf2_sha256$1200000$dl69FketXNQBXMgkcZcQ5I$VG2/O1U4YfKG0YoNUW+GaPuAAMf6sqDrT3aldD4YEIU=',NULL,0,'parent_810404143456','','','parent_810404143456@example.com',0,1,'2026-04-07 13:55:09.156587'),(19,'pbkdf2_sha256$1200000$QOIXCWeJ08VWOZ1iEbNp8U$eqXQlrXX8AAFMwP4/AnUp+1xgsDdbNDy3mfDpsRQeQQ=',NULL,0,'parent_810505147890','','','parent_810505147890@example.com',0,1,'2026-04-07 13:55:10.833768'),(20,'pbkdf2_sha256$1200000$JEup0IFpIHDv4Bv1oDKEqK$Ks25veOoXmX+FSshMgHNCtmjlW0tTRqiKWeDaz+AzdY=',NULL,0,'parent_820606141234','','','parent_820606141234@example.com',0,1,'2026-04-07 13:55:12.487824'),(21,'pbkdf2_sha256$1200000$FTIlXGNsVfWeWKZhyDqFMR$+Y3Mlcg57Hs2ItZwokTSpl0ZgTq3jcS6bk6PJSfevcw=',NULL,0,'parent_ttc_730728085911','','','parent_ttc_730728085911@example.com',0,1,'2026-04-07 14:42:24.537598'),(22,'pbkdf2_sha256$...',NULL,0,'parent_test','','','',0,1,'2026-04-08 04:03:51.669117');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (1,2,1),(2,3,1),(3,4,2),(4,5,1),(5,6,2),(6,7,2),(7,8,2);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
INSERT INTO `auth_user_user_permissions` VALUES (3,4,53),(4,4,54),(1,4,57),(2,4,58),(6,4,61),(7,4,62),(8,4,63),(5,4,64);
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
INSERT INTO `authtoken_token` VALUES ('0062f4732b7db9a2e1bdbd218f4ebf522e340a55','2026-04-07 14:31:48.779068',14),('74403de687f3f12869358e80c3b2e68a5e186467','2026-04-07 14:31:19.480503',12),('d13ded8468923d7edd2c59a041110810da58b042','2026-04-07 14:15:04.541485',9),('d923b3e8e3f94abaadd2597780f6a09587cb48b7','2026-04-07 14:50:08.026104',21);
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-04-07 13:17:54.570114','1','Taiping Taekwondo Club (ttc)',1,'[{\"added\": {}}]',10,1),(2,'2026-04-07 13:19:00.217440','2','Raintown TaeKwonDo Club (rtc)',1,'[{\"added\": {}}]',10,1),(3,'2026-04-07 13:20:04.074504','2','amirul',1,'[{\"added\": {}}, {\"added\": {\"name\": \"user profile\", \"object\": \"amirul - club_admin (Taiping Taekwondo Club)\"}}]',4,1),(4,'2026-04-07 13:21:06.293719','3','azizah',1,'[{\"added\": {}}, {\"added\": {\"name\": \"user profile\", \"object\": \"azizah - club_admin (Raintown TaeKwonDo Club)\"}}]',4,1),(5,'2026-04-07 13:22:08.057893','1','Taiping Taekwondo Club - SK KAMPUNG BOYAN',1,'[{\"added\": {}}]',12,1),(6,'2026-04-07 13:22:49.449279','2','Taiping Taekwondo Club - SK SERI AMAN',1,'[{\"added\": {}}]',12,1),(7,'2026-04-07 13:23:25.770754','3','Taiping Taekwondo Club - SK AYER PUTEH',1,'[{\"added\": {}}]',12,1),(8,'2026-04-07 13:23:55.615826','4','Taiping Taekwondo Club - SK SELAMA',1,'[{\"added\": {}}]',12,1),(9,'2026-04-07 13:24:33.565054','5','Taiping Taekwondo Club - PRIMA BAGAN SERAI',1,'[{\"added\": {}}]',12,1),(10,'2026-04-07 13:25:20.935446','6','Raintown TaeKwonDo Club - SK TAMAN TASIK',1,'[{\"added\": {}}]',12,1),(11,'2026-04-07 13:26:00.072184','7','Raintown TaeKwonDo Club - SERATAS',1,'[{\"added\": {}}]',12,1),(12,'2026-04-07 13:26:32.660786','8','Raintown TaeKwonDo Club - SK AULONG',1,'[{\"added\": {}}]',12,1),(13,'2026-04-07 13:30:03.249138','4','ayie',1,'[{\"added\": {}}, {\"added\": {\"name\": \"user profile\", \"object\": \"ayie - coach (Taiping Taekwondo Club)\"}}]',4,1),(14,'2026-04-07 13:31:28.366476','3','Assistant Coach',1,'[{\"added\": {}}]',2,1),(15,'2026-04-07 13:46:18.911985','4','ayie',2,'[]',4,1),(16,'2026-04-07 13:46:30.148696','4','ayie',2,'[{\"changed\": {\"fields\": [\"Last name\"]}}]',4,1),(17,'2026-04-07 14:40:19.448594','4','ayie',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(18,'2026-04-07 14:42:26.408347','7','Haziq - Taiping Taekwondo Club - SK KAMPUNG BOYAN - TTC2026001',1,'[{\"added\": {}}]',14,4),(19,'2026-04-07 14:47:11.321527','8','MIA - Taiping Taekwondo Club - SK KAMPUNG BOYAN - TTC2026002',1,'[{\"added\": {}}]',14,4),(20,'2026-04-07 14:51:00.163586','4','ayie',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(21,'2026-04-09 04:50:30.750716','97','Haziq - tshirt - RM45',1,'[{\"added\": {}}]',15,1),(22,'2026-04-09 05:05:06.382547','97','Haziq - tshirt - RM45.00',2,'[{\"changed\": {\"fields\": [\"Paid date\", \"Status\", \"Receipt number\"]}}]',15,1),(23,'2026-04-09 06:19:18.063635','3','TaeKwonDo SYSTEM (taekwondo-system)',1,'[{\"added\": {}}]',10,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(16,'attendance','attendance'),(2,'auth','group'),(3,'auth','permission'),(4,'auth','user'),(7,'authtoken','token'),(8,'authtoken','tokenproxy'),(5,'contenttypes','contenttype'),(15,'fees','fee'),(9,'schools','classschedule'),(10,'schools','club'),(11,'schools','contactinfo'),(12,'schools','school'),(13,'schools','userprofile'),(6,'sessions','session'),(17,'students','parent'),(14,'students','student');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-04-07 13:15:08.296109'),(2,'auth','0001_initial','2026-04-07 13:15:10.998743'),(3,'admin','0001_initial','2026-04-07 13:15:12.695645'),(4,'admin','0002_logentry_remove_auto_add','2026-04-07 13:15:12.773195'),(5,'admin','0003_logentry_add_action_flag_choices','2026-04-07 13:15:12.901081'),(6,'schools','0001_initial','2026-04-07 13:15:26.930703'),(7,'students','0001_initial','2026-04-07 13:15:35.337110'),(8,'attendance','0001_initial','2026-04-07 13:15:37.257184'),(9,'contenttypes','0002_remove_content_type_name','2026-04-07 13:15:39.579593'),(10,'auth','0002_alter_permission_name_max_length','2026-04-07 13:15:41.230834'),(11,'auth','0003_alter_user_email_max_length','2026-04-07 13:15:41.348395'),(12,'auth','0004_alter_user_username_opts','2026-04-07 13:15:41.401504'),(13,'auth','0005_alter_user_last_login_null','2026-04-07 13:15:41.708348'),(14,'auth','0006_require_contenttypes_0002','2026-04-07 13:15:41.730148'),(15,'auth','0007_alter_validators_add_error_messages','2026-04-07 13:15:41.760103'),(16,'auth','0008_alter_user_username_max_length','2026-04-07 13:15:42.198431'),(17,'auth','0009_alter_user_last_name_max_length','2026-04-07 13:15:42.858697'),(18,'auth','0010_alter_group_name_max_length','2026-04-07 13:15:42.988223'),(19,'auth','0011_update_proxy_permissions','2026-04-07 13:15:43.036336'),(20,'auth','0012_alter_user_first_name_max_length','2026-04-07 13:15:43.558320'),(21,'authtoken','0001_initial','2026-04-07 13:15:44.196495'),(22,'authtoken','0002_auto_20160226_1747','2026-04-07 13:15:44.290762'),(23,'authtoken','0003_tokenproxy','2026-04-07 13:15:44.315896'),(24,'authtoken','0004_alter_tokenproxy_options','2026-04-07 13:15:44.355377'),(25,'fees','0001_initial','2026-04-07 13:15:44.929323'),(26,'sessions','0001_initial','2026-04-07 13:15:45.227589'),(27,'fees','0002_alter_fee_receipt_number','2026-04-08 04:23:24.605806'),(28,'fees','0003_alter_fee_receipt_number','2026-04-08 04:25:08.033105');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fees_fee`
--

DROP TABLE IF EXISTS `fees_fee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fees_fee` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fee_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `month` date DEFAULT NULL,
  `due_date` date NOT NULL,
  `paid_date` date DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `receipt_number` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fees_fee_student_id_664ca066_fk_students_student_id` (`student_id`),
  CONSTRAINT `fees_fee_student_id_664ca066_fk_students_student_id` FOREIGN KEY (`student_id`) REFERENCES `students_student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fees_fee`
--

LOCK TABLES `fees_fee` WRITE;
/*!40000 ALTER TABLE `fees_fee` DISABLE KEYS */;
INSERT INTO `fees_fee` VALUES (1,'monthly',120.00,'2026-01-01','2026-02-01',NULL,'overdue',NULL,'','2026-04-07 13:54:55.771254','2026-04-07 13:54:55.771274',1),(2,'monthly',120.00,'2026-02-01','2026-03-01',NULL,'overdue',NULL,'','2026-04-07 13:54:55.772885','2026-04-07 13:54:55.772906',1),(3,'monthly',120.00,'2026-03-01','2026-04-01',NULL,'overdue',NULL,'','2026-04-07 13:54:55.774130','2026-04-07 13:54:55.774152',1),(4,'monthly',120.00,'2026-04-01','2026-05-01','2026-04-08','paid','REC-000004','','2026-04-07 13:54:55.775329','2026-04-08 04:27:53.161419',1),(5,'monthly',120.00,'2026-05-01','2026-06-01',NULL,'pending',NULL,'','2026-04-07 13:54:55.776491','2026-04-07 13:54:55.776512',1),(6,'monthly',120.00,'2026-06-01','2026-07-01',NULL,'pending',NULL,'','2026-04-07 13:54:55.777665','2026-04-07 13:54:55.777687',1),(7,'monthly',120.00,'2026-07-01','2026-08-01',NULL,'pending',NULL,'','2026-04-07 13:54:55.779239','2026-04-07 13:54:55.779276',1),(8,'monthly',120.00,'2026-08-01','2026-09-01',NULL,'pending',NULL,'','2026-04-07 13:54:55.780721','2026-04-07 13:54:55.780748',1),(9,'monthly',120.00,'2026-09-01','2026-10-01',NULL,'pending',NULL,'','2026-04-07 13:54:55.781962','2026-04-07 13:54:55.781983',1),(10,'monthly',120.00,'2026-10-01','2026-11-01',NULL,'pending',NULL,'','2026-04-07 13:54:55.783144','2026-04-07 13:54:55.783166',1),(11,'monthly',120.00,'2026-11-01','2026-12-01',NULL,'pending',NULL,'','2026-04-07 13:54:55.784556','2026-04-07 13:54:55.784576',1),(12,'monthly',120.00,'2026-12-01','2027-01-01',NULL,'pending',NULL,'','2026-04-07 13:54:55.785791','2026-04-07 13:54:55.785812',1),(13,'monthly',120.00,'2026-01-01','2026-02-01',NULL,'overdue',NULL,'','2026-04-07 13:54:57.443433','2026-04-07 13:54:57.443459',2),(14,'monthly',120.00,'2026-02-01','2026-03-01',NULL,'overdue',NULL,'','2026-04-07 13:54:57.444772','2026-04-07 13:54:57.444794',2),(15,'monthly',120.00,'2026-03-01','2026-04-01',NULL,'overdue',NULL,'','2026-04-07 13:54:57.446132','2026-04-07 13:54:57.446154',2),(16,'monthly',120.00,'2026-04-01','2026-05-01',NULL,'pending',NULL,'','2026-04-07 13:54:57.447317','2026-04-07 13:54:57.447338',2),(17,'monthly',120.00,'2026-05-01','2026-06-01',NULL,'pending',NULL,'','2026-04-07 13:54:57.448538','2026-04-07 13:54:57.448558',2),(18,'monthly',120.00,'2026-06-01','2026-07-01',NULL,'pending',NULL,'','2026-04-07 13:54:57.449716','2026-04-07 13:54:57.449763',2),(19,'monthly',120.00,'2026-07-01','2026-08-01',NULL,'pending',NULL,'','2026-04-07 13:54:57.451338','2026-04-07 13:54:57.451360',2),(20,'monthly',120.00,'2026-08-01','2026-09-01',NULL,'pending',NULL,'','2026-04-07 13:54:57.452596','2026-04-07 13:54:57.452618',2),(21,'monthly',120.00,'2026-09-01','2026-10-01',NULL,'pending',NULL,'','2026-04-07 13:54:57.453799','2026-04-07 13:54:57.453819',2),(22,'monthly',120.00,'2026-10-01','2026-11-01',NULL,'pending',NULL,'','2026-04-07 13:54:57.454964','2026-04-07 13:54:57.454984',2),(23,'monthly',120.00,'2026-11-01','2026-12-01',NULL,'pending',NULL,'','2026-04-07 13:54:57.456552','2026-04-07 13:54:57.456576',2),(24,'monthly',120.00,'2026-12-01','2027-01-01',NULL,'pending',NULL,'','2026-04-07 13:54:57.457851','2026-04-07 13:54:57.457872',2),(25,'monthly',120.00,'2026-01-01','2026-02-01',NULL,'overdue',NULL,'','2026-04-07 13:54:59.138471','2026-04-07 13:54:59.138494',3),(26,'monthly',120.00,'2026-02-01','2026-03-01',NULL,'overdue',NULL,'','2026-04-07 13:54:59.139657','2026-04-07 13:54:59.139679',3),(27,'monthly',120.00,'2026-03-01','2026-04-01',NULL,'overdue',NULL,'','2026-04-07 13:54:59.140843','2026-04-07 13:54:59.140865',3),(28,'monthly',120.00,'2026-04-01','2026-05-01',NULL,'pending',NULL,'','2026-04-07 13:54:59.142057','2026-04-07 13:54:59.142101',3),(29,'monthly',120.00,'2026-05-01','2026-06-01',NULL,'pending',NULL,'','2026-04-07 13:54:59.143833','2026-04-07 13:54:59.143875',3),(30,'monthly',120.00,'2026-06-01','2026-07-01',NULL,'pending',NULL,'','2026-04-07 13:54:59.145302','2026-04-07 13:54:59.145330',3),(31,'monthly',120.00,'2026-07-01','2026-08-01',NULL,'pending',NULL,'','2026-04-07 13:54:59.146793','2026-04-07 13:54:59.146814',3),(32,'monthly',120.00,'2026-08-01','2026-09-01',NULL,'pending',NULL,'','2026-04-07 13:54:59.148049','2026-04-07 13:54:59.148072',3),(33,'monthly',120.00,'2026-09-01','2026-10-01',NULL,'pending',NULL,'','2026-04-07 13:54:59.149236','2026-04-07 13:54:59.149257',3),(34,'monthly',120.00,'2026-10-01','2026-11-01',NULL,'pending',NULL,'','2026-04-07 13:54:59.150480','2026-04-07 13:54:59.150502',3),(35,'monthly',120.00,'2026-11-01','2026-12-01',NULL,'pending',NULL,'','2026-04-07 13:54:59.152097','2026-04-07 13:54:59.152118',3),(36,'monthly',120.00,'2026-12-01','2027-01-01',NULL,'pending',NULL,'','2026-04-07 13:54:59.153348','2026-04-07 13:54:59.153368',3),(37,'monthly',130.00,'2026-01-01','2026-02-01',NULL,'overdue',NULL,'','2026-04-07 13:55:00.786469','2026-04-07 13:55:00.786491',4),(38,'monthly',130.00,'2026-02-01','2026-03-01',NULL,'overdue',NULL,'','2026-04-07 13:55:00.787614','2026-04-07 13:55:00.787636',4),(39,'monthly',130.00,'2026-03-01','2026-04-01',NULL,'overdue',NULL,'','2026-04-07 13:55:00.788791','2026-04-07 13:55:00.788812',4),(40,'monthly',130.00,'2026-04-01','2026-05-01',NULL,'pending',NULL,'','2026-04-07 13:55:00.789996','2026-04-07 13:55:00.790017',4),(41,'monthly',130.00,'2026-05-01','2026-06-01',NULL,'pending',NULL,'','2026-04-07 13:55:00.791180','2026-04-07 13:55:00.791202',4),(42,'monthly',130.00,'2026-06-01','2026-07-01',NULL,'pending',NULL,'','2026-04-07 13:55:00.792385','2026-04-07 13:55:00.792407',4),(43,'monthly',130.00,'2026-07-01','2026-08-01',NULL,'pending',NULL,'','2026-04-07 13:55:00.793557','2026-04-07 13:55:00.793579',4),(44,'monthly',130.00,'2026-08-01','2026-09-01',NULL,'pending',NULL,'','2026-04-07 13:55:00.794735','2026-04-07 13:55:00.794756',4),(45,'monthly',130.00,'2026-09-01','2026-10-01',NULL,'pending',NULL,'','2026-04-07 13:55:00.795903','2026-04-07 13:55:00.795925',4),(46,'monthly',130.00,'2026-10-01','2026-11-01',NULL,'pending',NULL,'','2026-04-07 13:55:00.797059','2026-04-07 13:55:00.797082',4),(47,'monthly',130.00,'2026-11-01','2026-12-01',NULL,'pending',NULL,'','2026-04-07 13:55:00.798266','2026-04-07 13:55:00.798287',4),(48,'monthly',130.00,'2026-12-01','2027-01-01',NULL,'pending',NULL,'','2026-04-07 13:55:00.799449','2026-04-07 13:55:00.799471',4),(49,'monthly',130.00,'2026-01-01','2026-02-01',NULL,'overdue',NULL,'','2026-04-07 13:55:02.466641','2026-04-07 13:55:02.466662',5),(50,'monthly',130.00,'2026-02-01','2026-03-01',NULL,'overdue',NULL,'','2026-04-07 13:55:02.468399','2026-04-07 13:55:02.468434',5),(51,'monthly',130.00,'2026-03-01','2026-04-01',NULL,'overdue',NULL,'','2026-04-07 13:55:02.469775','2026-04-07 13:55:02.469818',5),(52,'monthly',130.00,'2026-04-01','2026-05-01',NULL,'pending',NULL,'','2026-04-07 13:55:02.470933','2026-04-07 13:55:02.470952',5),(53,'monthly',130.00,'2026-05-01','2026-06-01',NULL,'pending',NULL,'','2026-04-07 13:55:02.472071','2026-04-07 13:55:02.472092',5),(54,'monthly',130.00,'2026-06-01','2026-07-01',NULL,'pending',NULL,'','2026-04-07 13:55:02.473182','2026-04-07 13:55:02.473202',5),(55,'monthly',130.00,'2026-07-01','2026-08-01',NULL,'pending',NULL,'','2026-04-07 13:55:02.474248','2026-04-07 13:55:02.474268',5),(56,'monthly',130.00,'2026-08-01','2026-09-01',NULL,'pending',NULL,'','2026-04-07 13:55:02.475366','2026-04-07 13:55:02.475388',5),(57,'monthly',130.00,'2026-09-01','2026-10-01',NULL,'pending',NULL,'','2026-04-07 13:55:02.476459','2026-04-07 13:55:02.476480',5),(58,'monthly',130.00,'2026-10-01','2026-11-01',NULL,'pending',NULL,'','2026-04-07 13:55:02.477531','2026-04-07 13:55:02.477553',5),(59,'monthly',130.00,'2026-11-01','2026-12-01',NULL,'pending',NULL,'','2026-04-07 13:55:02.478691','2026-04-07 13:55:02.478711',5),(60,'monthly',130.00,'2026-12-01','2027-01-01',NULL,'pending',NULL,'','2026-04-07 13:55:02.479822','2026-04-07 13:55:02.479849',5),(61,'monthly',110.00,'2026-01-01','2026-02-01',NULL,'overdue',NULL,'','2026-04-07 13:55:04.117166','2026-04-07 13:55:04.117186',6),(62,'monthly',110.00,'2026-02-01','2026-03-01',NULL,'overdue',NULL,'','2026-04-07 13:55:04.118345','2026-04-07 13:55:04.118384',6),(63,'monthly',110.00,'2026-03-01','2026-04-01',NULL,'overdue',NULL,'','2026-04-07 13:55:04.119696','2026-04-07 13:55:04.119718',6),(64,'monthly',110.00,'2026-04-01','2026-05-01',NULL,'pending',NULL,'','2026-04-07 13:55:04.120864','2026-04-07 13:55:04.120885',6),(65,'monthly',110.00,'2026-05-01','2026-06-01',NULL,'pending',NULL,'','2026-04-07 13:55:04.122277','2026-04-07 13:55:04.122297',6),(66,'monthly',110.00,'2026-06-01','2026-07-01',NULL,'pending',NULL,'','2026-04-07 13:55:04.123471','2026-04-07 13:55:04.123492',6),(67,'monthly',110.00,'2026-07-01','2026-08-01',NULL,'pending',NULL,'','2026-04-07 13:55:04.124593','2026-04-07 13:55:04.124613',6),(68,'monthly',110.00,'2026-08-01','2026-09-01',NULL,'pending',NULL,'','2026-04-07 13:55:04.125789','2026-04-07 13:55:04.125810',6),(69,'monthly',110.00,'2026-09-01','2026-10-01',NULL,'pending',NULL,'','2026-04-07 13:55:04.126915','2026-04-07 13:55:04.126935',6),(70,'monthly',110.00,'2026-10-01','2026-11-01',NULL,'pending',NULL,'','2026-04-07 13:55:04.128049','2026-04-07 13:55:04.128068',6),(71,'monthly',110.00,'2026-11-01','2026-12-01',NULL,'pending',NULL,'','2026-04-07 13:55:04.129300','2026-04-07 13:55:04.129321',6),(72,'monthly',110.00,'2026-12-01','2027-01-01',NULL,'pending',NULL,'','2026-04-07 13:55:04.130516','2026-04-07 13:55:04.130537',6),(73,'monthly',35.00,'2026-01-01','2026-02-01','2026-04-07','paid','REC-000073','','2026-04-07 14:42:26.383598','2026-04-08 04:25:40.438186',7),(74,'monthly',35.00,'2026-02-01','2026-03-01','2026-04-07','paid','REC-000074','','2026-04-07 14:42:26.385159','2026-04-08 04:25:40.455905',7),(75,'monthly',35.00,'2026-03-01','2026-04-01',NULL,'overdue',NULL,'','2026-04-07 14:42:26.386315','2026-04-07 14:42:26.386340',7),(76,'monthly',35.00,'2026-04-01','2026-05-01',NULL,'pending',NULL,'','2026-04-07 14:42:26.387549','2026-04-07 14:42:26.387574',7),(77,'monthly',35.00,'2026-05-01','2026-06-01',NULL,'pending',NULL,'','2026-04-07 14:42:26.388659','2026-04-07 14:42:26.388684',7),(78,'monthly',35.00,'2026-06-01','2026-07-01',NULL,'pending',NULL,'','2026-04-07 14:42:26.389777','2026-04-07 14:42:26.389811',7),(79,'monthly',35.00,'2026-07-01','2026-08-01',NULL,'pending',NULL,'','2026-04-07 14:42:26.390955','2026-04-07 14:42:26.390980',7),(80,'monthly',35.00,'2026-08-01','2026-09-01',NULL,'pending',NULL,'','2026-04-07 14:42:26.392096','2026-04-07 14:42:26.392121',7),(81,'monthly',35.00,'2026-09-01','2026-10-01',NULL,'pending',NULL,'','2026-04-07 14:42:26.395697','2026-04-07 14:42:26.395752',7),(82,'monthly',35.00,'2026-10-01','2026-11-01',NULL,'pending',NULL,'','2026-04-07 14:42:26.397651','2026-04-07 14:42:26.397680',7),(83,'monthly',35.00,'2026-11-01','2026-12-01',NULL,'pending',NULL,'','2026-04-07 14:42:26.399454','2026-04-07 14:42:26.399481',7),(84,'monthly',35.00,'2026-12-01','2027-01-01',NULL,'pending',NULL,'','2026-04-07 14:42:26.400963','2026-04-07 14:42:26.401011',7),(85,'monthly',35.00,'2026-01-01','2026-02-01','2026-04-07','paid','REC-000085','','2026-04-07 14:47:11.298131','2026-04-08 04:25:40.470850',8),(86,'monthly',35.00,'2026-02-01','2026-03-01',NULL,'overdue',NULL,'','2026-04-07 14:47:11.301047','2026-04-07 14:47:11.301089',8),(87,'monthly',35.00,'2026-03-01','2026-04-01',NULL,'overdue',NULL,'','2026-04-07 14:47:11.303134','2026-04-07 14:47:11.303188',8),(88,'monthly',35.00,'2026-04-01','2026-05-01',NULL,'pending',NULL,'','2026-04-07 14:47:11.305189','2026-04-07 14:47:11.305224',8),(89,'monthly',35.00,'2026-05-01','2026-06-01',NULL,'pending',NULL,'','2026-04-07 14:47:11.306925','2026-04-07 14:47:11.306948',8),(90,'monthly',35.00,'2026-06-01','2026-07-01',NULL,'pending',NULL,'','2026-04-07 14:47:11.308591','2026-04-07 14:47:11.308642',8),(91,'monthly',35.00,'2026-07-01','2026-08-01',NULL,'pending',NULL,'','2026-04-07 14:47:11.310268','2026-04-07 14:47:11.310295',8),(92,'monthly',35.00,'2026-08-01','2026-09-01',NULL,'pending',NULL,'','2026-04-07 14:47:11.311446','2026-04-07 14:47:11.311472',8),(93,'monthly',35.00,'2026-09-01','2026-10-01',NULL,'pending',NULL,'','2026-04-07 14:47:11.312641','2026-04-07 14:47:11.312678',8),(94,'monthly',35.00,'2026-10-01','2026-11-01',NULL,'pending',NULL,'','2026-04-07 14:47:11.314016','2026-04-07 14:47:11.314043',8),(95,'monthly',35.00,'2026-11-01','2026-12-01',NULL,'pending',NULL,'','2026-04-07 14:47:11.316523','2026-04-07 14:47:11.316565',8),(96,'monthly',35.00,'2026-12-01','2027-01-01',NULL,'pending',NULL,'','2026-04-07 14:47:11.318388','2026-04-07 14:47:11.318432',8),(97,'tshirt',45.00,NULL,'2026-01-31',NULL,'overdue',NULL,'T-ShirtTaekwondo','2026-04-09 04:50:30.743602','2026-04-09 05:05:06.378847',7);
/*!40000 ALTER TABLE `fees_fee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schools_classschedule`
--

DROP TABLE IF EXISTS `schools_classschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schools_classschedule` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `day` varchar(3) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `belt_level` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `instructor` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `club_id` bigint NOT NULL,
  `school_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `schools_classschedule_club_id_1049c369_fk_schools_club_id` (`club_id`),
  KEY `schools_classschedule_school_id_2c451ea3_fk_schools_school_id` (`school_id`),
  CONSTRAINT `schools_classschedule_club_id_1049c369_fk_schools_club_id` FOREIGN KEY (`club_id`) REFERENCES `schools_club` (`id`),
  CONSTRAINT `schools_classschedule_school_id_2c451ea3_fk_schools_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools_school` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schools_classschedule`
--

LOCK TABLES `schools_classschedule` WRITE;
/*!40000 ALTER TABLE `schools_classschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `schools_classschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schools_club`
--

DROP TABLE IF EXISTS `schools_club`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schools_club` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subdomain` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `logo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `primary_color` varchar(7) COLLATE utf8mb4_unicode_ci NOT NULL,
  `secondary_color` varchar(7) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `website` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `subscription_tier` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `max_students` int NOT NULL,
  `subscription_expiry` date DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `subdomain` (`subdomain`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schools_club`
--

LOCK TABLES `schools_club` WRITE;
/*!40000 ALTER TABLE `schools_club` DISABLE KEYS */;
INSERT INTO `schools_club` VALUES (1,'Taiping Taekwondo Club','ttc','club_logos/logo_uo0Qw3Y.png','#007bff','#6c757d','amyrul@msn.com','0122604141','Taiping','',1,'free',50,NULL,'2026-04-07 13:17:54.568315','2026-04-07 13:17:54.568344'),(2,'Raintown TaeKwonDo Club','rtc','club_logos/raintown_gO435DF.jpg','#007bff','#6c757d','raintown@msn.com','013313120','Kamunting','',1,'free',50,NULL,'2026-04-07 13:19:00.214103','2026-04-07 13:19:00.214154'),(3,'TaeKwonDo SYSTEM','taekwondo-system','club_logos/dojang_nF7cQUm.png','#007bff','#6c757d','','','','',1,'free',50,NULL,'2026-04-09 06:19:18.061502','2026-04-09 06:19:18.061533');
/*!40000 ALTER TABLE `schools_club` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schools_contactinfo`
--

DROP TABLE IF EXISTS `schools_contactinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schools_contactinfo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_emergency` tinyint(1) NOT NULL,
  `order` int NOT NULL,
  `club_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `schools_contactinfo_club_id_b72ed766_fk_schools_club_id` (`club_id`),
  CONSTRAINT `schools_contactinfo_club_id_b72ed766_fk_schools_club_id` FOREIGN KEY (`club_id`) REFERENCES `schools_club` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schools_contactinfo`
--

LOCK TABLES `schools_contactinfo` WRITE;
/*!40000 ALTER TABLE `schools_contactinfo` DISABLE KEYS */;
INSERT INTO `schools_contactinfo` VALUES (1,'ayie simonm','Coach','0162264972','ayie@msn.com',1,0,1),(2,'Ali Bin Ahmad','Coach','012-1112223','coach_rt_ali@raintown.com',1,0,2);
/*!40000 ALTER TABLE `schools_contactinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schools_school`
--

DROP TABLE IF EXISTS `schools_school`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schools_school` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `monthly_fee` decimal(10,2) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `club_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `schools_school_club_id_name_f8c1f036_uniq` (`club_id`,`name`),
  UNIQUE KEY `schools_school_club_id_code_b10c8374_uniq` (`club_id`,`code`),
  CONSTRAINT `schools_school_club_id_6cf72f8e_fk_schools_club_id` FOREIGN KEY (`club_id`) REFERENCES `schools_club` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schools_school`
--

LOCK TABLES `schools_school` WRITE;
/*!40000 ALTER TABLE `schools_school` DISABLE KEYS */;
INSERT INTO `schools_school` VALUES (1,'SK KAMPUNG BOYAN','SKB','TIAPING PERAK','0112345678','boyan@msn.com',35.00,1,'2026-04-07 13:22:08.056479',1),(2,'SK SERI AMAN','SKSA','TAIPING PERAK','0141234651','SKSA@MSN.COM',35.00,1,'2026-04-07 13:22:49.447823',1),(3,'SK AYER PUTEH','SAP','SIMPANG TAIPING','0193125130','SKP@MSN.CPOM',35.00,1,'2026-04-07 13:23:25.769458',1),(4,'SK SELAMA','SKS','SELAMA PERAK','0197893120','SKS@MSN.COM',35.00,1,'2026-04-07 13:23:55.613894',1),(5,'PRIMA BAGAN SERAI','PGS','BAGAN SERAI PERAK','0141236782','PBS@MSN.COM',40.00,1,'2026-04-07 13:24:33.563099',1),(6,'SK TAMAN TASIK','SKTT','TAMAN TASIK TAIPING','0183125230','SKTT@MSN.COM',35.00,1,'2026-04-07 13:25:20.932922',2),(7,'SERATAS','STS','TAMAN TASIK TAIPING','0194321672','SERATAS@MSN.COM',50.00,1,'2026-04-07 13:26:00.070843',2),(8,'SK AULONG','SKA','ALONG TAIPING','0183125671','SKAULONG@MSN.COM',40.00,1,'2026-04-07 13:26:32.659397',2),(9,'RainTown Main Academy','RT001','Jalan RainTown 1, Kuala Lumpur','03-12345678','',120.00,1,'2026-04-07 13:54:48.788713',2),(10,'RainTown Bukit Jalil','RT002','Bukit Jalil, Kuala Lumpur','03-87654321','',130.00,1,'2026-04-07 13:54:48.804333',2),(11,'RainTown Puchong','RT003','Puchong, Selangor','03-11223344','',110.00,1,'2026-04-07 13:54:48.820740',2);
/*!40000 ALTER TABLE `schools_school` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schools_userprofile`
--

DROP TABLE IF EXISTS `schools_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schools_userprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `club_id` bigint DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `schools_userprofile_club_id_93bdbfb6_fk_schools_club_id` (`club_id`),
  CONSTRAINT `schools_userprofile_club_id_93bdbfb6_fk_schools_club_id` FOREIGN KEY (`club_id`) REFERENCES `schools_club` (`id`),
  CONSTRAINT `schools_userprofile_user_id_d2eb802b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schools_userprofile`
--

LOCK TABLES `schools_userprofile` WRITE;
/*!40000 ALTER TABLE `schools_userprofile` DISABLE KEYS */;
INSERT INTO `schools_userprofile` VALUES (1,'club_admin','0122604141',1,2),(2,'club_admin','',2,3),(3,'coach','0162264972',1,4),(4,'club_admin','012-3456789',2,5),(5,'coach','012-1112223',2,6),(6,'coach','012-4445556',2,7),(7,'coach','012-7778889',2,8),(8,'super_admin','',NULL,1);
/*!40000 ALTER TABLE `schools_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schools_userprofile_schools`
--

DROP TABLE IF EXISTS `schools_userprofile_schools`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schools_userprofile_schools` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `userprofile_id` bigint NOT NULL,
  `school_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `schools_userprofile_scho_userprofile_id_school_id_2d2939c8_uniq` (`userprofile_id`,`school_id`),
  KEY `schools_userprofile__school_id_b46798e8_fk_schools_s` (`school_id`),
  CONSTRAINT `schools_userprofile__school_id_b46798e8_fk_schools_s` FOREIGN KEY (`school_id`) REFERENCES `schools_school` (`id`),
  CONSTRAINT `schools_userprofile__userprofile_id_f60a7d05_fk_schools_u` FOREIGN KEY (`userprofile_id`) REFERENCES `schools_userprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schools_userprofile_schools`
--

LOCK TABLES `schools_userprofile_schools` WRITE;
/*!40000 ALTER TABLE `schools_userprofile_schools` DISABLE KEYS */;
INSERT INTO `schools_userprofile_schools` VALUES (1,3,1),(2,5,10),(3,6,9),(4,7,9),(5,7,10);
/*!40000 ALTER TABLE `schools_userprofile_schools` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_parent`
--

DROP TABLE IF EXISTS `students_parent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students_parent` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `phone` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `relationship` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `students_parent_user_id_student_id_c853728f_uniq` (`user_id`,`student_id`),
  KEY `students_parent_student_id_42cf9546_fk_students_student_id` (`student_id`),
  CONSTRAINT `students_parent_student_id_42cf9546_fk_students_student_id` FOREIGN KEY (`student_id`) REFERENCES `students_student` (`id`),
  CONSTRAINT `students_parent_user_id_4c06a8f5_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_parent`
--

LOCK TABLES `students_parent` WRITE;
/*!40000 ALTER TABLE `students_parent` DISABLE KEYS */;
INSERT INTO `students_parent` VALUES (1,'','Parent','2026-04-07 13:54:55.769275',9,1),(2,'','Parent','2026-04-07 13:54:57.441506',10,2),(3,'','Parent','2026-04-07 13:54:59.136893',11,3),(4,'','Parent','2026-04-07 13:55:00.784712',12,4),(5,'','Parent','2026-04-07 13:55:02.465111',13,5),(6,'','Parent','2026-04-07 13:55:04.115658',14,6),(13,'','Parent','2026-04-07 14:42:26.381721',21,7),(14,'','Parent','2026-04-07 14:47:11.296537',21,8);
/*!40000 ALTER TABLE `students_parent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_student`
--

DROP TABLE IF EXISTS `students_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students_student` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `student_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ic_number` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_of_birth` date NOT NULL,
  `gender` varchar(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `parent_ic` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `belt_rank` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `join_date` date NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `phone` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `emergency_contact` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `emergency_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `medical_conditions` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `blood_type` varchar(3) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `club_id` bigint DEFAULT NULL,
  `school_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_id` (`student_id`),
  UNIQUE KEY `ic_number` (`ic_number`),
  KEY `students_student_club_id_fcfae758_fk_schools_club_id` (`club_id`),
  KEY `students_student_school_id_be4a7ab9_fk_schools_school_id` (`school_id`),
  CONSTRAINT `students_student_club_id_fcfae758_fk_schools_club_id` FOREIGN KEY (`club_id`) REFERENCES `schools_club` (`id`),
  CONSTRAINT `students_student_school_id_be4a7ab9_fk_schools_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools_school` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_student`
--

LOCK TABLES `students_student` WRITE;
/*!40000 ALTER TABLE `students_student` DISABLE KEYS */;
INSERT INTO `students_student` VALUES (1,'RTC2026001','Muhammad Danish','050101141234','2015-01-01','M','800101141234','blue_1','2026-04-07',1,'012-3456789','','RainTown Main Academy, Malaysia','012-3456789','Encik Danish','','','2026-04-07 13:54:54.161409','2026-04-07 13:54:54.161453',2,9),(2,'RTC2026002','Nur Aisyah','050202145678','2015-02-02','F','800202145678','green_1','2026-04-07',1,'012-3456780','','RainTown Main Academy, Malaysia','012-3456780','Puan Aisyah','','','2026-04-07 13:54:55.803968','2026-04-07 13:54:55.803987',2,9),(3,'RTC2026003','Lim Zheng Wei','050303149012','2015-03-03','M','800303149012','yellow_2','2026-04-07',1,'012-3456781','','RainTown Main Academy, Malaysia','012-3456781','Encik Lim','','','2026-04-07 13:54:57.476424','2026-04-07 13:54:57.476442',2,9),(4,'RTC2026004','Thivya a/p Raj','060404143456','2016-04-04','F','810404143456','yellow_1','2026-04-07',1,'012-3456782','','RainTown Bukit Jalil, Malaysia','012-3456782','Encik Raj','','','2026-04-07 13:54:59.170625','2026-04-07 13:54:59.170642',2,10),(5,'RTC2026005','Muhammad Haikal','060505147890','2016-05-05','M','810505147890','white','2026-04-07',1,'012-3456783','','RainTown Bukit Jalil, Malaysia','012-3456783','Encik Haikal','','','2026-04-07 13:55:00.817967','2026-04-07 13:55:00.817998',2,10),(6,'RTC2026006','Wong Mei Ling','070606141234','2017-06-06','F','820606141234','white','2026-04-07',1,'012-3456784','','RainTown Puchong, Malaysia','012-3456784','Puan Wong','','','2026-04-07 13:55:02.499538','2026-04-07 13:55:02.499578',2,11),(7,'TTC2026001','Haziq','150728085911','2015-07-28','M','730728085911','white','2026-01-01',1,'0193125120','','KAMPONG BOYAN FLAT','0193125120','MIA','','','2026-04-07 14:42:24.534598','2026-04-07 14:42:24.534624',1,1),(8,'TTC2026002','MIA','160728085911','2016-07-28','F','730728085911','white','2026-01-01',1,'0193215120','','KAMPUNG BOYANG','0193215120','MAK MIA','','','2026-04-07 14:47:11.291279','2026-04-07 14:47:11.291303',1,1);
/*!40000 ALTER TABLE `students_student` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-15 11:21:36
