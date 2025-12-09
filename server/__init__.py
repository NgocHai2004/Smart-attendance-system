"""
Server module - Các repository để trích xuất và quản lý dữ liệu từ MySQL database
"""

from server.db_connection import db, DatabaseConnection
from server.students import StudentsRepository
from server.teachers import TeachersRepository
from server.classes import ClassesRepository
from server.face_embeddings import FaceEmbeddingsRepository
from server.cameras import CamerasRepository
from server.attendance import AttendanceRepository

__all__ = [
    'db',
    'DatabaseConnection',
    'StudentsRepository',
    'TeachersRepository',
    'ClassesRepository',
    'FaceEmbeddingsRepository',
    'CamerasRepository',
    'AttendanceRepository'
]

