-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Янв 31 2022 г., 19:00
-- Версия сервера: 10.4.18-MariaDB
-- Версия PHP: 8.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `hackaton`
--

-- --------------------------------------------------------

--
-- Структура таблицы `admin_applications`
--

CREATE TABLE `admin_applications` (
  `id` int(11) NOT NULL,
  `application_id` int(11) NOT NULL,
  `administration_id` int(11) NOT NULL,
  `task_type` tinyint(1) NOT NULL DEFAULT 0,
  `explanation` varchar(255) DEFAULT NULL,
  `estimated_date_work` date DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `media_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`media_data`)),
  `create_date` datetime NOT NULL DEFAULT current_timestamp(),
  `update_date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `applications`
--

CREATE TABLE `applications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `redirect_to_application_id` int(11) DEFAULT NULL,
  `address` varchar(255) NOT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL,
  `status_id` int(11) DEFAULT 1,
  `media_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`media_data`)),
  `applicants_details` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`applicants_details`)),
  `review_date` datetime DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `complete_date` datetime DEFAULT NULL,
  `final_date` datetime DEFAULT NULL,
  `is_moderate` tinyint(1) NOT NULL DEFAULT 0,
  `moderator_id` int(11) DEFAULT NULL,
  `problem_desc` varchar(255) DEFAULT NULL,
  `base_rate` int(11) NOT NULL DEFAULT 0,
  `source` varchar(255) DEFAULT NULL,
  `delete_date` datetime DEFAULT NULL,
  `create_date` datetime NOT NULL DEFAULT current_timestamp(),
  `update_date` datetime NOT NULL DEFAULT current_timestamp(),
  `views_count` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `applications_categories`
--

