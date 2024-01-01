-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 01, 2023 at 03:27 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `price_comparison`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `rt_cart`
--

CREATE TABLE `rt_cart` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pid` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `price` int(11) NOT NULL,
  `category` varchar(30) NOT NULL,
  `quantity` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `bill_id` int(11) NOT NULL,
  `check_st` int(11) NOT NULL,
  `av_product` int(11) NOT NULL,
  `retailer` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rt_cart`
--

INSERT INTO `rt_cart` (`id`, `uname`, `pid`, `status`, `rdate`, `price`, `category`, `quantity`, `amount`, `bill_id`, `check_st`, `av_product`, `retailer`) VALUES
(1, 'siva', 5, 0, '21-03-2023', 13000, 'Oppo', 1, 13000, 0, 0, 0, 'poorvika');

-- --------------------------------------------------------

--
-- Table structure for table `rt_category`
--

CREATE TABLE `rt_category` (
  `id` int(11) NOT NULL,
  `retailer` varchar(20) NOT NULL,
  `category` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rt_category`
--

INSERT INTO `rt_category` (`id`, `retailer`, `category`) VALUES
(1, 'amazon', 'Mobile'),
(2, 'amazon', 'Laptop'),
(3, 'amazon', 'Camera'),
(4, 'homeshop', 'Mobile'),
(5, 'homeshop', 'Laptop'),
(6, 'poorvika', 'Mobile'),
(7, 'flipkart', 'Mobile');

-- --------------------------------------------------------

--
-- Table structure for table `rt_customer`
--

CREATE TABLE `rt_customer` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `create_date` varchar(20) NOT NULL,
  `otp` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rt_customer`
--

INSERT INTO `rt_customer` (`id`, `name`, `address`, `city`, `mobile`, `email`, `uname`, `pass`, `create_date`, `otp`) VALUES
(1, 'Siva', '5, Big Bazar Road', 'Trichy', 8541212545, 'siva@gmail.com', 'siva', '123456', '14-03-2023', '');

-- --------------------------------------------------------

--
-- Table structure for table `rt_product`
--

CREATE TABLE `rt_product` (
  `id` int(11) NOT NULL,
  `retailer` varchar(20) NOT NULL,
  `category` varchar(50) NOT NULL,
  `product` varchar(100) NOT NULL,
  `price` double NOT NULL,
  `quantity` int(11) NOT NULL,
  `photo` varchar(50) NOT NULL,
  `details` varchar(200) NOT NULL,
  `status` int(11) NOT NULL,
  `required_qty` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rt_product`
--

INSERT INTO `rt_product` (`id`, `retailer`, `category`, `product`, `price`, `quantity`, `photo`, `details`, `status`, `required_qty`) VALUES
(1, 'amazon', 'Mobile', 'Oppo', 16000, 10, 'P1P1oppo.jpg', '6.6 inch screen ,129 GB, 48 MP', 0, 0),
(2, 'homeshop', 'Mobile', 'Asus Mobile', 15000, 10, 'P2P3asus.jpg', 'Black, 128 GB, 28MP Camera', 0, 0),
(3, 'homeshop', 'Mobile', 'Oppo', 14500, 10, 'P3P1oppo.jpg', 'Black, 128 GB, 24MP Camera', 0, 0),
(4, 'poorvika', 'Mobile', 'Vivo z5x', 12000, 10, 'P4P2vivo-z5x.jpg', 'White, 64 GB, 16 MP', 0, 0),
(5, 'poorvika', 'Mobile', 'Oppo', 13000, 10, 'P5P1oppo.jpg', 'White, 64 GB, 16 MP', 0, 1),
(6, 'flipkart', 'Mobile', 'Oppo', 18000, 10, 'P6P1oppo.jpg', 'Black, 128 GB, 32MP Camera', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `rt_purchase`
--

CREATE TABLE `rt_purchase` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `amount` int(11) NOT NULL,
  `rdate` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rt_purchase`
--


-- --------------------------------------------------------

--
-- Table structure for table `rt_reply`
--

CREATE TABLE `rt_reply` (
  `id` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `retailer` varchar(20) NOT NULL,
  `product` varchar(50) NOT NULL,
  `price` double NOT NULL,
  `photo` varchar(50) NOT NULL,
  `details` text NOT NULL,
  `status` int(11) NOT NULL,
  `date_time` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rt_reply`
--

INSERT INTO `rt_reply` (`id`, `pid`, `retailer`, `product`, `price`, `photo`, `details`, `status`, `date_time`) VALUES
(1, 1, 'homeshop', 'Oppo A54', 15990, 'R1op1.jpg', 'Rear Camera: 13 MP + 2 MP + 2 MP, 4 GB RAM and 128 GB internal memory, Color : Starry Blue, 1 Year Manufacturer Warranty', 1, '2023-03-15 19:56:00');

-- --------------------------------------------------------

--
-- Table structure for table `rt_request`
--

CREATE TABLE `rt_request` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `product` varchar(50) NOT NULL,
  `date_time` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `status` int(11) NOT NULL,
  `retailer` varchar(20) NOT NULL,
  `details` varchar(200) NOT NULL,
  `reply_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rt_request`
--

INSERT INTO `rt_request` (`id`, `uname`, `product`, `date_time`, `status`, `retailer`, `details`, `reply_id`) VALUES
(1, 'siva', 'oppo', '2023-03-15 20:17:21', 1, 'homeshop', 'big bazar', 1);

-- --------------------------------------------------------

--
-- Table structure for table `rt_retailer`
--

CREATE TABLE `rt_retailer` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `create_date` varchar(20) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rt_retailer`
--

INSERT INTO `rt_retailer` (`id`, `name`, `address`, `city`, `mobile`, `email`, `uname`, `pass`, `create_date`, `status`) VALUES
(1, 'Home Shop', '8, Bazar', 'Thanjavur', 8956214752, 'mshop1@gmail.com', 'homeshop', '123456', '13-03-2023', 1),
(2, 'Poorvika', '5, Big Bazar Road', 'Trichy', 8541212545, 'poorvika@gmail.com', 'poorvika', '123456', '13-03-2023', 1),
(3, 'Flipkart', '8, Bazar', 'Thanjavur', 8956214752, 'flipkart@gmail.com', 'flipkart', '123456', '14-03-2023', 1),
(4, 'Amazon', '31, Bus Stand', 'Erode', 8785454545, 'amazon@gmail.com', 'amazon', '123456', '14-03-2023', 1);
