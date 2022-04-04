-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 14, 2019 at 06:42 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */
;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */
;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */
;
/*!40101 SET NAMES utf8mb4 */
;
--
-- Database: `cart`
--
CREATE DATABASE IF NOT EXISTS `inventory` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `inventory`;
-- --------------------------------------------------------
--
-- Table structure for table `cart`
--
DROP TABLE IF EXISTS `inventory`;
CREATE TABLE IF NOT EXISTS `inventory` (
    `product_id` int(11) NOT NULL AUTO_INCREMENT,
    `product_name` varchar(64) NOT NULL,
    `quantity` int(11) DEFAULT NULL,
    `price` int(11) DEFAULT NULL,
    PRIMARY KEY (`product_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
--
-- Dumping data for table `cart`
--
INSERT INTO `inventory` (
        `product_id`,
        `product_name`,
        `quantity`,
        `price`
    )
VALUES (1, 'apple', 100, 80),
    (2, 'banana', 5, 400),
    (3, 'pineapple', 0, 250),
    (4, 'orange', 1000, 100),
    (5, 'pear', 1000, 110),
    (6, 'grapes', 1000, 500);
COMMIT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */
;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */
;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */
;