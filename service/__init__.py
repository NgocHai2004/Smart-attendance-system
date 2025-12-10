"""
Service module - Các repository để trích xuất và quản lý dữ liệu từ MySQL database
"""

from service.db_connection import db, DatabaseConnection
from service.students import StudentsRepository
from service.teachers import TeachersRepository
from service.classes import ClassesRepository
from service.face_embeddings import FaceEmbeddingsRepository
from service.cameras import CamerasRepository
from service.attendance import AttendanceRepository

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

