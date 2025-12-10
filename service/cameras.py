from service.db_connection import db
from typing import List, Dict, Optional

class CamerasRepository:
    """Repository để trích xuất và quản lý dữ liệu camera"""
    
    @staticmethod
    def get_all_cameras() -> List[Dict]:
        """Lấy tất cả camera"""
        query = """
            SELECT 
                camera_id,
                camera_name,
                location,
                ip_address
            FROM cameras
            ORDER BY camera_name
        """
        return db.execute_query(query)
    
    @staticmethod
    def get_camera_by_id(camera_id: int) -> Optional[Dict]:
        """Lấy camera theo ID"""
        query = """
            SELECT 
                camera_id,
                camera_name,
                location,
                ip_address
            FROM cameras
            WHERE camera_id = %s
        """
        results = db.execute_query(query, (camera_id,))
        return results[0] if results else None
    
    @staticmethod
    def get_cameras_by_location(location: str) -> List[Dict]:
        """Lấy camera theo vị trí"""
        query = """
            SELECT 
                camera_id,
                camera_name,
                location,
                ip_address
            FROM cameras
            WHERE location LIKE %s
            ORDER BY camera_name
        """
        search_pattern = f"%{location}%"
        return db.execute_query(query, (search_pattern,))
    
    @staticmethod
    def search_cameras(keyword: str) -> List[Dict]:
        """Tìm kiếm camera theo tên hoặc vị trí"""
        query = """
            SELECT 
                camera_id,
                camera_name,
                location,
                ip_address
            FROM cameras
            WHERE camera_name LIKE %s OR location LIKE %s OR ip_address LIKE %s
            ORDER BY camera_name
        """
        search_pattern = f"%{keyword}%"
        return db.execute_query(query, (search_pattern, search_pattern, search_pattern))
    
    @staticmethod
    def create_camera(
        camera_name: str,
        location: str = None,
        ip_address: str = None
    ) -> int:
        """Tạo camera mới"""
        query = """
            INSERT INTO cameras (camera_name, location, ip_address)
            VALUES (%s, %s, %s)
        """
        params = (camera_name, location, ip_address)
        _, last_id = db.execute_update(query, params)
        return last_id
    
    @staticmethod
    def update_camera(
        camera_id: int,
        camera_name: str = None,
        location: str = None,
        ip_address: str = None
    ) -> bool:
        """Cập nhật thông tin camera"""
        updates = []
        params = []
        
        if camera_name:
            updates.append("camera_name = %s")
            params.append(camera_name)
        if location:
            updates.append("location = %s")
            params.append(location)
        if ip_address:
            updates.append("ip_address = %s")
            params.append(ip_address)
        
        if not updates:
            return False
        
        params.append(camera_id)
        query = f"UPDATE cameras SET {', '.join(updates)} WHERE camera_id = %s"
        affected_rows, _ = db.execute_update(query, tuple(params))
        return affected_rows > 0
    
    @staticmethod
    def delete_camera(camera_id: int) -> bool:
        """Xóa camera"""
        query = "DELETE FROM cameras WHERE camera_id = %s"
        affected_rows, _ = db.execute_update(query, (camera_id,))
        return affected_rows > 0
    
    @staticmethod
    def get_camera_statistics(camera_id: int) -> Dict:
        """Lấy thống kê camera (số lần điểm danh qua camera này)"""
        query = """
            SELECT 
                c.camera_id,
                c.camera_name,
                c.location,
                COUNT(a.attendance_id) as total_attendance_records
            FROM cameras c
            LEFT JOIN attendance a ON c.camera_id = a.camera_id
            WHERE c.camera_id = %s
            GROUP BY c.camera_id, c.camera_name, c.location
        """
        results = db.execute_query(query, (camera_id,))
        return results[0] if results else {
            'camera_id': camera_id,
            'total_attendance_records': 0
        }