CREATE TABLE `applications_categories` (
  `id` int(11) NOT NULL,
  `application_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `application_status`
--

CREATE TABLE `application_status` (
  `id` int(11) NOT NULL,
  `title` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `application_status`
--

INSERT INTO `application_status` (`id`, `title`) VALUES
(6, 'Архивная'),
(1, 'В обработке'),
(2, 'В рассмотрении'),
(5, 'Выполнено'),
(3, 'Исполнение'),
(4, 'Проверка исполнения');

-- --------------------------------------------------------

--
-- Структура таблицы `contractors_problems`
--

CREATE TABLE `contractors_problems` (
  `id` int(11) NOT NULL,
  `problem_id` int(11) NOT NULL,
  `contractor_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `contractors_problems`
--

INSERT INTO `contractors_problems` (`id`, `problem_id`, `contractor_id`) VALUES
(3, 16, 3),
(4, 2, 5),
(5, 3, 5),
(6, 11, 5),
(7, 4, 6),
(8, 5, 9),
(9, 6, 6),
(10, 7, 6),
(11, 8, 8),
(12, 9, 6),
(13, 10, 6),
(14, 10, 7),
(15, 11, 5),
(16, 11, 7),
(17, 12, 3),
(18, 13, 7),
(19, 15, 6),
(20, 16, 3),
(21, 11, 11),
(22, 14, 10);

-- --------------------------------------------------------

--
-- Структура таблицы `executive_authority`
--

CREATE TABLE `executive_authority` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `mnemomic_name` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `responsible_person` varchar(255) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `hash_tag` varchar(255) DEFAULT NULL,
  `contact_phone` varchar(20) DEFAULT NULL,
  `contact_email` varchar(255) DEFAULT NULL,
  `contact_email_administration` varchar(255) DEFAULT NULL,
  `tg_id` varchar(255) DEFAULT NULL,
  `web_site_link` varchar(255) DEFAULT NULL,
  `additional_information` varchar(255) DEFAULT NULL,
  `type` varchar(20) NOT NULL DEFAULT 'исполнительный',
  `work_schedule` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`work_schedule`)),
  `is_email_alert` tinyint(1) NOT NULL DEFAULT 0,
  `is_sms_alert` tinyint(1) NOT NULL DEFAULT 0,
  `is_generate_daily_report` tinyint(1) NOT NULL DEFAULT 0,
  `is_visible` tinyint(1) NOT NULL DEFAULT 1,
  `create_date` datetime NOT NULL DEFAULT current_timestamp(),
  `update_date` datetime NOT NULL DEFAULT current_timestamp(),
  `delete_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `executive_authority`
--

INSERT INTO `executive_authority` (`id`, `title`, `mnemomic_name`, `description`, `responsible_person`, `image`, `hash_tag`, `contact_phone`, `contact_email`, `contact_email_administration`, `tg_id`, `web_site_link`, `additional_information`, `type`, `work_schedule`, `is_email_alert`, `is_sms_alert`, `is_generate_daily_report`, `is_visible`, `create_date`, `update_date`, `delete_date`) VALUES
(3, 'Министерство внутренних дел', 'mvd', 'Министерство внутренних дел - контролирующий орган', 'Петров В.В., старший лейтинант', 'avatar.jpg', '#мвд', '0713333333', 'mvd@mvd.com', 'mvd@mvd.com', '-1001519915986', 'https://mvd.com', 'На службе добра', 'EXECUTIVE', '[]', 1, 1, 1, 1, '2022-01-29 20:36:00', '2022-01-29 20:36:00', NULL),
(5, 'Министерство транспорта', 'transport', 'Министерство транспорта, контролирует транспорт =)', 'Петров П.П.', NULL, '#мин_транспорта', '071000000', NULL, NULL, '-1001519915986', 'http://donmintrans.ru', NULL, 'исполнительный', NULL, 0, 0, 0, 1, '2022-01-31 19:53:54', '2022-01-31 19:53:54', '2022-01-31 17:48:35'),
(6, 'Министерство агропромышленной политики и продовольствия', 'agroprom', 'Министерство агропромышленной политики и продовольствия', 'Петров П.П.', NULL, '#мин_агропром', NULL, NULL, NULL, '-1001519915986', NULL, NULL, 'исполнительный', NULL, 0, 0, 0, 1, '2022-01-31 20:00:16', '2022-01-31 20:00:16', NULL),
(7, 'МЧС', 'mchs', 'МЧС ДНР', 'Петрова Г.А.', NULL, '#мчс', NULL, NULL, NULL, '-1001519915986', 'https://dnmchs.ru', NULL, 'исполнительный', NULL, 0, 0, 0, 1, '2022-01-31 20:01:53', '2022-01-31 20:01:53', NULL),
(8, 'Инспекция по защите прав потребителей', 'potreb_nadzor', NULL, 'Петрова Г.А.', NULL, '#потреб_надзор', NULL, NULL, NULL, '-1001519915986', 'https://izpp.govdnr.ru/', NULL, 'исполнительный', NULL, 0, 0, 0, 1, '2022-01-31 20:08:28', '2022-01-31 20:08:28', NULL),
(9, 'ЖЭК', 'zjek', 'ЖЭК ДНР', NULL, NULL, '#жэк', NULL, NULL, NULL, '-1001519915986', NULL, NULL, 'исполнительный', NULL, 0, 0, 0, 1, '2022-01-31 20:09:42', '2022-01-31 20:09:42', NULL),
(10, 'Профсоюзная комиссия', 'prof_soyouz', NULL, NULL, NULL, '#профсоюз', NULL, NULL, NULL, '-1001519915986', NULL, NULL, 'исполнительный', NULL, 0, 0, 0, 1, '2022-01-31 20:27:03', '2022-01-31 20:27:03', '2022-01-31 18:24:11'),
(11, 'Вооруженные силы ДНР', 'soliders', NULL, NULL, NULL, '#вооруженные_силы', NULL, NULL, NULL, '-1001519915986', NULL, NULL, 'исполнительный', NULL, 0, 0, 0, 1, '2022-01-31 20:27:03', '2022-01-31 20:27:03', '2022-01-31 18:24:11');

-- --------------------------------------------------------

--
-- Структура таблицы `mailing_queue`
--

CREATE TABLE `mailing_queue` (
  `id` int(11) NOT NULL,
  `mailing_address` varchar(30) NOT NULL,
  `mailing_type` tinyint(1) NOT NULL DEFAULT 0,
  `status` tinyint(1) NOT NULL DEFAULT 0,
  `template_name` varchar(30) DEFAULT NULL,
  `template_object` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`template_object`)),
  `application_id` int(11) DEFAULT NULL,
  `create_date` datetime NOT NULL DEFAULT current_timestamp(),
  `update_date` datetime NOT NULL DEFAULT current_timestamp(),
  `delete_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `news`
