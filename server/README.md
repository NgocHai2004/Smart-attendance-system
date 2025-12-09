# Server Module - MySQL Database Repositories

Thư mục này chứa các repository để trích xuất và quản lý dữ liệu từ MySQL database theo schema trong `database.sql`.

## Cấu trúc

- `db_connection.py` - Quản lý kết nối MySQL database
- `students.py` - Repository cho bảng học sinh (students)
- `teachers.py` - Repository cho bảng giáo viên (teachers)
- `classes.py` - Repository cho bảng lớp học (classes)
- `face_embeddings.py` - Repository cho bảng face embeddings
- `cameras.py` - Repository cho bảng camera
- `attendance.py` - Repository cho bảng điểm danh (attendance)
- `example_usage.py` - Ví dụ sử dụng các repository

## Cài đặt

1. Cài đặt dependencies:
```bash
pip install mysql-connector-python
```

2. Cấu hình biến môi trường (hoặc sửa trong `db_connection.py`):
```bash
export DB_HOST=localhost
export DB_NAME=ai_attendance
export DB_USER=root
export DB_PASSWORD=your_password
```

## Sử dụng

### Kết nối database

```python
from server import db

# Kết nối
db.connect()

# Sử dụng các repository...

# Đóng kết nối khi xong
db.disconnect()
```

### Ví dụ với StudentsRepository

```python
from server import StudentsRepository

# Lấy tất cả học sinh
all_students = StudentsRepository.get_all_students()

# Lấy học sinh theo ID
student = StudentsRepository.get_student_by_id(1)

# Lấy học sinh theo lớp
class_students = StudentsRepository.get_students_by_class(class_id=1)

# Tìm kiếm học sinh
results = StudentsRepository.search_students("Nguyễn")

# Tạo học sinh mới
student_id = StudentsRepository.create_student(
    full_name="Nguyễn Văn A",
    class_id=1,
    student_code="HS001",
    gender="male"
)
```

### Ví dụ với AttendanceRepository

```python
from server import AttendanceRepository
from datetime import date, datetime

# Lấy điểm danh của một lớp
attendance = AttendanceRepository.get_attendance_by_class(class_id=1)

# Lấy điểm danh theo ngày
today_attendance = AttendanceRepository.get_attendance_by_date(date.today())

# Tạo bản ghi điểm danh
attendance_id = AttendanceRepository.create_attendance(
    student_id=1,
    class_id=1,
    session="morning",
    status="present",
    method="face_recognition",
    camera_id=1
)

# Lấy thống kê điểm danh
stats = AttendanceRepository.get_attendance_statistics_by_class(class_id=1)
```

## Các phương thức chính

### StudentsRepository
- `get_all_students()` - Lấy tất cả học sinh
- `get_student_by_id(student_id)` - Lấy học sinh theo ID
- `get_students_by_class(class_id)` - Lấy học sinh theo lớp
- `get_student_by_code(student_code)` - Lấy học sinh theo mã
- `search_students(keyword)` - Tìm kiếm học sinh
- `create_student(...)` - Tạo học sinh mới
- `update_student(...)` - Cập nhật học sinh
- `delete_student(student_id)` - Xóa học sinh

### TeachersRepository
- `get_all_teachers()` - Lấy tất cả giáo viên
- `get_teacher_by_id(teacher_id)` - Lấy giáo viên theo ID
- `get_teacher_by_email(email)` - Lấy giáo viên theo email
- `get_teacher_classes(teacher_id)` - Lấy lớp học của giáo viên
- `create_teacher(...)` - Tạo giáo viên mới
- `update_teacher(...)` - Cập nhật giáo viên

### ClassesRepository
- `get_all_classes()` - Lấy tất cả lớp học
- `get_class_by_id(class_id)` - Lấy lớp học theo ID
- `get_classes_by_teacher(teacher_id)` - Lấy lớp học theo giáo viên
- `get_class_students(class_id)` - Lấy học sinh trong lớp
- `get_class_with_students(class_id)` - Lấy lớp kèm danh sách học sinh
- `create_class(...)` - Tạo lớp học mới

### FaceEmbeddingsRepository
- `get_all_embeddings()` - Lấy tất cả embeddings
- `get_embeddings_by_student(student_id)` - Lấy embeddings của học sinh
- `get_latest_embedding_by_student(student_id)` - Lấy embedding mới nhất
- `get_embeddings_by_class(class_id)` - Lấy embeddings theo lớp
- `create_embedding(...)` - Tạo embedding mới

### CamerasRepository
- `get_all_cameras()` - Lấy tất cả camera
- `get_camera_by_id(camera_id)` - Lấy camera theo ID
- `get_cameras_by_location(location)` - Lấy camera theo vị trí
- `create_camera(...)` - Tạo camera mới

### AttendanceRepository
- `get_all_attendance()` - Lấy tất cả điểm danh
- `get_attendance_by_student(student_id)` - Lấy điểm danh của học sinh
- `get_attendance_by_class(class_id)` - Lấy điểm danh của lớp
- `get_attendance_by_date(date)` - Lấy điểm danh theo ngày
- `get_attendance_by_status(status)` - Lấy điểm danh theo trạng thái
- `create_attendance(...)` - Tạo bản ghi điểm danh
- `get_attendance_statistics_by_class(...)` - Lấy thống kê điểm danh

## Lưu ý

- Tất cả các phương thức trả về danh sách hoặc dictionary
- Các phương thức `create_*` trả về ID của bản ghi mới được tạo
- Các phương thức `update_*` và `delete_*` trả về `True` nếu thành công
- Nhớ đóng kết nối database sau khi sử dụng xong

