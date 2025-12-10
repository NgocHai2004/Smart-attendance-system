"""
Script để tạo database và các bảng
Tất cả SQL đã được tích hợp sẵn trong file này
"""

import mysql.connector
from mysql.connector import Error
import os
import sys
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# SQL script để tạo database và các bảng
SQL_SCRIPT = """
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
    student_code VARCHAR(20) UNIQUE,
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
    embedding_json LONGTEXT NOT NULL,
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
"""

def execute_sql_file(connection, sql_content: str):
    """Thực thi SQL từ string"""
    try:
        cursor = connection.cursor()
        
        # Tách các câu lệnh SQL (tách theo dấu ;)
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        for statement in statements:
            if statement:
                try:
                    cursor.execute(statement)
                    print(f"✓ Đã thực thi: {statement[:50]}...")
                except Error as e:
                    # Bỏ qua lỗi nếu bảng đã tồn tại
                    if "already exists" in str(e).lower() or "Duplicate" in str(e):
                        print(f"⚠ Bỏ qua (đã tồn tại): {statement[:50]}...")
                    else:
                        print(f"✗ Lỗi: {e}")
                        print(f"  Câu lệnh: {statement[:100]}")
        
        connection.commit()
        cursor.close()
        print("\n✓ Đã tạo database và các bảng thành công!")
        
    except Error as e:
        print(f"✗ Lỗi thực thi SQL: {e}")
        connection.rollback()
        sys.exit(1)

def main():
    """Hàm chính"""
    # Cấu hình kết nối
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci'
    }
    
    print("=" * 60)
    print("TẠO DATABASE VÀ CÁC BẢNG")
    print("=" * 60)
    print(f"Host: {config['host']}")
    print(f"User: {config['user']}")
    print(f"Database: {os.getenv('DB_NAME', 'ai_attendance')}")
    print()
    
    # Kết nối và thực thi
    connection = None
    try:
        print("\nĐang kết nối đến MySQL server...")
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            print("✓ Kết nối thành công!\n")
            print("Đang tạo database và các bảng...")
            execute_sql_file(connection, SQL_SCRIPT)
        else:
            print("✗ Không thể kết nối đến MySQL server")
            sys.exit(1)
            
    except Error as e:
        print(f"✗ Lỗi kết nối: {e}")
        print("\nHãy kiểm tra:")
        print("1. MySQL server đã được cài đặt và đang chạy")
        print("2. Thông tin kết nối trong biến môi trường hoặc sửa trong file này")
        sys.exit(1)
        
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("\nĐã đóng kết nối.")

if __name__ == "__main__":
    main()

