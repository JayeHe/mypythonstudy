# _*_coding:utf-8_*_
# Author:Jaye He

from ClassElectiveSystem.lib import role_module


def action(msg, menu):
    """
    执行选择的操作
    :param msg:
    :param menu:
    """
    while True:
        print(msg)
        choice = input('请选择操作>>').strip()
        if choice in menu:
            menu.get(choice)()


def admin_manage():
    """创建和删除管理员账号"""
    msg = '''
    1.创建管理员账号
    2.删除管理员账号
    3.退出
    '''
    menu = {
        '1': role_module.Initialize.create_admin,
        '2': role_module.Initialize.del_admin,
        '3': exit
    }
    action(msg, menu)


def admin_login():
    """管理员登录操作"""
    role_module.AdminRights.admin_login()
    msg = '''
    1:创建学校 2:查看学校 3:创建课程 4:查看课程
    5:创建老师 6:查看老师 7:创建班级 8:查看班级
               9:查看学生 10:退出
    '''
    menu = {
        '1': role_module.AdminRights.create_school,
        '2': role_module.AdminRights.show_school,
        '3': role_module.AdminRights.have_course,
        '4': role_module.AdminRights.show_course,
        '5': role_module.AdminRights.create_teacher,
        '6': role_module.AdminRights.show_teacher,
        '7': role_module.AdminRights.have_classes,
        '8': role_module.AdminRights.show_classes,
        '9': role_module.AdminRights.show_student,
        '10': exit
    }
    action(msg, menu)


def teacher_login():
    """老师登录操作"""
    teacher_obj = role_module.TeacherRights.teacher_login()
    msg = '''
    1.选择班级上课
    2.查看我的学员
    3.修改学员的成绩
    4.查看我的收入
    5.修改密码
    6.退出
    '''
    menu = {
        '1': teacher_obj.to_take_lessons,
        '2': teacher_obj.show_students,
        '3': teacher_obj.alter_record,
        '4': teacher_obj.show_income,
        '5': teacher_obj.change_password,
        '6': exit
    }
    action(msg, menu)


def student_enroll():
    """学生注册"""
    role_module.StudentRights.student_enroll()


def student_login():
    """学生登录操作"""
    student_obj = role_module.StudentRights.student_login()
    msg = '''
    1.选择班级并交学费
    2.查看我的信息
    3.修改密码
    4.退出
    '''
    menu = {
        '1': student_obj.choice_classes,
        '2': student_obj.show_my_info,
        '3': student_obj.change_password,
        '4': exit
    }
    action(msg, menu)


def run():
    msg = '''
    0.初始化管理员账号
    1.管理员账户登录
    2.老师账户登录
    3.学生注册
    4.学生账户登录
    5.退出
    '''
    menu = {
        '0': admin_manage,
        '1': admin_login,
        '2': teacher_login,
        '3': student_enroll,
        '4': student_login,
        '5': exit
    }
    action(msg, menu)
