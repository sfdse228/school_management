"""
analytics.py - Аналитика успеваемости
"""

from typing import List, Dict, Optional
from src.storage import SchoolStorage
from src.models import Course, Student


class Analytics:
    """Класс для аналитики успеваемости"""
    
    def __init__(self, storage: SchoolStorage):
        self.storage = storage
    
    def get_course_statistics(self, course_id: str) -> Optional[Dict]:
        """Статистика по курсу"""
        course = self.storage.get_course(course_id)
        if not course:
            return None
        
        grades = []
        for student_id in course.students:
            student = self.storage.get_student(student_id)
            if student:
                student_grades = student.grades.get(course_id, [])
                grades.extend(student_grades)
        
        return {
            'course_name': course.name,
            'topic': course.topic,
            'status': course.status,
            'teacher': self.storage.get_teacher(course.teacher_id),
            'students_count': len(course.students),
            'grades_count': len(grades),
            'average_grade': sum(grades) / len(grades) if grades else 0,
            'max_grade': max(grades) if grades else 0,
            'min_grade': min(grades) if grades else 0
        }
    
    def get_top_students(self, n: int = 5) -> List[Dict]:
        """Топ-N студентов по успеваемости"""
        results = []
        for student in self.storage.get_all_students():
            avg = student.get_average_grade()
            if avg > 0:
                results.append({
                    'name': student.name,
                    'email': student.email,
                    'average_grade': round(avg, 2),
                    'courses_completed': len(student.completed_courses),
                    'active_courses': len(student.courses)
                })
        
        results.sort(key=lambda x: x['average_grade'], reverse=True)
        return results[:n]
    
    def get_teacher_statistics(self, teacher_id: str) -> Optional[Dict]:
        """Статистика преподавателя"""
        teacher = self.storage.get_teacher(teacher_id)
        if not teacher:
            return None
        
        courses = [self.storage.get_course(cid) for cid in teacher.courses]
        active_courses = [c for c in courses if c and c.status == Course.STATUS_ACTIVE]
        completed_courses = [c for c in courses if c and c.status == Course.STATUS_COMPLETED]
        
        total_students = sum(len(c.students) for c in courses if c)
        
        return {
            'teacher_name': teacher.name,
            'specialization': teacher.specialization,
            'total_courses': len(courses),
            'active_courses': len(active_courses),
            'completed_courses': len(completed_courses),
            'total_students': total_students
        }
