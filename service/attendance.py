from service.db_connection import db
from typing import List, Dict, Optional
from datetime import datetime, date

class AttendanceRepository:
    """Repository để trích xuất và quản lý dữ liệu điểm danh"""
    
    @staticmethod
    def get_all_attendance() -> List[Dict]:
        """Lấy tất cả bản ghi điểm danh"""
        query = """
            SELECT 
                a.attendance_id,
                a.student_id,
                a.class_id,
                a.timestamp,
                a.session,
                a.status,
                a.method,
                a.camera_id,
                a.note,
                s.full_name as student_name,
                s.student_code,
                c.class_name,
                cam.camera_name,
                cam.location as camera_location
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            JOIN classes c ON a.class_id = c.class_id
            LEFT JOIN cameras cam ON a.camera_id = cam.camera_id
            ORDER BY a.timestamp DESC
        """
        return db.execute_query(query)
    
    @staticmethod
    def get_attendance_by_id(attendance_id: int) -> Optional[Dict]:
        """Lấy bản ghi điểm danh theo ID"""
        query = """
            SELECT 
                a.attendance_id,
                a.student_id,
                a.class_id,
                a.timestamp,
                a.session,
                a.status,
                a.method,
                a.camera_id,
                a.note,
                s.full_name as student_name,
                s.student_code,
                c.class_name,
                cam.camera_name,
                cam.location as camera_location
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            JOIN classes c ON a.class_id = c.class_id
            LEFT JOIN cameras cam ON a.camera_id = cam.camera_id
            WHERE a.attendance_id = %s
        """
        results = db.execute_query(query, (attendance_id,))
        return results[0] if results else None
    
    @staticmethod
    def get_attendance_by_student(student_id: int) -> List[Dict]:
        """Lấy tất cả điểm danh của một học sinh"""
        query = """
            SELECT 
                a.attendance_id,
                a.student_id,
                a.class_id,
                a.timestamp,
                a.session,
                a.status,
                a.method,
                a.camera_id,
                a.note,
                s.full_name as student_name,
                s.student_code,
                c.class_name,
                cam.camera_name
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            JOIN classes c ON a.class_id = c.class_id
            LEFT JOIN cameras cam ON a.camera_id = cam.camera_id
            WHERE a.student_id = %s
            ORDER BY a.timestamp DESC
        """
        return db.execute_query(query, (student_id,))
    
    @staticmethod
    def get_attendance_by_class(class_id: int) -> List[Dict]:
        """Lấy tất cả điểm danh của một lớp"""
        query = """
            SELECT 
                a.attendance_id,
                a.student_id,
                a.class_id,
                a.timestamp,
                a.session,
                a.status,
                a.method,
                a.camera_id,
                a.note,
                s.full_name as student_name,
                s.student_code,
                c.class_name,
                cam.camera_name
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            JOIN classes c ON a.class_id = c.class_id
            LEFT JOIN cameras cam ON a.camera_id = cam.camera_id
            WHERE a.class_id = %s
            ORDER BY a.timestamp DESC
        """
        return db.execute_query(query, (class_id,))
    
    @staticmethod
    def get_attendance_by_date(attendance_date: date) -> List[Dict]:
        """Lấy điểm danh theo ngày"""
        query = """
            SELECT 
                a.attendance_id,
                a.student_id,
                a.class_id,
                a.timestamp,
                a.session,
                a.status,
                a.method,
                a.camera_id,
                a.note,
                s.full_name as student_name,
                s.student_code,
                c.class_name,
                cam.camera_name
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            JOIN classes c ON a.class_id = c.class_id
            LEFT JOIN cameras cam ON a.camera_id = cam.camera_id
            WHERE DATE(a.timestamp) = %s
            ORDER BY a.timestamp DESC
        """
        return db.execute_query(query, (attendance_date,))
    
    @staticmethod
    def get_attendance_by_class_and_date(class_id: int, attendance_date: date) -> List[Dict]:
        """Lấy điểm danh của một lớp trong một ngày"""
        query = """
            SELECT 
                a.attendance_id,
                a.student_id,
                a.class_id,
                a.timestamp,
                a.session,
                a.status,
                a.method,
                a.camera_id,
                a.note,
                s.full_name as student_name,
                s.student_code,
                c.class_name,
                cam.camera_name
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            JOIN classes c ON a.class_id = c.class_id
            LEFT JOIN cameras cam ON a.camera_id = cam.camera_id
            WHERE a.class_id = %s AND DATE(a.timestamp) = %s
            ORDER BY a.timestamp DESC
        """
        return db.execute_query(query, (class_id, attendance_date))
    
    @staticmethod
    def get_attendance_by_status(status: str) -> List[Dict]:
        """Lấy điểm danh theo trạng thái (present, absent, late, excused)"""
        query = """
            SELECT 
                a.attendance_id,
                a.student_id,
                a.class_id,
                a.timestamp,
                a.session,
                a.status,
                a.method,
                a.camera_id,
                a.note,
                s.full_name as student_name,
                s.student_code,
                c.class_name,
                cam.camera_name
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            JOIN classes c ON a.class_id = c.class_id
            LEFT JOIN cameras cam ON a.camera_id = cam.camera_id
            WHERE a.status = %s
            ORDER BY a.timestamp DESC
        """
        return db.execute_query(query, (status,))
    
    @staticmethod
    def get_attendance_by_session(session: str) -> List[Dict]:
        """Lấy điểm danh theo ca học (morning, afternoon, evening)"""
        query = """
            SELECT 
                a.attendance_id,
                a.student_id,
                a.class_id,
                a.timestamp,
                a.session,
                a.status,
                a.method,
                a.camera_id,
                a.note,
                s.full_name as student_name,
                s.student_code,
                c.class_name,
                cam.camera_name
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            JOIN classes c ON a.class_id = c.class_id
            LEFT JOIN cameras cam ON a.camera_id = cam.camera_id
            WHERE a.session = %s
            ORDER BY a.timestamp DESC
        """
        return db.execute_query(query, (session,))
    
    @staticmethod
    def create_attendance(
        student_id: int,
        class_id: int,
        session: str,
        status: str,
        method: str = 'face_recognition',
        camera_id: int = None,
        note: str = None,
        timestamp: datetime = None
    ) -> int:
        """Tạo bản ghi điểm danh mới"""
        if timestamp is None:
            timestamp = datetime.now()
        
        query = """
            INSERT INTO attendance 
            (student_id, class_id, timestamp, session, status, method, camera_id, note)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (student_id, class_id, timestamp, session, status, method, camera_id, note)
        _, last_id = db.execute_update(query, params)
        return last_id
    
    @staticmethod
    def update_attendance(
        attendance_id: int,
        status: str = None,
        session: str = None,
        note: str = None
    ) -> bool:
        """Cập nhật bản ghi điểm danh"""
        updates = []
        params = []
        
        if status:
            updates.append("status = %s")
            params.append(status)
        if session:
            updates.append("session = %s")
            params.append(session)
        if note:
            updates.append("note = %s")
            params.append(note)
        
        if not updates:
            return False
        
        params.append(attendance_id)
        query = f"UPDATE attendance SET {', '.join(updates)} WHERE attendance_id = %s"
        affected_rows, _ = db.execute_update(query, tuple(params))
        return affected_rows > 0
    
    @staticmethod
    def delete_attendance(attendance_id: int) -> bool:
        """Xóa bản ghi điểm danh"""
        query = "DELETE FROM attendance WHERE attendance_id = %s"
        affected_rows, _ = db.execute_update(query, (attendance_id,))
        return affected_rows > 0
    
    @staticmethod
    def get_attendance_statistics_by_class(class_id: int, start_date: date = None, end_date: date = None) -> Dict:
        """Lấy thống kê điểm danh của một lớp"""
        if start_date and end_date:
            query = """
                SELECT 
                    COUNT(*) as total_records,
                    SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present_count,
                    SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent_count,
                    SUM(CASE WHEN status = 'late' THEN 1 ELSE 0 END) as late_count,
                    SUM(CASE WHEN status = 'excused' THEN 1 ELSE 0 END) as excused_count
                FROM attendance
                WHERE class_id = %s 
                AND DATE(timestamp) BETWEEN %s AND %s
            """
            params = (class_id, start_date, end_date)
        else:
            query = """
                SELECT 
                    COUNT(*) as total_records,
                    SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present_count,
                    SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent_count,
                    SUM(CASE WHEN status = 'late' THEN 1 ELSE 0 END) as late_count,
                    SUM(CASE WHEN status = 'excused' THEN 1 ELSE 0 END) as excused_count
                FROM attendance
                WHERE class_id = %s
            """
            params = (class_id,)
        
        results = db.execute_query(query, params)
        return results[0] if results else {
            'total_records': 0,
            'present_count': 0,
            'absent_count': 0,
            'late_count': 0,
            'excused_count': 0
        }
    
    @staticmethod
    def get_student_attendance_summary(student_id: int, start_date: date = None, end_date: date = None) -> Dict:
        """Lấy tổng hợp điểm danh của một học sinh"""
        if start_date and end_date:
            query = """
                SELECT 
                    COUNT(*) as total_records,
                    SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present_count,
                    SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent_count,
                    SUM(CASE WHEN status = 'late' THEN 1 ELSE 0 END) as late_count,
                    SUM(CASE WHEN status = 'excused' THEN 1 ELSE 0 END) as excused_count
                FROM attendance
                WHERE student_id = %s 
                AND DATE(timestamp) BETWEEN %s AND %s
            """
            params = (student_id, start_date, end_date)
        else:
            query = """
                SELECT 
                    COUNT(*) as total_records,
                    SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present_count,
                    SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent_count,
                    SUM(CASE WHEN status = 'late' THEN 1 ELSE 0 END) as late_count,
                    SUM(CASE WHEN status = 'excused' THEN 1 ELSE 0 END) as excused_count
                FROM attendance
                WHERE student_id = %s
            """
            params = (student_id,)
        
        results = db.execute_query(query, params)
        return results[0] if results else {
            'total_records': 0,
            'present_count': 0,
            'absent_count': 0,
            'late_count': 0,
            'excused_count': 0
        }

