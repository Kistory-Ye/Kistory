import json
import datetime
from app.student import StudentUser
from app.teacher import TeacherUser, Course

class ScheduleManager:
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []
        self._load_data()

    def _load_data(self):
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
            self.students.clear()
            for s_dict in data.get("students", []):
                stu = StudentUser(s_dict["id"], s_dict["name"])
                stu.enrolled_course_ids = s_dict.get("enrolled_course_ids", [])
                self.students.append(stu)

            self.teachers.clear()
            for t_dict in data.get("teachers", []):
                tea = TeacherUser(t_dict["id"], t_dict["name"], t_dict["speciality"])
                self.teachers.append(tea)

            self.courses.clear()
            for c_dict in data.get("courses", []):
                cou = Course(c_dict["id"], c_dict["name"], c_dict["instrument"], c_dict["teacher_id"])
                cou.enrolled_student_ids = c_dict.get("enrolled_student_ids", [])
                cou.lessons = c_dict.get("lessons", [])
                self.courses.append(cou)

            self.attendance_log = data.get("attendance", [])
            print("Loaded data successfully")
        except FileNotFoundError:
            print("Warning: json file not found, empty data")

    def _save_data(self):
        output = {
            "students": [{"id": s.id, "name": s.name, "enrolled_course_ids": s.enrolled_course_ids} for s in self.students],
            "teachers": [{"id": t.id, "name": t.name, "speciality": t.speciality} for t in self.teachers],
            "courses": [
                {
                    "id": c.id,
                    "name": c.name,
                    "instrument": c.instrument,
                    "teacher_id": c.teacher_id,
                    "enrolled_student_ids": c.enrolled_student_ids,
                    "lessons": c.lessons
                }
                for c in self.courses
            ],
            "attendance": self.attendance_log
        }
        with open(self.data_path, "w") as f:
            json.dump(output, f, indent=4)

    def find_student_by_id(self, student_id):
        for s in self.students:
            if s.id == student_id:
                return s
        return None

    def find_course_by_id(self, course_id):
        for c in self.courses:
            if c.id == course_id:
                return c
        return None

    def check_in(self, student_id, course_id):
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)
        if student is None or course is None:
            print("Error: Check‑in failed. Invalid Student or Course ID.")
            return False
        timestamp = datetime.datetime.now().isoformat()
        record = {"student_id": student_id, "course_id": course_id, "timestamp": timestamp}
        self.attendance_log.append(record)
        self._save_data()
        print(f"Success: Student {student.name} checked into {course.name}.")
        return True

    def get_lessons_for_day(self, day_name):
        result = []
        for course in self.courses:
            for lesson in course.lessons:
                if lesson["day"].lower() == day_name.lower():
                    result.append({"course": course, "lesson": lesson})
        return result