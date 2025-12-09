CREATE DATABASE IF NOT EXISTS ai_attendance
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE ai_attendance;

-- ===========================================================
-- 1. Bảng giáo viên (teachers)
-- ===========================================================

CREATE TABLE teachers (
    teacher_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20)
);

-- ===========================================================
-- 2. Bảng lớp học (classes)
-- ===========================================================

CREATE TABLE classes (
    class_id INT PRIMARY KEY AUTO_INCREMENT,
    class_name VARCHAR(50) NOT NULL,
    teacher_id INT NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

-- ===========================================================
-- 3. Bảng học sinh (students)
-- ===========================================================

CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    gender ENUM('male','female','other'),
    student_code VARCHAR(20) UNIQUE,   -- mã học sinh
    class_id INT NOT NULL,
    avatar_url VARCHAR(255),
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

-- ===========================================================
-- 4. Bảng lưu vector embedding từ InsightFace
-- ===========================================================

CREATE TABLE face_embeddings (
    embedding_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    embedding_json LONGTEXT NOT NULL,     -- chứa 512 số float
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- ===========================================================
-- 5. Bảng camera AI trong trường
-- ===========================================================

CREATE TABLE cameras (
    camera_id INT PRIMARY KEY AUTO_INCREMENT,
    camera_name VARCHAR(50),
    location VARCHAR(100),
    ip_address VARCHAR(50)
);

-- ===========================================================
-- 6. Bảng điểm danh
-- ===========================================================

CREATE TABLE attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    class_id INT NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    session ENUM('morning','afternoon','evening') NOT NULL,
    status ENUM('present','absent','late','excused') NOT NULL,
    method ENUM('face_recognition','manual') DEFAULT 'face_recognition',
    camera_id INT,
    note VARCHAR(255),

    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (class_id) REFERENCES classes(class_id),
    FOREIGN KEY (camera_id) REFERENCES cameras(camera_id),

    INDEX idx_attendance_student_date (student_id, timestamp)
);