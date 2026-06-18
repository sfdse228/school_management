"""
models.py - Модели данных (Студент, Преподаватель, Курс)
"""

import uuid
from datetime import datetime
from typing import List, Dict, Optional, Any


class Student:
    """Модель студента"""
    
    def __init__(self, name: str, email: str, student_id: Optional[str] = None):
        self.id = student_id or str(uuid.uuid4())[:8]
        self.name = name
        self.email = email
        self.courses: List[str] = []  # ID курсов, на которые зачислен
        self.grades: Dict[str, List[int]] = {}  # {course_id: [grades]}
        self.completed_courses: List[str] = []  # ID завершённых курсов
        self.created_at = datetime.now().isoformat()
    
    def enroll(self, course_id: str):
        """Зачислить студента на курс"""
        if course_id not in self.courses:
            self.courses.append(course_id)
    
    def add_grade(self, course_id: str, grade: int):
        """Добавить оценку по курсу"""
        if course_id not in self.grades:
            self.grades[course_id] = []
        self.grades[course_id].append(grade)
    
    def complete_course(self, course_id: str):
        """Завершить курс"""
        if course_id in self.courses:
            self.courses.remove(course_id)
        if course_id not in self.completed_courses:
            self.completed_courses.append(course_id)
    
    def get_average_grade(self, course_id: Optional[str] = None) -> float:
        """Получить среднюю оценку"""
        if course_id:
            grades = self.grades.get(course_id, [])
            return sum(grades) / len(grades) if grades else 0.0
        
        # Средняя по всем курсам
        all_grades = []
        for grades in self.grades.values():
            all_grades.extend(grades)
        return sum(all_grades) / len(all_grades) if all_grades else 0.0
    
    def to_dict(self) -> Dict:
        """Преобразовать в словарь для JSON"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'courses': self.courses,
            'grades': self.grades,
            'completed_courses': self.completed_courses,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Student':
        """Создать студента из словаря"""
        student = cls(
            name=data['name'],
            email=data['email'],
            student_id=data.get('id')
        )
        student.courses = data.get('courses', [])
        student.grades = data.get('grades', {})
        student.completed_courses = data.get('completed_courses', [])
        student.created_at = data.get('created_at', datetime.now().isoformat())
        return student
    
    def __str__(self) -> str:
        return f"{self.name} ({self.email})"


class Teacher:
    """Модель преподавателя"""
    
    def __init__(self, name: str, specialization: str, teacher_id: Optional[str] = None):
        self.id = teacher_id or str(uuid.uuid4())[:8]
        self.name = name
        self.specialization = specialization
        self.courses: List[str] = []  # ID курсов, которые ведёт
        self.created_at = datetime.now().isoformat()
    
    def assign_course(self, course_id: str):
        """Назначить курс преподавателю"""
        if course_id not in self.courses:
            self.courses.append(course_id)
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'specialization': self.specialization,
            'courses': self.courses,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Teacher':
        teacher = cls(
            name=data['name'],
            specialization=data['specialization'],
            teacher_id=data.get('id')
        )
        teacher.courses = data.get('courses', [])
        teacher.created_at = data.get('created_at', datetime.now().isoformat())
        return teacher
    
    def __str__(self) -> str:
        return f"{self.name} ({self.specialization})"


class Course:
    """Модель курса"""
    
    STATUS_ACTIVE = "активен"
    STATUS_COMPLETED = "завершён"
    
    def __init__(
        self,
        name: str,
        topic: str,
        course_id: Optional[str] = None,
        teacher_id: Optional[str] = None,
        status: str = STATUS_ACTIVE
    ):
        self.id = course_id or str(uuid.uuid4())[:8]
        self.name = name
        self.topic = topic
        self.teacher_id = teacher_id
        self.status = status
        self.students: List[str] = []  # ID студентов
        self.grades: Dict[str, List[int]] = {}  # {student_id: [grades]}
        self.created_at = datetime.now().isoformat()
        self.completed_at = None
    
    def add_student(self, student_id: str):
        """Добавить студента на курс"""
        if student_id not in self.students:
            self.students.append(student_id)
    
    def remove_student(self, student_id: str):
        """Удалить студента с курса"""
        if student_id in self.students:
            self.students.remove(student_id)
    
    def assign_teacher(self, teacher_id: str):
        """Назначить преподавателя"""
        self.teacher_id = teacher_id
    
    def add_grade(self, student_id: str, grade: int):
        """Добавить оценку студенту"""
        if student_id not in self.grades:
            self.grades[student_id] = []
        self.grades[student_id].append(grade)
    
    def complete(self):
        """Завершить курс"""
        self.status = self.STATUS_COMPLETED
        self.completed_at = datetime.now().isoformat()
    
    def get_average_grade(self) -> float:
        """Средняя оценка по курсу"""
        all_grades = []
        for grades in self.grades.values():
            all_grades.extend(grades)
        return sum(all_grades) / len(all_grades) if all_grades else 0.0
    
    def get_student_grades(self, student_id: str) -> List[int]:
        """Получить оценки студента по курсу"""
        return self.grades.get(student_id, [])
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'topic': self.topic,
            'teacher_id': self.teacher_id,
            'status': self.status,
            'students': self.students,
            'grades': self.grades,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Course':
        course = cls(
            name=data['name'],
            topic=data['topic'],
            course_id=data.get('id'),
            teacher_id=data.get('teacher_id'),
            status=data.get('status', cls.STATUS_ACTIVE)
        )
        course.students = data.get('students', [])
        course.grades = data.get('grades', {})
        course.created_at = data.get('created_at', datetime.now().isoformat())
        course.completed_at = data.get('completed_at')
        return course
    
    def __str__(self) -> str:
        status_icon = "🟢" if self.status == self.STATUS_ACTIVE else "🔴"
        return f"{status_icon} {self.name} ({self.topic})"
