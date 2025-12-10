"""
FastAPI Backend để lấy dữ liệu từ các bảng database
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
from datetime import date, datetime
import sys
import os
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()

# Thêm thư mục service vào path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from service import (
    db,
    StudentsRepository,
    TeachersRepository,
    ClassesRepository,
    FaceEmbeddingsRepository,
    CamerasRepository,
    AttendanceRepository
)

app = FastAPI(title="Attendance System API", version="1.0.0")

# Cấu hình CORS để cho phép React frontend kết nối
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Kết nối database khi khởi động
@app.on_event("startup")
async def startup_event():
    """Kết nối database khi khởi động"""
    db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """Đóng kết nối database khi tắt"""
    db.disconnect()

# ===========================================================
# Endpoints cho Teachers
# ===========================================================

@app.get("/api/teachers", response_model=List[Dict])
async def get_all_teachers():
    """Lấy tất cả giáo viên"""
    try:
        return TeachersRepository.get_all_teachers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/teachers/{teacher_id}", response_model=Dict)
async def get_teacher_by_id(teacher_id: int):
    """Lấy giáo viên theo ID"""
    teacher = TeachersRepository.get_teacher_by_id(teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@app.get("/api/teachers/{teacher_id}/classes", response_model=List[Dict])
async def get_teacher_classes(teacher_id: int):
    """Lấy các lớp học của giáo viên"""
    try:
        return TeachersRepository.get_teacher_classes(teacher_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===========================================================
# Endpoints cho Classes
# ===========================================================

@app.get("/api/classes", response_model=List[Dict])
async def get_all_classes():
    """Lấy tất cả lớp học"""
    try:
        return ClassesRepository.get_all_classes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/classes/{class_id}", response_model=Dict)
async def get_class_by_id(class_id: int):
    """Lấy lớp học theo ID"""
    class_info = ClassesRepository.get_class_by_id(class_id)
    if not class_info:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_info

@app.get("/api/classes/{class_id}/students", response_model=List[Dict])
async def get_class_students(class_id: int):
    """Lấy học sinh trong lớp"""
    try:
        return ClassesRepository.get_class_students(class_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/classes/{class_id}/full", response_model=Dict)
async def get_class_with_students(class_id: int):
    """Lấy lớp học kèm danh sách học sinh"""
    class_info = ClassesRepository.get_class_with_students(class_id)
    if not class_info:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_info

# ===========================================================
# Endpoints cho Students
# ===========================================================

@app.get("/api/students", response_model=List[Dict])
async def get_all_students():
    """Lấy tất cả học sinh"""
    try:
        return StudentsRepository.get_all_students()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/students/{student_id}", response_model=Dict)
async def get_student_by_id(student_id: int):
    """Lấy học sinh theo ID"""
    student = StudentsRepository.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.get("/api/students/class/{class_id}", response_model=List[Dict])
async def get_students_by_class(class_id: int):
    """Lấy học sinh theo lớp"""
    try:
        return StudentsRepository.get_students_by_class(class_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===========================================================
# Endpoints cho Face Embeddings
# ===========================================================

@app.get("/api/embeddings", response_model=List[Dict])
async def get_all_embeddings():
    """Lấy tất cả embeddings"""
    try:
        return FaceEmbeddingsRepository.get_all_embeddings()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/embeddings/student/{student_id}", response_model=List[Dict])
async def get_embeddings_by_student(student_id: int):
    """Lấy embeddings của học sinh"""
    try:
        return FaceEmbeddingsRepository.get_embeddings_by_student(student_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===========================================================
# Endpoints cho Cameras
# ===========================================================

@app.get("/api/cameras", response_model=List[Dict])
async def get_all_cameras():
    """Lấy tất cả camera"""
    try:
        return CamerasRepository.get_all_cameras()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cameras/{camera_id}", response_model=Dict)
async def get_camera_by_id(camera_id: int):
    """Lấy camera theo ID"""
    camera = CamerasRepository.get_camera_by_id(camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    return camera

# ===========================================================
# Endpoints cho Attendance
# ===========================================================

@app.get("/api/attendance", response_model=List[Dict])
async def get_all_attendance():
    """Lấy tất cả điểm danh"""
    try:
        return AttendanceRepository.get_all_attendance()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/attendance/student/{student_id}", response_model=List[Dict])
async def get_attendance_by_student(student_id: int):
    """Lấy điểm danh của học sinh"""
    try:
        return AttendanceRepository.get_attendance_by_student(student_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/attendance/class/{class_id}", response_model=List[Dict])
async def get_attendance_by_class(class_id: int):
    """Lấy điểm danh của lớp"""
    try:
        return AttendanceRepository.get_attendance_by_class(class_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/attendance/statistics/class/{class_id}", response_model=Dict)
async def get_attendance_statistics(class_id: int):
    """Lấy thống kê điểm danh của lớp"""
    try:
        return AttendanceRepository.get_attendance_statistics_by_class(class_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===========================================================
# Health check
# ===========================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Attendance System API", "status": "running"}

@app.get("/api/health")
async def health_check():
    """Health check với database"""
    try:
        if db.connection and db.connection.is_connected():
            return {"status": "healthy", "database": "connected"}
        else:
            return {"status": "unhealthy", "database": "disconnected"}
    except:
        return {"status": "unhealthy", "database": "error"}

