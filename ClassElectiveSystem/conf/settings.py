# _*_coding:utf-8_*_
# Author:Jaye He
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADMIN_DB_DIR = os.path.join(BASE_DIR, 'db', 'admin')
SCHOOL_DB_DIR = os.path.join(BASE_DIR, 'db', 'school')
CLASSES_DB_DIR = os.path.join(BASE_DIR, 'db', 'classes')
COURSE_DB_DIR = os.path.join(BASE_DIR, 'db', 'course')
PERSON_DB_DIR = os.path.join(BASE_DIR, 'db', 'person')
TEACHER_DB_DIR = os.path.join(BASE_DIR, 'db', 'teacher')
STUDENT_DB_DIR = os.path.join(BASE_DIR, 'db', 'student')

COURSE_TO_TEACHER_DB_DIR = os.path.join(BASE_DIR, 'db', 'course_to_teacher')


INCOME_PRO = 0.5


