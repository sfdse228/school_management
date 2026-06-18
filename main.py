#!/usr/bin/env python3
"""
main.py - Система управления онлайн-школой (CLI)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.storage import SchoolStorage
from src.analytics import Analytics
from src.logger_setup import logger


class SchoolCLI:
    """Консольный интерфейс школы"""
    
    def __init__(self):
        self.storage = SchoolStorage()
        self.analytics = Analytics(self.storage)
    
    def show_menu(self):
        """Главное меню"""
        print("\n" + "=" * 50)
        print("🏫 СИСТЕМА УПРАВЛЕНИЯ ОНЛАЙН-ШКОЛОЙ")
        print("=" * 50)
        print("1. 👨‍🎓 Добавить студента")
        print("2. 👨‍🏫 Добавить преподавателя")
        print("3. 📚 Создать курс")
        print("4. 📋 Список всех курсов")
        print("5. ➕ Зачислить студента на курс")
        print("6. 👨‍🏫 Назначить преподавателя на курс")
        print("7. 📝 Выставить оценку")
        print("8. ✅ Завершить курс")
        print("9. 📊 Отчёт по студенту")
        print("10. 🏆 Топ студентов")
        print("11. 📈 Статистика курса")
        print("12. 💾 Сохранить и выйти")
        print("0. ❌ Выйти без сохранения")
        print("=" * 50)
    
    def add_student(self):
        """Добавить студента"""
        print("\n👨‍🎓 ДОБАВЛЕНИЕ СТУДЕНТА")
        name = input("Имя: ").strip()
        email = input("Email: ").strip()
        
        if not name or not email:
            print("❌ Имя и email обязательны!")
            return
        
        student = self.storage.add_student(name, email)
        print(f"✅ Студент добавлен! ID: {student.id}")
    
    def add_teacher(self):
        """Добавить преподавателя"""
        print("\n👨‍🏫 ДОБАВЛЕНИЕ ПРЕПОДАВАТЕЛЯ")
        name = input("Имя: ").strip()
        specialization = input("Специализация: ").strip()
        
        if not name or not specialization:
            print("❌ Имя и специализация обязательны!")
            return
        
        teacher = self.storage.add_teacher(name, specialization)
        print(f"✅ Преподаватель добавлен! ID: {teacher.id}")
    
    def add_course(self):
        """Создать курс"""
        print("\n📚 СОЗДАНИЕ КУРСА")
        name = input("Название: ").strip()
        topic = input("Тема: ").strip()
        
        if not name or not topic:
            print("❌ Название и тема обязательны!")
            return
        
        # Показать преподавателей для назначения
        teachers = self.storage.get_all_teachers()
        if teachers:
            print("\nДоступные преподаватели:")
            for i, t in enumerate(teachers, 1):
                print(f"  {i}. {t.name} ({t.specialization})")
            choice = input("Выберите преподавателя (номер, или Enter пропустить): ").strip()
            
            teacher_id = None
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(teachers):
                    teacher_id = teachers[idx].id
        else:
            print("⚠️ Нет преподавателей. Курс будет создан без преподавателя.")
            teacher_id = None
        
        course = self.storage.add_course(name, topic, teacher_id)
        print(f"✅ Курс создан! ID: {course.id}")
    
    def list_courses(self):
        """Список всех курсов"""
        print("\n📋 СПИСОК КУРСОВ")
        courses = self.storage.get_all_courses()
        
        if not courses:
            print("📭 Нет курсов")
            return
        
        print("=" * 60)
        for course in courses:
            teacher = self.storage.get_teacher(course.teacher_id)
            teacher_name = teacher.name if teacher else "Не назначен"
            print(f"📚 {course}")
            print(f"   ID: {course.id}")
            print(f"   Преподаватель: {teacher_name}")
            print(f"   Студентов: {len(course.students)}")
            print(f"   Статус: {course.status}")
            print("-" * 60)
    
    def enroll_student(self):
        """Зачислить студента на курс"""
        print("\n➕ ЗАЧИСЛЕНИЕ СТУДЕНТА")
        
        # Показать студентов
        students = self.storage.get_all_students()
        if not students:
            print("❌ Нет студентов")
            return
        print("\nСтуденты:")
        for i, s in enumerate(students, 1):
            print(f"  {i}. {s.name} ({s.email})")
        
        student_choice = input("Выберите студента (номер): ").strip()
        if not student_choice.isdigit():
            print("❌ Неверный выбор!")
            return
        student_idx = int(student_choice) - 1
        if not (0 <= student_idx < len(students)):
            print("❌ Неверный выбор!")
            return
        
        # Показать активные курсы
        courses = self.storage.get_active_courses()
        if not courses:
            print("❌ Нет активных курсов")
            return
        print("\nАктивные курсы:")
        for i, c in enumerate(courses, 1):
            print(f"  {i}. {c.name} ({c.topic})")
        
        course_choice = input("Выберите курс (номер): ").strip()
        if not course_choice.isdigit():
            print("❌ Неверный выбор!")
            return
        course_idx = int(course_choice) - 1
        if not (0 <= course_idx < len(courses)):
            print("❌ Неверный выбор!")
            return
        
        success, message = self.storage.enroll_student(
            students[student_idx].id,
            courses[course_idx].id
        )
        print(f"{'✅' if success else '❌'} {message}")
    
    def assign_teacher_to_course(self):
        """Назначить преподавателя на курс"""
        print("\n👨‍🏫 НАЗНАЧЕНИЕ ПРЕПОДАВАТЕЛЯ")
        
        # Показать преподавателей
        teachers = self.storage.get_all_teachers()
        if not teachers:
            print("❌ Нет преподавателей")
            return
        print("\nПреподаватели:")
        for i, t in enumerate(teachers, 1):
            print(f"  {i}. {t.name} ({t.specialization})")
        
        teacher_choice = input("Выберите преподавателя (номер): ").strip()
        if not teacher_choice.isdigit():
            print("❌ Неверный выбор!")
            return
        teacher_idx = int(teacher_choice) - 1
        if not (0 <= teacher_idx < len(teachers)):
            print("❌ Неверный выбор!")
            return
        
        # Показать курсы без преподавателя или с другим
        courses = [c for c in self.storage.get_active_courses() if c.teacher_id != teachers[teacher_idx].id]
        if not courses:
            print("❌ Нет доступных курсов")
            return
        print("\nДоступные курсы:")
        for i, c in enumerate(courses, 1):
            current_teacher = self.storage.get_teacher(c.teacher_id)
            current = f" (сейчас: {current_teacher.name})" if current_teacher else " (без преподавателя)"
            print(f"  {i}. {c.name}{current}")
        
        course_choice = input("Выберите курс (номер): ").strip()
        if not course_choice.isdigit():
            print("❌ Неверный выбор!")
            return
        course_idx = int(course_choice) - 1
        if not (0 <= course_idx < len(courses)):
            print("❌ Неверный выбор!")
            return
        
        success, message = self.storage.assign_teacher(
            teachers[teacher_idx].id,
            courses[course_idx].id
        )
        print(f"{'✅' if success else '❌'} {message}")
    
    def add_grade(self):
        """Выставить оценку"""
        print("\n📝 ВЫСТАВЛЕНИЕ ОЦЕНКИ")
        
        # Показать студентов
        students = self.storage.get_all_students()
        if not students:
            print("❌ Нет студентов")
            return
        print("\nСтуденты:")
        for i, s in enumerate(students, 1):
            print(f"  {i}. {s.name} ({s.email})")
        
        student_choice = input("Выберите студента (номер): ").strip()
        if not student_choice.isdigit():
            print("❌ Неверный выбор!")
            return
        student_idx = int(student_choice) - 1
        if not (0 <= student_idx < len(students)):
            print("❌ Неверный выбор!")
            return
        
        student = students[student_idx]
        
        # Показать курсы студента
        if not student.courses:
            print(f"❌ Студент {student.name} не зачислен ни на один курс")
            return
        print(f"\nКурсы {student.name}:")
        for i, course_id in enumerate(student.courses, 1):
            course = self.storage.get_course(course_id)
            if course:
                print(f"  {i}. {course.name}")
        
        course_choice = input("Выберите курс (номер): ").strip()
        if not course_choice.isdigit():
            print("❌ Неверный выбор!")
            return
        course_idx = int(course_choice) - 1
        if not (0 <= course_idx < len(student.courses)):
            print("❌ Неверный выбор!")
            return
        
        course_id = student.courses[course_idx]
        
        grade = input("Введите оценку (0-100): ").strip()
        if not grade.isdigit():
            print("❌ Оценка должна быть числом!")
            return
        
        success, message = self.storage.add_grade(student.id, course_id, int(grade))
        print(f"{'✅' if success else '❌'} {message}")
    
    def complete_course(self):
        """Завершить курс"""
        print("\n✅ ЗАВЕРШЕНИЕ КУРСА")
        
        courses = self.storage.get_active_courses()
        if not courses:
            print("❌ Нет активных курсов")
            return
        
        print("\nАктивные курсы:")
        for i, c in enumerate(courses, 1):
            print(f"  {i}. {c.name} ({c.topic}) - {len(c.students)} студентов")
        
        choice = input("Выберите курс для завершения (номер): ").strip()
        if not choice.isdigit():
            print("❌ Неверный выбор!")
            return
        idx = int(choice) - 1
        if not (0 <= idx < len(courses)):
            print("❌ Неверный выбор!")
            return
        
        success, message = self.storage.complete_course(courses[idx].id)
        print(f"{'✅' if success else '❌'} {message}")
    
    def student_report(self):
        """Отчёт по студенту"""
        print("\n📊 ОТЧЁТ ПО СТУДЕНТУ")
        
        students = self.storage.get_all_students()
        if not students:
            print("❌ Нет студентов")
            return
        
        print("\nСтуденты:")
        for i, s in enumerate(students, 1):
            print(f"  {i}. {s.name} ({s.email})")
        
        choice = input("Выберите студента (номер): ").strip()
        if not choice.isdigit():
            print("❌ Неверный выбор!")
            return
        idx = int(choice) - 1
        if not (0 <= idx < len(students)):
            print("❌ Неверный выбор!")
            return
        
        report = self.storage.get_student_report(students[idx].id)
        if not report:
            print("❌ Студент не найден")
            return
        
        print("\n" + "=" * 50)
        print(f"📊 ОТЧЁТ ПО СТУДЕНТУ: {report['student']}")
        print("=" * 50)
        print(f"📧 Email: {report['email']}")
        print(f"📚 Всего курсов: {report['total_courses']}")
        print(f"⭐ Средняя оценка: {report['average_grade']:.2f}")
        
        if report['active_courses']:
            print(f"\n🟢 Активные курсы ({len(report['active_courses'])}):")
            for c in report['active_courses']:
                print(f"  • {c['name']} (Преподаватель: {c['teacher']})")
        
        if report['completed_courses']:
            print(f"\n✅ Завершённые курсы ({len(report['completed_courses'])}):")
            for c in report['completed_courses']:
                print(f"  • {c['name']} - Оценки: {c['grades']} (ср.: {c['average']})")
        
        print("=" * 50)
    
    def top_students(self):
        """Топ студентов"""
        print("\n🏆 ТОП СТУДЕНТОВ")
        top = self.analytics.get_top_students(5)
        
        if not top:
            print("📭 Нет данных об успеваемости")
            return
        
        print("=" * 50)
        print(f"{'#':>3} {'Имя':<20} {'Ср. оценка':<12} {'Курсов':<8}")
        print("-" * 50)
        for i, student in enumerate(top, 1):
            print(f"{i:>3} {student['name']:<20} {student['average_grade']:<12} {student['courses_completed']:<8}")
        print("=" * 50)
    
    def course_statistics(self):
        """Статистика курса"""
        print("\n📈 СТАТИСТИКА КУРСА")
        
        courses = self.storage.get_all_courses()
        if not courses:
            print("❌ Нет курсов")
            return
        
        print("\nКурсы:")
        for i, c in enumerate(courses, 1):
            print(f"  {i}. {c.name} ({c.status})")
        
        choice = input("Выберите курс (номер): ").strip()
        if not choice.isdigit():
            print("❌ Неверный выбор!")
            return
        idx = int(choice) - 1
        if not (0 <= idx < len(courses)):
            print("❌ Неверный выбор!")
            return
        
        stats = self.analytics.get_course_statistics(courses[idx].id)
        if not stats:
            print("❌ Курс не найден")
            return
        
        print("\n" + "=" * 50)
        print(f"📈 СТАТИСТИКА КУРСА: {stats['course_name']}")
        print("=" * 50)
        print(f"📚 Тема: {stats['topic']}")
        print(f"📊 Статус: {stats['status']}")
        print(f"👨‍🏫 Преподаватель: {stats['teacher']}")
        print(f"👨‍🎓 Студентов: {stats['students_count']}")
        print(f"📝 Всего оценок: {stats['grades_count']}")
        print(f"⭐ Средняя оценка: {stats['average_grade']:.2f}")
        print(f"⬆ Максимальная: {stats['max_grade']}")
        print(f"⬇ Минимальная: {stats['min_grade']}")
        print("=" * 50)
    
    def run(self):
        """Запуск CLI"""
        print("\n🏫 ДОБРО ПОЖАЛОВАТЬ В СИСТЕМУ УПРАВЛЕНИЯ ШКОЛОЙ")
        print(f"📊 Загружено: {len(self.storage.students)} студентов, "
              f"{len(self.storage.teachers)} преподавателей, "
              f"{len(self.storage.courses)} курсов")
        
        while True:
            self.show_menu()
            choice = input("Выберите действие: ").strip()
            
            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.add_teacher()
            elif choice == "3":
                self.add_course()
            elif choice == "4":
                self.list_courses()
            elif choice == "5":
                self.enroll_student()
            elif choice == "6":
                self.assign_teacher_to_course()
            elif choice == "7":
                self.add_grade()
            elif choice == "8":
                self.complete_course()
            elif choice == "9":
                self.student_report()
            elif choice == "10":
                self.top_students()
            elif choice == "11":
                self.course_statistics()
            elif choice == "12":
                self.storage.save_all()
                print("✅ Данные сохранены. До свидания!")
                logger.info("Программа завершена (сохранение)")
                break
            elif choice == "0":
                print("⚠️ Выход без сохранения!")
                logger.warning("Программа завершена без сохранения")
                break
            else:
                print("❌ Неверный выбор!")
            
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    try:
        cli = SchoolCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ Принудительное завершение...")
        logger.info("Принудительное завершение программы")
        sys.exit(0)
