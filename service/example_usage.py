"""
Ví dụ sử dụng các repository để trích xuất dữ liệu từ database
"""

from service import (
    db,
    StudentsRepository,
    TeachersRepository,
    ClassesRepository,
    FaceEmbeddingsRepository,
    CamerasRepository,
    AttendanceRepository
)
from datetime import date, datetime

# Kết nối database
db.connect()

# ===========================================================
# Ví dụ với StudentsRepository
# ===========================================================

# Lấy tất cả học sinh
all_students = StudentsRepository.get_all_students()
print(f"Tổng số học sinh: {len(all_students)}")

# Lấy học sinh theo ID
student = StudentsRepository.get_student_by_id(1)
if student:
    print(f"Học sinh: {student['full_name']}, Mã: {student['student_code']}")

# Lấy học sinh theo lớp
class_students = StudentsRepository.get_students_by_class(class_id=1)
print(f"Số học sinh trong lớp: {len(class_students)}")

# Tìm kiếm học sinh
search_results = StudentsRepository.search_students("Nguyễn")
print(f"Kết quả tìm kiếm: {len(search_results)} học sinh")

# ===========================================================
# Ví dụ với TeachersRepository
# ===========================================================

# Lấy tất cả giáo viên
all_teachers = TeachersRepository.get_all_teachers()
print(f"Tổng số giáo viên: {len(all_teachers)}")

# Lấy lớp học của giáo viên
teacher_classes = TeachersRepository.get_teacher_classes(teacher_id=1)
print(f"Số lớp của giáo viên: {len(teacher_classes)}")

# ===========================================================
# Ví dụ với ClassesRepository
# ===========================================================

# Lấy tất cả lớp học
all_classes = ClassesRepository.get_all_classes()
print(f"Tổng số lớp: {len(all_classes)}")

# Lấy thông tin lớp kèm học sinh
class_info = ClassesRepository.get_class_with_students(class_id=1)
if class_info:
    print(f"Lớp: {class_info['class_name']}, Số học sinh: {class_info['student_count']}")

# ===========================================================
# Ví dụ với FaceEmbeddingsRepository
# ===========================================================

# Lấy embeddings của một học sinh
embeddings = FaceEmbeddingsRepository.get_embeddings_by_student(student_id=1)
print(f"Số embeddings của học sinh: {len(embeddings)}")

# Lấy embedding mới nhất
latest_embedding = FaceEmbeddingsRepository.get_latest_embedding_by_student(student_id=1)
if latest_embedding:
    print(f"Embedding mới nhất có {len(latest_embedding['embedding'])} chiều")

# ===========================================================
# Ví dụ với AttendanceRepository
# ===========================================================

# Lấy điểm danh của một lớp
attendance_records = AttendanceRepository.get_attendance_by_class(class_id=1)
print(f"Số bản ghi điểm danh: {len(attendance_records)}")

# Lấy điểm danh theo ngày
today = date.today()
today_attendance = AttendanceRepository.get_attendance_by_date(today)
print(f"Điểm danh hôm nay: {len(today_attendance)} bản ghi")

# Lấy thống kê điểm danh
stats = AttendanceRepository.get_attendance_statistics_by_class(class_id=1)
print(f"Thống kê: Có mặt: {stats['present_count']}, Vắng: {stats['absent_count']}")

# ===========================================================
# Ví dụ với CamerasRepository
# ===========================================================

# Lấy tất cả camera
all_cameras = CamerasRepository.get_all_cameras()
print(f"Tổng số camera: {len(all_cameras)}")

# Đóng kết nối
db.disconnect()

