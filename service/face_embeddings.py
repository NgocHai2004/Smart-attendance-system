from service.db_connection import db
from typing import List, Dict, Optional
import json
from datetime import datetime

class FaceEmbeddingsRepository:
    """Repository để trích xuất và quản lý dữ liệu face embeddings"""
    
    @staticmethod
    def get_all_embeddings() -> List[Dict]:
        """Lấy tất cả embeddings"""
        query = """
            SELECT 
                e.embedding_id,
                e.student_id,
                e.embedding_json,
                e.image_url,
                e.created_at,
                s.full_name as student_name,
                s.student_code
            FROM face_embeddings e
            JOIN students s ON e.student_id = s.student_id
            ORDER BY e.created_at DESC
        """
        results = db.execute_query(query)
        # Parse JSON embedding
        for result in results:
            if result.get('embedding_json'):
                try:
                    result['embedding'] = json.loads(result['embedding_json'])
                except:
                    result['embedding'] = None
        return results
    
    @staticmethod
    def get_embedding_by_id(embedding_id: int) -> Optional[Dict]:
        """Lấy embedding theo ID"""
        query = """
            SELECT 
                e.embedding_id,
                e.student_id,
                e.embedding_json,
                e.image_url,
                e.created_at,
                s.full_name as student_name,
                s.student_code
            FROM face_embeddings e
            JOIN students s ON e.student_id = s.student_id
            WHERE e.embedding_id = %s
        """
        results = db.execute_query(query, (embedding_id,))
        if results:
            result = results[0]
            if result.get('embedding_json'):
                try:
                    result['embedding'] = json.loads(result['embedding_json'])
                except:
                    result['embedding'] = None
            return result
        return None
    
    @staticmethod
    def get_embeddings_by_student(student_id: int) -> List[Dict]:
        """Lấy tất cả embeddings của một học sinh"""
        query = """
            SELECT 
                e.embedding_id,
                e.student_id,
                e.embedding_json,
                e.image_url,
                e.created_at,
                s.full_name as student_name,
                s.student_code
            FROM face_embeddings e
            JOIN students s ON e.student_id = s.student_id
            WHERE e.student_id = %s
            ORDER BY e.created_at DESC
        """
        results = db.execute_query(query, (student_id,))
        # Parse JSON embedding
        for result in results:
            if result.get('embedding_json'):
                try:
                    result['embedding'] = json.loads(result['embedding_json'])
                except:
                    result['embedding'] = None
        return results
    
    @staticmethod
    def get_latest_embedding_by_student(student_id: int) -> Optional[Dict]:
        """Lấy embedding mới nhất của một học sinh"""
        query = """
            SELECT 
                e.embedding_id,
                e.student_id,
                e.embedding_json,
                e.image_url,
                e.created_at,
                s.full_name as student_name,
                s.student_code
            FROM face_embeddings e
            JOIN students s ON e.student_id = s.student_id
            WHERE e.student_id = %s
            ORDER BY e.created_at DESC
            LIMIT 1
        """
        results = db.execute_query(query, (student_id,))
        if results:
            result = results[0]
            if result.get('embedding_json'):
                try:
                    result['embedding'] = json.loads(result['embedding_json'])
                except:
                    result['embedding'] = None
            return result
        return None
    
    @staticmethod
    def create_embedding(
        student_id: int,
        embedding: List[float],
        image_url: str = None
    ) -> int:
        """Tạo embedding mới"""
        embedding_json = json.dumps(embedding)
        query = """
            INSERT INTO face_embeddings (student_id, embedding_json, image_url)
            VALUES (%s, %s, %s)
        """
        params = (student_id, embedding_json, image_url)
        _, last_id = db.execute_update(query, params)
        return last_id
    
    @staticmethod
    def update_embedding(
        embedding_id: int,
        embedding: List[float] = None,
        image_url: str = None
    ) -> bool:
        """Cập nhật embedding"""
        updates = []
        params = []
        
        if embedding:
            embedding_json = json.dumps(embedding)
            updates.append("embedding_json = %s")
            params.append(embedding_json)
        if image_url:
            updates.append("image_url = %s")
            params.append(image_url)
        
        if not updates:
            return False
        
        params.append(embedding_id)
        query = f"UPDATE face_embeddings SET {', '.join(updates)} WHERE embedding_id = %s"
        affected_rows, _ = db.execute_update(query, tuple(params))
        return affected_rows > 0
    
    @staticmethod
    def delete_embedding(embedding_id: int) -> bool:
        """Xóa embedding"""
        query = "DELETE FROM face_embeddings WHERE embedding_id = %s"
        affected_rows, _ = db.execute_update(query, (embedding_id,))
        return affected_rows > 0
    
    @staticmethod
    def get_all_embeddings_for_recognition() -> List[Dict]:
        """Lấy tất cả embeddings để nhận diện (chỉ lấy embedding mới nhất của mỗi học sinh)"""
        query = """
            SELECT 
                e.student_id,
                e.embedding_json,
                s.full_name as student_name,
                s.student_code,
                s.class_id
            FROM face_embeddings e
            JOIN students s ON e.student_id = s.student_id
            WHERE e.embedding_id IN (
                SELECT MAX(embedding_id)
                FROM face_embeddings
                GROUP BY student_id
            )
        """
        results = db.execute_query(query)
        # Parse JSON embedding
        for result in results:
            if result.get('embedding_json'):
                try:
                    result['embedding'] = json.loads(result['embedding_json'])
                except:
                    result['embedding'] = None
        return results
    
    @staticmethod
    def get_embeddings_by_class(class_id: int) -> List[Dict]:
        """Lấy tất cả embeddings của học sinh trong một lớp"""
        query = """
            SELECT 
                e.embedding_id,
                e.student_id,
                e.embedding_json,
                e.image_url,
                e.created_at,
                s.full_name as student_name,
                s.student_code,
                s.class_id
            FROM face_embeddings e
            JOIN students s ON e.student_id = s.student_id
            WHERE s.class_id = %s
            AND e.embedding_id IN (
                SELECT MAX(embedding_id)
                FROM face_embeddings fe
                JOIN students st ON fe.student_id = st.student_id
                WHERE st.class_id = %s
                GROUP BY fe.student_id
            )
            ORDER BY s.full_name
        """
        results = db.execute_query(query, (class_id, class_id))
        # Parse JSON embedding
        for result in results:
            if result.get('embedding_json'):
                try:
                    result['embedding'] = json.loads(result['embedding_json'])
                except:
                    result['embedding'] = None
        return results

