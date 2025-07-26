-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: marketplace
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `id_producto` int NOT NULL,
  `contenido` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `destino` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `estado` enum('pendiente','enviado','entregado','cancelado') COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`) ON DELETE CASCADE,
  CONSTRAINT `pedido_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `alergenos` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `paradero` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `origen` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_vendedor` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_vendedor` (`id_vendedor`),
  CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`id_vendedor`) REFERENCES `usuario` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (12,'Manzanas','fruta','A1','Mercado Central','Tarragona',6),(13,'Naranjas','fruta','A2','Mercado Central','Valencia',7),(14,'Leche','lácteo','B3','Tienda Bio','Tarragona',8),(15,'Pan','panadería','A1,B3','Panadería Sol','Tarragona',9),(16,'Queso','lácteo','A2','Mercado Central','Reus',10),(17,'Tomates','verdura','','Mercado Central','Tarragona',6),(18,'Aceite','aceite','','Tienda Bio','Siurana',7),(19,'Huevos','huevos','','Mercado Central','Tarragona',8),(20,'Miel','miel','','Tienda Bio','Prades',9),(21,'Pera','fruta','A1','Mercado Central','Lleida',10),(22,'Chuletón','carne de ternera','','Carnicería Central','Tarragona',6);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `apellido1` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `apellido2` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `correo` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contraseña` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `direccion` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rol` enum('cliente','vendedor') COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'Juan','Pérez','García','juan1@correo.com','$2b$12$CvnNSVGc6/X31hqco8zP3e88XSfnPxjR0KvzSbziF0qza.v6hZYdO','Calle Mayor 1','600000001','cliente'),(2,'Ana','López','Martínez','ana2@correo.com','$2b$12$CvnNSVGc6/X31hqco8zP3e88XSfnPxjR0KvzSbziF0qza.v6hZYdO','Calle Sol 2','600000002','cliente'),(3,'Luis','Sánchez','Ruiz','luis3@correo.com','$2b$12$CvnNSVGc6/X31hqco8zP3e88XSfnPxjR0KvzSbziF0qza.v6hZYdO','Calle Luna 3','600000003','cliente'),(4,'Marta','Gómez','Díaz','marta4@correo.com','$2b$12$CvnNSVGc6/X31hqco8zP3e88XSfnPxjR0KvzSbziF0qza.v6hZYdO','Calle Mar 4','600000004','cliente'),(5,'Pedro','Fernández','Moreno','pedro5@correo.com','$2b$12$CvnNSVGc6/X31hqco8zP3e88XSfnPxjR0KvzSbziF0qza.v6hZYdO','Calle Río 5','600000005','cliente'),(6,'Lucía','Jiménez','Navarro','lucia6@correo.com','$2b$12$CvnNSVGc6/X31hqco8zP3e88XSfnPxjR0KvzSbziF0qza.v6hZYdO','Calle Viento 6','600000006','vendedor'),(7,'Carlos','Romero','Serrano','carlos7@correo.com','$2b$12$CvnNSVGc6/X31hqco8zP3e88XSfnPxjR0KvzSbziF0qza.v6hZYdO','Calle Fuego 7','600000007','vendedor'),(8,'Elena','Torres','Ramos','elena8@correo.com','$2b$12$CvnNSVGc6/X31hqco8zP3e88XSfnPxjR0KvzSbziF0qza.v6hZYdO','Calle Tierra 8','600000008','vendedor'),(9,'David','Vega','Castro','david9@correo.com','$2b$12$CvnNSVGc6/X31hqco8zP3e88XSfnPxjR0KvzSbziF0qza.v6hZYdO','Calle Nube 9','600000009','vendedor'),(10,'Sara','Molina','Ortega','sara10@correo.com','$2b$12$CvnNSVGc6/X31hqco8zP3e88XSfnPxjR0KvzSbziF0qza.v6hZYdO','Calle Flor 10','600000010','vendedor');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-26 10:13:03
