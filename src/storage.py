"""
storage.py - Централизованное хранилище и операции
"""

import json
import os
from typing import List, Optional, Dict, Tuple
from src.models import Student, Teacher, Course
from src.logger_setup import logger


class SchoolStorage:
    """Централизованное хранилище школы"""
    
    def __init__(self):
        self.students: Dict[str, Student] = {}
        self.teachers: Dict[str, Teacher] = {}
        self.courses: Dict[str, Course] = {}
        
        self.data_dir = "data"
        self._ensure_data_dir()
        self.load_all()
    
    def _ensure_data_dir(self):
        """Создаёт папку для данных"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    # ========== СОХРАНЕНИЕ ==========
    
    def save_all(self):
        """Сохраняет все данные в JSON"""
        self._save_students()
        self._save_teachers()
        self._save_courses()
        logger.info("Все данные сохранены")
    
    def _save_students(self):
        with open(f"{self.data_dir}/students.json", 'w', encoding='utf-8') as f:
            data = {sid: student.to_dict() for sid, student in self.students.items()}
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _save_teachers(self):
        with open(f"{self.data_dir}/teachers.json", 'w', encoding='utf-8') as f:
            data = {tid: teacher.to_dict() for tid, teacher in self.teachers.items()}
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _save_courses(self):
        with open(f"{self.data_dir}/courses.json", 'w', encoding='utf-8') as f:
            data = {cid: course.to_dict() for cid, course in self.courses.items()}
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ========== ЗАГРУЗКА ==========
    
    def load_all(self):
        """Загружает все данные из JSON"""
        self._load_students()
        self._load_teachers()
        self._load_courses()
        logger.info("Все данные загружены")
    
    def _load_students(self):
        filepath = f"{self.data_dir}/students.json"
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.students = {
                        sid: Student.from_dict(sdata)
                        for sid, sdata in data.items()
                    }
            except (json.JSONDecodeError, FileNotFoundError) as e:
                logger.error(f"Ошибка загрузки студентов: {e}")
                self.students = {}
    
    def _load_teachers(self):
        filepath = f"{self.data_dir}/teachers.json"
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.teachers = {
                        tid: Teacher.from_dict(tdata)
                        for tid, tdata in data.items()
                    }
            except (json.JSONDecodeError, FileNotFoundError) as e:
                logger.error(f"Ошибка загрузки преподавателей: {e}")
                self.teachers = {}
    
    def _load_courses(self):
        filepath = f"{self.data_dir}/courses.json"
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.courses = {
                        cid: Course.from_dict(cdata)
                        for cid, cdata in data.items()
                    }
            except (json.JSONDecodeError, FileNotFoundError) as e:
                logger.error(f"Ошибка загрузки курсов: {e}")
                self.courses = {}
    
    # ========== ОПЕРАЦИИ СО СТУДЕНТАМИ ==========
    
    def add_student(self, name: str, email: str) -> Student:
        """Добавить студента"""
        student = Student(name, email)
        self.students[student.id] = student
        self._save_students()
        logger.info(f"Добавлен студент: {name} ({email})")
        return student
    
    def get_student(self, student_id: str) -> Optional[Student]:
        return self.students.get(student_id)
    
    def get_all_students(self) -> List[Student]:
        return list(self.students.values())
    
    def find_student_by_email(self, email: str) -> Optional[Student]:
        for student in self.students.values():
            if student.email == email:
                return student
        return None
    
    # ========== ОПЕРАЦИИ С ПРЕПОДАВАТЕЛЯМИ ==========
    
    def add_teacher(self, name: str, specialization: str) -> Teacher:
        """Добавить преподавателя"""
        teacher = Teacher(name, specialization)
        self.teachers[teacher.id] = teacher
        self._save_teachers()
        logger.info(f"Добавлен преподаватель: {name} ({specialization})")
        return teacher
    
    def get_teacher(self, teacher_id: str) -> Optional[Teacher]:
        return self.teachers.get(teacher_id)
    
    def get_all_teachers(self) -> List[Teacher]:
        return list(self.teachers.values())
    
    # ========== ОПЕРАЦИИ С КУРСАМИ ==========
    
    def add_course(self, name: str, topic: str, teacher_id: Optional[str] = None) -> Course:
        """Создать курс"""
        course = Course(name, topic, teacher_id=teacher_id)
        self.courses[course.id] = course
        
        # Если указан преподаватель, назначаем его
        if teacher_id and teacher_id in self.teachers:
            self.teachers[teacher_id].assign_course(course.id)
        
        self._save_courses()
        self._save_teachers()
        logger.info(f"Создан курс: {name} ({topic})")
        return course
    
    def get_course(self, course_id: str) -> Optional[Course]:
        return self.courses.get(course_id)
    
    def get_all_courses(self) -> List[Course]:
        return list(self.courses.values())
    
    def get_active_courses(self) -> List[Course]:
        return [c for c in self.courses.values() if c.status == Course.STATUS_ACTIVE]
    
    def get_completed_courses(self) -> List[Course]:
        return [c for c in self.courses.values() if c.status == Course.STATUS_COMPLETED]
    
    # ========== ОПЕРАЦИИ: ЗАЧИСЛЕНИЕ ==========
    
    def enroll_student(self, student_id: str, course_id: str) -> Tuple[bool, str]:
        """
        Задание 2: Зачислить студента на курс
        """
        student = self.get_student(student_id)
        course = self.get_course(course_id)
        
        if not student:
            return False, f"Студент с ID {student_id} не найден"
        if not course:
            return False, f"Курс с ID {course_id} не найден"
        if course.status == Course.STATUS_COMPLETED:
            return False, f"Курс '{course.name}' уже завершён"
        if student_id in course.students:
            return False, f"Студент уже зачислен на курс '{course.name}'"
        
        # Зачисляем
        student.enroll(course_id)
        course.add_student(student_id)
        
        self._save_students()
        self._save_courses()
        logger.info(f"Студент {student.name} зачислен на курс {course.name}")
        return True, f"Студент {student.name} зачислен на курс '{course.name}'"
    
    # ========== ОПЕРАЦИИ: НАЗНАЧЕНИЕ ПРЕПОДАВАТЕЛЯ ==========
    
    def assign_teacher(self, teacher_id: str, course_id: str) -> Tuple[bool, str]:
        """
        Задание 2: Назначить преподавателя на курс
        """
        teacher = self.get_teacher(teacher_id)
        course = self.get_course(course_id)
        
        if not teacher:
            return False, f"Преподаватель с ID {teacher_id} не найден"
        if not course:
            return False, f"Курс с ID {course_id} не найден"
        if course.status == Course.STATUS_COMPLETED:
            return False, f"Курс '{course.name}' уже завершён"
        
        # Назначаем
        course.assign_teacher(teacher_id)
        teacher.assign_course(course_id)
        
        self._save_courses()
        self._save_teachers()
        logger.info(f"Преподаватель {teacher.name} назначен на курс {course.name}")
        return True, f"Преподаватель {teacher.name} назначен на курс '{course.name}'"
    
    # ========== ОПЕРАЦИИ: ВЫСТАВЛЕНИЕ ОЦЕНКИ ==========
    
    def add_grade(self, student_id: str, course_id: str, grade: int) -> Tuple[bool, str]:
        """
        Задание 2: Выставить оценку
        """
        student = self.get_student(student_id)
        course = self.get_course(course_id)
        
        if not student:
            return False, f"Студент с ID {student_id} не найден"
        if not course:
            return False, f"Курс с ID {course_id} не найден"
        if course.status == Course.STATUS_COMPLETED:
            return False, f"Курс '{course.name}' уже завершён"
        if student_id not in course.students:
            return False, f"Студент не зачислен на курс '{course.name}'"
        if not 0 <= grade <= 100:
            return False, "Оценка должна быть от 0 до 100"
        
        # Выставляем оценку
        student.add_grade(course_id, grade)
        course.add_grade(student_id, grade)
        
        self._save_students()
        self._save_courses()
        logger.info(f"Студенту {student.name} выставлена оценка {grade} за курс {course.name}")
        return True, f"Студенту {student.name} выставлена оценка {grade} за курс '{course.name}'"
    
    # ========== ОПЕРАЦИИ: ЗАВЕРШЕНИЕ КУРСА ==========
    
    def complete_course(self, course_id: str) -> Tuple[bool, str]:
        """
        Задание 2: Завершить курс
        Задание 3: При завершении фиксируются оценки и добавляются в историю
        """
        course = self.get_course(course_id)
        
        if not course:
            return False, f"Курс с ID {course_id} не найден"
        if course.status == Course.STATUS_COMPLETED:
            return False, f"Курс '{course.name}' уже завершён"
        
        # Завершаем курс
        course.complete()
        
        # Для всех студентов на курсе:
        # 1. Добавляем курс в завершённые
        # 2. Убираем из активных
        for student_id in course.students:
            student = self.get_student(student_id)
            if student:
                student.complete_course(course_id)
        
        self._save_courses()
        self._save_students()
        logger.info(f"Курс '{course.name}' завершён")
        return True, f"Курс '{course.name}' завершён. Записано в историю {len(course.students)} студентов"
    
    # ========== ОТЧЁТЫ ==========
    
    def get_student_report(self, student_id: str) -> Optional[Dict]:
        """
        Задание 4: Показать отчёт по студенту
        """
        student = self.get_student(student_id)
        if not student:
            return None
        
        report = {
            'student': student.name,
            'email': student.email,
            'active_courses': [],
            'completed_courses': [],
            'grades': {},
            'average_grade': student.get_average_grade(),
            'total_courses': len(student.courses) + len(student.completed_courses)
        }
        
        # Активные курсы
        for course_id in student.courses:
            course = self.get_course(course_id)
            if course:
                report['active_courses'].append({
                    'name': course.name,
                    'teacher': self.teachers.get(course.teacher_id, 'Не назначен')
                })
        
        # Завершённые курсы с оценками
        for course_id in student.completed_courses:
            course = self.get_course(course_id)
            if course:
                grades = student.grades.get(course_id, [])
                avg = sum(grades) / len(grades) if grades else 0
                report['completed_courses'].append({
                    'name': course.name,
                    'grades': grades,
                    'average': round(avg, 2)
                })
                report['grades'][course.name] = grades
        
        return report
