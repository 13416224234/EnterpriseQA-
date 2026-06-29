-- ===================================================
-- 企业知识库问答系统 - 数据库建表脚本
-- ===================================================

CREATE DATABASE IF NOT EXISTS db_enterprise_qa DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE db_enterprise_qa;

-- 用户表：存储管理员和普通用户信息
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '用户ID，主键',
    `username` VARCHAR(50) NOT NULL COMMENT '用户名',
    `password` VARCHAR(255) NOT NULL COMMENT 'MD5加密后的密码',
    `email` VARCHAR(100) DEFAULT NULL COMMENT '邮箱地址',
    `real_name` VARCHAR(50) DEFAULT NULL COMMENT '真实姓名',
    `role` ENUM('admin', 'user') NOT NULL DEFAULT 'user' COMMENT '角色：admin=管理员, user=普通用户',
    `avatar` VARCHAR(255) DEFAULT NULL COMMENT '头像URL',
    `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态：1=正常, 0=禁用',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_username` (`username`),
    KEY `idx_role` (`role`),
    KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 知识分类表：用于对文档进行分类管理
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '分类ID，主键',
    `name` VARCHAR(100) NOT NULL COMMENT '分类名称',
    `description` VARCHAR(500) DEFAULT NULL COMMENT '分类描述',
    `parent_id` INT DEFAULT NULL COMMENT '父分类ID，支持层级分类',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `idx_parent_id` (`parent_id`),
    CONSTRAINT `fk_category_parent` FOREIGN KEY (`parent_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='知识分类表';

-- 文档表：存储上传的知识文档信息
DROP TABLE IF EXISTS `documents`;
CREATE TABLE `documents` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '文档ID，主键',
    `title` VARCHAR(255) NOT NULL COMMENT '文档标题',
    `content` LONGTEXT COMMENT '文档原始文本内容',
    `file_path` VARCHAR(500) DEFAULT NULL COMMENT '文件存储路径',
    `file_type` VARCHAR(50) DEFAULT NULL COMMENT '文件类型：pdf/txt/docx/md等',
    `file_size` BIGINT DEFAULT 0 COMMENT '文件大小（字节）',
    `category_id` INT DEFAULT NULL COMMENT '所属分类ID',
    `uploaded_by` INT NOT NULL COMMENT '上传者用户ID',
    `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态：1=已导入, 0=待导入, -1=导入失败',
    `chunk_status` TINYINT NOT NULL DEFAULT 0 COMMENT '分片状态：0=未处理, 1=已分片, 2=已向量化',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_category` (`category_id`),
    KEY `idx_uploaded_by` (`uploaded_by`),
    KEY `idx_status` (`status`),
    CONSTRAINT `fk_doc_category` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_doc_uploader` FOREIGN KEY (`uploaded_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文档表';

-- 对话表：存储用户的问答会话
DROP TABLE IF EXISTS `conversations`;
CREATE TABLE `conversations` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '对话ID，主键',
    `user_id` INT NOT NULL COMMENT '所属用户ID',
    `title` VARCHAR(255) NOT NULL DEFAULT '新对话' COMMENT '对话标题',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_user_id` (`user_id`),
    CONSTRAINT `fk_conv_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='对话表';

-- 消息表：存储对话中的每一条消息
DROP TABLE IF EXISTS `messages`;
CREATE TABLE `messages` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '消息ID，主键',
    `conversation_id` INT NOT NULL COMMENT '所属对话ID',
    `role` ENUM('user', 'assistant') NOT NULL COMMENT '角色：user=用户, assistant=AI助手',
    `content` LONGTEXT NOT NULL COMMENT '消息内容',
    `sources` TEXT DEFAULT NULL COMMENT '引用的文档来源（JSON格式）',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `idx_conversation` (`conversation_id`),
    CONSTRAINT `fk_msg_conversation` FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='消息表';
