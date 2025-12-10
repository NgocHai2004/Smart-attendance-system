"""
Script để khởi tạo database với dữ liệu mẫu
Chạy file này sau khi đã chạy database/create_database.py
"""

import sys
import os
from datetime import date, datetime, timedelta
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Thêm thư mục gốc của project vào path để tìm module service
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from service import db, StudentsRepository, TeachersRepository, ClassesRepository, FaceEmbeddingsRepository, CamerasRepository, AttendanceRepository

def create_sample_data():
    """Tạo dữ liệu mẫu"""
    print("=" * 60)
    print("KHỞI TẠO DỮ LIỆU MẪU")
    print("=" * 60)
    
    # Kết nối database
    if not db.connect():
        print("✗ Không thể kết nối database!")
        print("\nHãy chạy database/create_database.py trước!")
        return False
    
    try:
        # ===========================================================
        # 1. Tạo giáo viên
        # ===========================================================
        print("\n1. Tạo giáo viên...")
        teacher1_id = TeachersRepository.create_teacher(
            full_name="Nguyễn Văn A",
            email="nguyenvana@example.com",
            phone="0123456789"
        )
        print(f"   ✓ Đã tạo giáo viên ID: {teacher1_id}")
        
        teacher2_id = TeachersRepository.create_teacher(
            full_name="Trần Thị B",
            email="tranthib@example.com",
            phone="0987654321"
        )
        print(f"   ✓ Đã tạo giáo viên ID: {teacher2_id}")
        
        # ===========================================================
        # 2. Tạo lớp học
        # ===========================================================
        print("\n2. Tạo lớp học...")
        class1_id = ClassesRepository.create_class(
            class_name="Lớp 10A1",
            teacher_id=teacher1_id
        )
        print(f"   ✓ Đã tạo lớp ID: {class1_id} - Lớp 10A1")
        
        class2_id = ClassesRepository.create_class(
            class_name="Lớp 10A2",
            teacher_id=teacher2_id
        )
        print(f"   ✓ Đã tạo lớp ID: {class2_id} - Lớp 10A2")
        
        # ===========================================================
        # 3. Tạo học sinh
        # ===========================================================
        print("\n3. Tạo học sinh...")
        students_data = [
            ("Nguyễn Văn An", "HS001", class1_id, date(2008, 5, 15), "male"),
            ("Trần Thị Bình", "HS002", class1_id, date(2008, 7, 20), "female"),
            ("Lê Văn Cường", "HS003", class1_id, date(2008, 3, 10), "male"),
            ("Phạm Thị Dung", "HS004", class2_id, date(2008, 9, 25), "female"),
            ("Hoàng Văn Em", "HS005", class2_id, date(2008, 11, 5), "male"),
        ]
        
        student_ids = []
        for name, code, cid, dob, gender in students_data:
            student_id = StudentsRepository.create_student(
                full_name=name,
                student_code=code,
                class_id=cid,
                date_of_birth=dob,
                gender=gender
            )
            student_ids.append(student_id)
            print(f"   ✓ Đã tạo học sinh ID: {student_id} - {name} ({code})")
        
        # ===========================================================
        # 4. Tạo face embeddings mẫu (dữ liệu giả)
        # ===========================================================
        print("\n4. Tạo face embeddings mẫu...")
        import random
        
        for student_id in student_ids:
            # Tạo embedding giả (512 chiều như InsightFace)
            fake_embedding = [random.random() for _ in range(512)]
            
            embedding_id = FaceEmbeddingsRepository.create_embedding(
                student_id=student_id,
                embedding=fake_embedding,
                image_url=f"data/images/student_{student_id}.jpg"
            )
            print(f"   ✓ Đã tạo embedding ID: {embedding_id} cho học sinh ID: {student_id}")
        
        # ===========================================================
        # 5. Tạo camera
        # ===========================================================
        print("\n5. Tạo camera...")
        camera1_id = CamerasRepository.create_camera(
            camera_name="Camera Lối vào chính",
            location="Cổng trường",
            ip_address="192.168.1.100"
        )
        print(f"   ✓ Đã tạo camera ID: {camera1_id}")
        
        camera2_id = CamerasRepository.create_camera(
            camera_name="Camera Phòng học A",
            location="Tầng 1 - Phòng A101",
            ip_address="192.168.1.101"
        )
        print(f"   ✓ Đã tạo camera ID: {camera2_id}")
        
        # ===========================================================
        # 6. Tạo điểm danh mẫu
        # ===========================================================
        print("\n6. Tạo điểm danh mẫu...")
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        # Điểm danh hôm qua
        for student_id in student_ids[:3]:  # 3 học sinh đầu
            AttendanceRepository.create_attendance(
                student_id=student_id,
                class_id=class1_id,
                session="morning",
                status="present",
                method="face_recognition",
                camera_id=camera1_id,
                timestamp=yesterday.replace(hour=7, minute=30)
            )
        
        # Điểm danh hôm nay
        for student_id in student_ids[:2]:  # 2 học sinh đầu
            AttendanceRepository.create_attendance(
                student_id=student_id,
                class_id=class1_id,
                session="morning",
                status="present",
                method="face_recognition",
                camera_id=camera1_id,
                timestamp=today.replace(hour=7, minute=25)
            )
        
        # Một học sinh đến muộn
        AttendanceRepository.create_attendance(
            student_id=student_ids[2],
            class_id=class1_id,
            session="morning",
            status="late",
            method="manual",
            note="Đến muộn 15 phút",
            timestamp=today.replace(hour=7, minute=45)
        )
        
        print(f"   ✓ Đã tạo {len(student_ids[:3]) + len(student_ids[:2]) + 1} bản ghi điểm danh")
        
        # ===========================================================
        # Hiển thị thống kê
        # ===========================================================
        print("\n" + "=" * 60)
        print("THỐNG KÊ DỮ LIỆU")
        print("=" * 60)
        
        all_teachers = TeachersRepository.get_all_teachers()
        all_classes = ClassesRepository.get_all_classes()
        all_students = StudentsRepository.get_all_students()
        all_cameras = CamerasRepository.get_all_cameras()
        all_attendance = AttendanceRepository.get_all_attendance()
        
        print(f"\nTổng số giáo viên: {len(all_teachers)}")
        print(f"Tổng số lớp học: {len(all_classes)}")
        print(f"Tổng số học sinh: {len(all_students)}")
        print(f"Tổng số camera: {len(all_cameras)}")
        print(f"Tổng số bản ghi điểm danh: {len(all_attendance)}")
        
        print("\n✓ Hoàn thành khởi tạo dữ liệu mẫu!")
        return True
        
    except Exception as e:
        print(f"\n✗ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        db.disconnect()

if __name__ == "__main__":
    success = create_sample_data()
    sys.exit(0 if success else 1)

