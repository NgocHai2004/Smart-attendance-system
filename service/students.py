from service.db_connection import db
from typing import List, Dict, Optional
from datetime import date

class StudentsRepository:
    """Repository để trích xuất và quản lý dữ liệu học sinh"""
    
    @staticmethod
    def get_all_students() -> List[Dict]:
        """Lấy tất cả học sinh"""
        query = """
            SELECT 
                student_id,
                full_name,
                date_of_birth,
                gender,
                student_code,
                class_id,
                avatar_url
            FROM students
            ORDER BY full_name
        """
        return db.execute_query(query)
    
    @staticmethod
    def get_student_by_id(student_id: int) -> Optional[Dict]:
        """Lấy học sinh theo ID"""
        query = """
            SELECT 
                student_id,
                full_name,
                date_of_birth,
                gender,
                student_code,
                class_id,
                avatar_url
            FROM students
            WHERE student_id = %s
        """
        results = db.execute_query(query, (student_id,))
        return results[0] if results else None
    
    @staticmethod
    def get_students_by_class(class_id: int) -> List[Dict]:
        """Lấy tất cả học sinh trong một lớp"""
        query = """
            SELECT 
                s.student_id,
                s.full_name,
                s.date_of_birth,
                s.gender,
                s.student_code,
                s.class_id,
                s.avatar_url,
                c.class_name
            FROM students s
            JOIN classes c ON s.class_id = c.class_id
            WHERE s.class_id = %s
            ORDER BY s.full_name
        """
        return db.execute_query(query, (class_id,))
    
    @staticmethod
    def get_student_by_code(student_code: str) -> Optional[Dict]:
        """Lấy học sinh theo mã học sinh"""
        query = """
            SELECT 
                student_id,
                full_name,
                date_of_birth,
                gender,
                student_code,
                class_id,
                avatar_url
            FROM students
            WHERE student_code = %s
        """
        results = db.execute_query(query, (student_code,))
        return results[0] if results else None
    
    @staticmethod
    def search_students(keyword: str) -> List[Dict]:
        """Tìm kiếm học sinh theo tên hoặc mã học sinh"""
        query = """
            SELECT 
                s.student_id,
                s.full_name,
                s.date_of_birth,
                s.gender,
                s.student_code,
                s.class_id,
                s.avatar_url,
                c.class_name
            FROM students s
            LEFT JOIN classes c ON s.class_id = c.class_id
            WHERE s.full_name LIKE %s OR s.student_code LIKE %s
            ORDER BY s.full_name
        """
        search_pattern = f"%{keyword}%"
        return db.execute_query(query, (search_pattern, search_pattern))
    
    @staticmethod
    def get_students_by_gender(gender: str) -> List[Dict]:
        """Lấy học sinh theo giới tính"""
        query = """
            SELECT 
                student_id,
                full_name,
                date_of_birth,
                gender,
                student_code,
                class_id,
                avatar_url
            FROM students
            WHERE gender = %s
            ORDER BY full_name
        """
        return db.execute_query(query, (gender,))
    
    @staticmethod
    def create_student(
        full_name: str,
        class_id: int,
        student_code: str = None,
        date_of_birth: date = None,
        gender: str = None,
        avatar_url: str = None
    ) -> int:
        """Tạo học sinh mới"""
        query = """
            INSERT INTO students 
            (full_name, date_of_birth, gender, student_code, class_id, avatar_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (full_name, date_of_birth, gender, student_code, class_id, avatar_url)
        _, last_id = db.execute_update(query, params)
        return last_id
    
    @staticmethod
    def update_student(
        student_id: int,
        full_name: str = None,
        date_of_birth: date = None,
        gender: str = None,
        student_code: str = None,
        class_id: int = None,
        avatar_url: str = None
    ) -> bool:
        """Cập nhật thông tin học sinh"""
        updates = []
        params = []
        
        if full_name:
            updates.append("full_name = %s")
            params.append(full_name)
        if date_of_birth:
            updates.append("date_of_birth = %s")
            params.append(date_of_birth)
        if gender:
            updates.append("gender = %s")
            params.append(gender)
        if student_code:
            updates.append("student_code = %s")
            params.append(student_code)
        if class_id:
            updates.append("class_id = %s")
            params.append(class_id)
        if avatar_url:
            updates.append("avatar_url = %s")
            params.append(avatar_url)
        
        if not updates:
            return False
        
        params.append(student_id)
        query = f"UPDATE students SET {', '.join(updates)} WHERE student_id = %s"
        affected_rows, _ = db.execute_update(query, tuple(params))
        return affected_rows > 0
    
    @staticmethod
    def delete_student(student_id: int) -> bool:
        """Xóa học sinh"""
        query = "DELETE FROM students WHERE student_id = %s"
        affected_rows, _ = db.execute_update(query, (student_id,))
        return affected_rows > 0
    
    @staticmethod
    def get_student_count_by_class() -> List[Dict]:
        """Đếm số học sinh theo từng lớp"""
        query = """
            SELECT 
                c.class_id,
                c.class_name,
                COUNT(s.student_id) as student_count
            FROM classes c
            LEFT JOIN students s ON c.class_id = s.class_id
            GROUP BY c.class_id, c.class_name
            ORDER BY c.class_name
        """
        return db.execute_query(query)