--

CREATE TABLE `news` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `text` varchar(255) DEFAULT NULL,
  `group_name` varchar(255) DEFAULT NULL,
  `position` int(11) NOT NULL,
  `author_name` varchar(30) NOT NULL,
  `type` tinyint(1) NOT NULL DEFAULT 0,
  `url` varchar(255) DEFAULT NULL,
  `life_time` datetime DEFAULT NULL,
  `duration` time DEFAULT NULL,
  `admin_id` int(11) DEFAULT NULL,
  `is_visible` tinyint(1) NOT NULL DEFAULT 1,
  `create_date` datetime NOT NULL DEFAULT current_timestamp(),
  `update_date` datetime NOT NULL DEFAULT current_timestamp(),
  `delete_date` datetime DEFAULT NULL,
  `stories_type` tinyint(3) NOT NULL DEFAULT 0,
  `views_count` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `problem_categories`
--

CREATE TABLE `problem_categories` (
  `id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `mnemonic_name` varchar(100) NOT NULL,
  `hash_tag` varchar(100) NOT NULL,
  `icon_file_path` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 0,
  `is_visible` tinyint(1) NOT NULL DEFAULT 0,
  `priority` int(11) NOT NULL DEFAULT 0,
  `create_date` datetime NOT NULL DEFAULT current_timestamp(),
  `update_date` datetime NOT NULL DEFAULT current_timestamp(),
  `delete_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `problem_categories`
--

INSERT INTO `problem_categories` (`id`, `title`, `mnemonic_name`, `hash_tag`, `icon_file_path`, `is_active`, `is_visible`, `priority`, `create_date`, `update_date`, `delete_date`) VALUES
(2, 'Общественный транспорт ', 'public_transport', '#общественный_транспорт', '/media/transport_1.png', 1, 1, 0, '2022-01-31 19:28:57', '2022-01-31 19:28:57', NULL),
(3, 'Состояние дорог и прилегающий территорий ', 'road_status_and_territory', '#состояние_дорог', '/media/road_2.png', 1, 1, 0, '2022-01-31 19:30:10', '2022-01-31 19:30:10', NULL),
(4, 'Состояние благоустройства города', 'city_status', '#благоустройство_города', '/media/city_3.png', 1, 1, 0, '2022-01-31 19:31:05', '2022-01-31 19:31:05', NULL),
(5, 'Аварийные участки', 'emergency_areas', '#аварийные_участки', '/media/breaking_4.png', 1, 1, 0, '2022-01-31 19:32:22', '2022-01-31 19:32:22', NULL),
(6, 'Постройки в аварийном состоянии', 'emergency_buildings', '#аварийная_постройка', '/media/building_5.png', 1, 1, 0, '2022-01-31 19:33:20', '2022-01-31 19:33:20', NULL),
(7, 'Уборка территории и вывоз отходов', 'cleaning_territory', '#уборка_территории_и_вызов_отходов', '/media/trash_6.png', 1, 1, 0, '2022-01-31 19:35:07', '2022-01-31 19:35:07', NULL),
(8, 'Некачественные товары ', 'low_quality_goods', '#некачественные_товары', '/media/food_7.png', 1, 1, 0, '2022-01-31 19:36:11', '2022-01-31 19:36:11', NULL),
(9, 'Скопление животных', 'accumulation_of_animals', '#скопление_животных', '/media/animal_8.png', 1, 1, 0, '2022-01-31 19:37:17', '2022-01-31 19:37:17', NULL),
(10, 'Последствия стихийных бедствий', 'consequences_of_natural_disasters', '#стихийные_бедствия', '/media/wind_9.png', 1, 1, 0, '2022-01-31 19:38:45', '2022-01-31 19:38:45', NULL),
(11, 'Последствие военных действий', 'consequences_of_war', '#военные_действия', '/media/tank_10.png', 1, 1, 0, '2022-01-31 19:39:45', '2022-01-31 19:39:45', NULL),
(12, 'Проявления вандализма ', 'vandalism', '#вандализм', '/media/vandalism_11.png', 1, 1, 0, '2022-01-31 19:40:38', '2022-01-31 19:40:38', NULL),
(13, 'Состояние фортификационных сооружений', 'condition_of_fortifications', '#фортификационные_сооружения', '/media/fort_12.png', 1, 1, 0, '2022-01-31 19:42:18', '2022-01-31 19:42:18', NULL),
(14, 'Состояние рабочего места', 'workplace_condition', '#состояние_рабочего_места', '/media/work_13.png', 1, 1, 0, '2022-01-31 19:43:16', '2022-01-31 19:43:16', NULL),
(15, 'Регулярное скопление криминальных элементов общества или проявление аморального поведения в обществе', 'crime', '#криминал', '/media/crime_14.png', 1, 1, 0, '2022-01-31 19:44:56', '2022-01-31 19:44:56', NULL),
(16, 'Нарушение ПДД участниками дорожного движения', 'traffic_regulations', '#пдд', '/media/car_15.png', 1, 1, 0, '2022-01-31 19:45:42', '2022-01-31 19:45:42', NULL),
(17, 'Другое', 'other', '#другое', '/media/', 1, 1, 0, '2022-01-31 19:46:30', '2022-01-31 19:46:30', NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `regions`
--

CREATE TABLE `regions` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `is_available` smallint(6) NOT NULL DEFAULT 0,
  `position` int(11) NOT NULL,
  `create_date` datetime NOT NULL DEFAULT current_timestamp(),
  `update_date` datetime NOT NULL DEFAULT current_timestamp(),
  `delete_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `regions`
--

INSERT INTO `regions` (`id`, `title`, `is_available`, `position`, `create_date`, `update_date`, `delete_date`) VALUES
(2, 'Донецк', 1, 1, '2022-01-19 00:00:00', '2022-01-19 14:11:36', NULL),
(4, 'Макеевка', 1, 2, '2022-01-20 12:27:14', '2022-01-20 12:27:14', NULL),
(5, 'Горловка', 1, 3, '2022-01-20 12:28:43', '2022-01-20 12:28:43', NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `title` varchar(50) NOT NULL,
  `mnemomic_name` varchar(50) DEFAULT NULL,
  `delete_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT current_timestamp(),
  `create_date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `roles`
--

INSERT INTO `roles` (`id`, `title`, `mnemomic_name`, `delete_date`, `update_date`, `create_date`) VALUES
(1, 'ADMINISTRATOR', 'administrator', NULL, '2022-01-20 15:37:01', '2022-01-20 15:37:01'),
(2, 'USER', 'user', NULL, '2022-01-20 15:43:06', '2022-01-20 15:43:06'),
(3, 'GUEST', 'guest', NULL, '2022-01-20 20:56:17', '2022-01-20 20:56:17');

-- --------------------------------------------------------

--
-- Структура таблицы `saved_coord`
--

CREATE TABLE `saved_coord` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` int(11) NOT NULL,
  `explanation` varchar(255) DEFAULT NULL,
  `media_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`media_data`)),
  `create_date` datetime NOT NULL DEFAULT current_timestamp(),
  `update_date` datetime NOT NULL DEFAULT current_timestamp(),
  `delete_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `token_blocklist`
--

CREATE TABLE `token_blocklist` (
  `id` int(11) NOT NULL,
  `jti` varchar(36) NOT NULL,
  `created_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `login` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role_id` int(11) DEFAULT NULL,
  `sms_code` varchar(4) DEFAULT NULL,
  `email_code` varchar(255) DEFAULT NULL,
  `phone_confirm_date` datetime DEFAULT NULL,
  `email_confirm_date` datetime DEFAULT NULL,
  `ban_date` datetime DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `is_admin` tinyint(1) NOT NULL DEFAULT 0,
  `is_stuff` tinyint(1) NOT NULL DEFAULT 0,
  `delete_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT current_timestamp(),
  `create_date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `login`, `password`, `role_id`, `sms_code`, `email_code`, `phone_confirm_date`, `email_confirm_date`, `ban_date`, `is_active`, `is_admin`, `is_stuff`, `delete_date`, `update_date`, `create_date`) VALUES
(2, 'test_admin', '1234', 1, NULL, NULL, '2022-01-20 14:27:25', '2022-01-20 14:27:25', '2022-01-20 14:27:25', 1, 1, 0, '2022-01-20 14:27:25', '2022-01-20 16:27:36', '2022-01-20 16:27:36'),
(5, '0714313265', 'm545454hgfhgfhf', 2, NULL, NULL, NULL, NULL, NULL, 1, 0, 0, NULL, '2022-01-24 23:11:20', '2022-01-24 23:11:20'),
(6, '+380713336666', '12345йцуке', 2, NULL, NULL, NULL, NULL, NULL, 1, 0, 0, NULL, '2022-01-25 12:41:18', '2022-01-25 12:41:18'),
(7, '+380716669999', '123456qwe', 2, NULL, NULL, NULL, NULL, NULL, 1, 0, 0, NULL, '2022-01-25 18:34:08', '2022-01-25 18:34:08');

-- --------------------------------------------------------

--
-- Структура таблицы `user_profiles`
--

CREATE TABLE `user_profiles` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `is_email_alert` tinyint(1) NOT NULL DEFAULT 0,
  `is_sms_alert` tinyint(1) NOT NULL DEFAULT 0,
  `is_anonym` tinyint(1) NOT NULL DEFAULT 0,
  `create_date` datetime NOT NULL DEFAULT current_timestamp(),
  `update_date` datetime NOT NULL DEFAULT current_timestamp(),
  `delete_date` datetime DEFAULT NULL,
  `rate` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `user_profiles`
--

INSERT INTO `user_profiles` (`id`, `user_id`, `name`, `phone_number`, `email`, `location`, `is_email_alert`, `is_sms_alert`, `is_anonym`, `create_date`, `update_date`, `delete_date`, `rate`) VALUES
(1, 2, 'Василий Иванович Пупкин', '+380710000022', 'some12@email.ru', 'ул.Артёма, 15', 0, 0, 0, '2022-01-22 00:56:44', '2022-01-25 18:11:11', NULL, 200),
(2, 5, 'Олег', NULL, NULL, NULL, 0, 0, 0, '2022-01-24 23:11:20', '2022-01-24 23:11:20', NULL, 0),
(3, 6, 'Добрый Иван Петрович', '+380713336666', 'ivan.ivanovich@gmail.com', 'ул.Артёма, 15', 0, 0, 0, '2022-01-25 12:41:18', '2022-01-25 18:18:51', '2022-01-25 18:18:51', 0),
(4, 7, 'Добрыня', '+380716669999', 'dobro32@ukr.com', 'ул.Артёма, 15', 0, 0, 0, '2022-01-25 18:34:08', '2022-01-25 18:40:28', NULL, 0);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `admin_applications`
--
ALTER TABLE `admin_applications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `application_id` (`application_id`),
  ADD KEY `administration_id` (`administration_id`);

--
-- Индексы таблицы `applications`
--
ALTER TABLE `applications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `applications_ibfk_1` (`status_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `moderator_id` (`moderator_id`),
  ADD KEY `applications_ibfk_4` (`redirect_to_application_id`);

--
-- Индексы таблицы `applications_categories`
--
ALTER TABLE `applications_categories`
  ADD PRIMARY KEY (`id`),
  ADD KEY `application_id` (`application_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Индексы таблицы `application_status`
--
ALTER TABLE `application_status`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `title` (`title`),
  ADD KEY `id` (`id`);

--
-- Индексы таблицы `contractors_problems`
--
ALTER TABLE `contractors_problems`
  ADD PRIMARY KEY (`id`),
  ADD KEY `contractor_id` (`contractor_id`),
  ADD KEY `problem_id` (`problem_id`);

--
-- Индексы таблицы `executive_authority`
--
ALTER TABLE `executive_authority`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `title` (`title`,`hash_tag`,`tg_id`);

--
-- Индексы таблицы `mailing_queue`
--
ALTER TABLE `mailing_queue`
  ADD PRIMARY KEY (`id`),
  ADD KEY `application_id` (`application_id`);

--
-- Индексы таблицы `news`
--
ALTER TABLE `news`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ord` (`position`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Индексы таблицы `problem_categories`
--
ALTER TABLE `problem_categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `title` (`title`,`hash_tag`);

--
-- Индексы таблицы `regions`
--
ALTER TABLE `regions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ord` (`position`);

--
-- Индексы таблицы `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`);

--
-- Индексы таблицы `saved_coord`
--
ALTER TABLE `saved_coord`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Индексы таблицы `token_blocklist`
--
ALTER TABLE `token_blocklist`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `login` (`login`,`email_code`),
  ADD KEY `role_id` (`role_id`);

--
-- Индексы таблицы `user_profiles`
--
ALTER TABLE `user_profiles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_profiles_ibfk_1` (`user_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `admin_applications`
--
ALTER TABLE `admin_applications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `applications`
--
ALTER TABLE `applications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=69;

--
-- AUTO_INCREMENT для таблицы `applications_categories`
--
ALTER TABLE `applications_categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- AUTO_INCREMENT для таблицы `application_status`
--
ALTER TABLE `application_status`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `contractors_problems`
--
ALTER TABLE `contractors_problems`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT для таблицы `executive_authority`
--
ALTER TABLE `executive_authority`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT для таблицы `mailing_queue`
--
ALTER TABLE `mailing_queue`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `news`
--
ALTER TABLE `news`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `problem_categories`
--
ALTER TABLE `problem_categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT для таблицы `regions`
--
ALTER TABLE `regions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `saved_coord`
--
ALTER TABLE `saved_coord`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `token_blocklist`
--
ALTER TABLE `token_blocklist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT для таблицы `user_profiles`
--
ALTER TABLE `user_profiles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `admin_applications`
--
ALTER TABLE `admin_applications`
  ADD CONSTRAINT `admin_applications_ibfk_1` FOREIGN KEY (`application_id`) REFERENCES `applications` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `admin_applications_ibfk_2` FOREIGN KEY (`administration_id`) REFERENCES `executive_authority` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `applications`
--
ALTER TABLE `applications`
  ADD CONSTRAINT `applications_ibfk_1` FOREIGN KEY (`status_id`) REFERENCES `application_status` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `applications_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `applications_ibfk_3` FOREIGN KEY (`moderator_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `applications_ibfk_4` FOREIGN KEY (`redirect_to_application_id`) REFERENCES `applications` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `applications_categories`
--
ALTER TABLE `applications_categories`
  ADD CONSTRAINT `applications_categories_ibfk_1` FOREIGN KEY (`application_id`) REFERENCES `applications` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `applications_categories_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `problem_categories` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `contractors_problems`
--
ALTER TABLE `contractors_problems`
  ADD CONSTRAINT `contractors_problems_ibfk_1` FOREIGN KEY (`contractor_id`) REFERENCES `executive_authority` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `contractors_problems_ibfk_2` FOREIGN KEY (`problem_id`) REFERENCES `problem_categories` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `mailing_queue`
--
ALTER TABLE `mailing_queue`
  ADD CONSTRAINT `mailing_queue_ibfk_1` FOREIGN KEY (`application_id`) REFERENCES `applications` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `news`
--
ALTER TABLE `news`
  ADD CONSTRAINT `news_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `saved_coord`
--
ALTER TABLE `saved_coord`
  ADD CONSTRAINT `saved_coord_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `user_profiles`
--
ALTER TABLE `user_profiles`
  ADD CONSTRAINT `user_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
