# _*_coding:utf-8_*_
# Author:Jaye He

import pickle,os,time,re,uuid
from ClassElectiveSystem.conf import settings


class BaseModel(object):
    """用来存储和读取数据的基类"""
    def save(self):
        """保存pickle序列化实例对象"""
        file_path = os.path.join(self.db_path, str(self.nid))
        f = open(file_path, 'wb')
        pickle.dump(self, f)
        f.flush()
        f.close()

    @staticmethod
    def create_uuid():
        """生成唯一标识符"""
        return str(uuid.uuid1())

    @staticmethod
    def get_obj_list(path, nid_list):
        """
        载入一个nid列表对应的所有实例
        :param path: 实例所在文件夹的路径
        :param nid_list: 实例文件名的列表
        :return obj_list: 包含实例的列表
        """
        obj_list = []
        for nid in nid_list:
            file_path = os.path.join(path, nid)
            obj_list.append(pickle.load(open(file_path, 'rb')))
        return obj_list

    @classmethod
    def get_all_obj_list(cls):
        """载入文件夹中所有pickle序列化实例对象"""
        nid_list = os.listdir(cls.db_path)
        obj_list = cls.get_obj_list(cls.db_path, nid_list)
        return obj_list

    @classmethod
    def del_obj(cls):
        """删除指定pickle序列化实例对象"""
        while True:
            username = input('请输入需要删除的账户>>').strip()
            if len(username) != 0:
                break
        user_dic = {}
        for nid in os.listdir(cls.db_path):
            file_path = os.path.join(cls.db_path, nid)
            f = open(file_path, 'rb')
            obj = pickle.load(f)
            f.close()
            user_dic[obj.username] = file_path
        if username in user_dic:
            os.remove(user_dic[username])
            return True, username
        else:
            return False, username


class Admin(BaseModel):
    """管理员类"""
    db_path = settings.ADMIN_DB_DIR

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.create_time = time.strftime('%Y-%m-%d %X')
        self.nid = BaseModel.create_uuid()


class School(BaseModel):
    """学校类"""
    db_path = settings.SCHOOL_DB_DIR

    def __init__(self, name, addr):
        self.name = name
        self.addr = addr
        self.nid = BaseModel.create_uuid()
        self.create_time = time.strftime('%Y-%m-%d %X')
        self.classes_list = []
        self.course_list = []
        self.teacher_list = []
        self.__income = 0

    def __str__(self):
        return self.name

    def create_classes(self):
        """通过学校实例创建班级"""
        # 第一步为班级关联课程,如果课程未创建,必须先创建课程
        school = '%s-%s校区' % (self.name, self.addr)
        course_obj_list = BaseModel.get_obj_list(Course.db_path, self.course_list)
        if course_obj_list:
            course_dic = {}
            print('课程列表如下'.center(60, '-'))
            sn = 1
            for obj in course_obj_list:
                course_dic[str(sn)] = obj
                print('\033[1;33m序列[%s] 课程[%s]\033[0m'.center(60, '-') % (str(sn), obj.name))
                sn += 1
            while True:
                course = input('请选择本班课程序列号>>').strip()
                if course in course_dic:break
            course_obj = course_dic[course]

            # 第二步为班级关联老师
            teacher_obj_list = BaseModel.get_obj_list(Teacher.db_path, self.teacher_list)
            if teacher_obj_list:
                teacher_dic = {}
                print('学校[%s]教师列表如下'.center(60, '-') % school)
                sn_t = 1
                for obj in teacher_obj_list:
                    teacher_dic[str(sn_t)] = obj
                    age = obj.get_age()
                    print('\033[1;33m序列[%s] 姓名[%s] 性别[%s] 年龄[%s]\033[0m'.center(60, '-')
                          % (str(sn_t), obj.name, obj.sex, age))
                    sn_t += 1
                while True:
                    choice = input('请选择本班导师序列号>>').strip()
                    if choice in teacher_dic:break
                teacher_obj = teacher_dic[choice]
                name = 'classes-' + str(time.strftime('%Y%m%d%H%M%S', time.localtime()))
                classes_obj = Classes(name, self.nid, teacher_obj.nid, course_obj.nid)
                course_obj.classes_list.append(classes_obj.nid)
                self.classes_list.append(classes_obj.nid)
                teacher_obj.classes_list.append(classes_obj.nid)
                course_obj.save()
                self.save()
                teacher_obj.save()
                classes_obj.save()
                print('\033[1;33m班级[%s] 课程[%s] 导师[%s] 所属学校[%s] 创建成功!\033[0m'
                      % (name, course_obj.name, teacher_obj.name, school))
            else:
                print('\033[1;31m学校[%s]老师尚未创建,请先创建老师!!!\033[0m' % school)
        else:
            print('\033[1;31m学校[%s]课程尚未创建,请先创建课程!!!\033[0m' % school)

    def create_course(self):
        """通过学校实例创建课程"""
        school = '%s-%s校区' % (self.name, self.addr)
        print('学校[%s]开始创建课程'.center(60, '-') % school)
        while True:
            name = input('请输入课程名称>>').strip()
            price = input('请输入课程价格>>').strip()
            if not price.isdigit():continue
            period = input('请输入课程周期数,单位为月>>').strip()
            if len(name) == 0 or len(price) == 0 or len(period) == 0:continue
            elif not price.isdigit() or not period.isdigit():continue
            else:break
        school_nid = self.nid
        course_obj = Course(name, price, period, school_nid)
        self.course_list.append(course_obj.nid)
        self.save()
        course_obj.save()
        print('\033[1;33m课程[%s] 学费[%s元] 周期[%s月] 所属学校[%s] 创建成功!\033[0m'
              % (name, price, period, school))


class Classes(BaseModel):
    """班级类"""
    db_path = settings.CLASSES_DB_DIR

    def __init__(self, name, school_nid, teacher_nid, course_nid):
        self.name = name
        self.school_nid = school_nid
        self.teacher_nid = teacher_nid
        self.course_nid = course_nid
        self.student_list = []
        self.create_time = time.strftime('%Y-%m-%d %X')
        self.nid = BaseModel.create_uuid()


class Course(BaseModel):
    """课程类"""
    db_path = settings.COURSE_DB_DIR

    def __init__(self, name, price, period, school_nid):
        self.name = name
        self.price = price
        self.period = period
        self.school_nid = school_nid
        self.classes_list = []
        self.create_time = time.strftime('%Y-%m-%d %X')
        self.nid = BaseModel.create_uuid()


class Person(BaseModel):
    """成员类"""
    def __init__(self, username, password, name, sex, birthday, school_nid):
        self.username = username
        self.password = password
        self.name = name
        self.sex = sex
        self.birthday = birthday
        self.school_nid = school_nid
        self.create_time = time.strftime('%Y-%m-%d %X')

    def get_age(self):
        """通过生日计算出年龄"""
        # 1900年5月6日 ---> 1900-5-6
        birthday = '-'.join([i for i in re.split('\D', self.birthday) if i])
        bir = time.mktime(time.strptime(birthday, '%Y-%m-%d'))
        now = time.time()
        age = int((now-bir)/3600/24/365)
        return str(age)

    def change_password(self):
        """修改密码"""
        count = 0
        while True:
            if count == 3:
                exit('\033[1;31m错误次数过多!!!\033[0m')
            old_pwd = input('请输入原密码>>').strip()
            if old_pwd == self.password:
                while True:
                    new_pwd = input('请输入新密码,必须同时且只能包含字母和数字,6-10位>>').strip()
                    if re.search('[ ]+', new_pwd):continue
                    if re.search('^(?!([a-zA-Z]+|\d+)$)[a-zA-Z\d]{6,10}$', new_pwd):
                        check_pwd = input('再次输入新密码>>').strip()
                        if check_pwd == new_pwd:break
                self.password = new_pwd
                self.save()
                print('\033[1;33m密码修改成功\033[0m')
                break
            count += 1


class Teacher(Person):
    """老师类"""
    db_path = settings.TEACHER_DB_DIR

    def __init__(self, username, password, name, sex, birthday, school_nid):
        super(Teacher, self).__init__(username, password, name, sex, birthday, school_nid)
        self.classes_list = []   # [classes_nid,......]
        self.nid = BaseModel.create_uuid()

    def get_classes(self):
        """获取老师关联班级的信息"""
        res = {}
        if self.classes_list:
            for nid in self.classes_list:
                classes_obj = BaseModel.get_obj_list(Classes.db_path, [nid])[0]
                course_obj = BaseModel.get_obj_list(Course.db_path, [classes_obj.course_nid])[0]
                school_obj = BaseModel.get_obj_list(School.db_path, [self.school_nid])[0]
                res[str(self.classes_list.index(nid))] = {'classes': classes_obj,
                                                          'course': course_obj,
                                                          'school': school_obj}
        return res

    def show_classes(self):
        """显示老师关联班级的信息"""
        res = self.get_classes()
        if res:
            for i in res:
                classes_name = res[i]['classes'].name
                course_name = res[i]['course'].name
                course_price = res[i]['course'].price
                course_period = res[i]['course'].period
                sum_student = len(res[i]['classes'].student_list)
                school = '%s-%s校区' % (res[i]['school'].name, res[i]['school'].addr)
                print('''
                \033[1;33m 序号[%s] 班级:[%s] 课程:[%s] 学费:[%s元]
                周期:[%s] 学员人数:[%s] 学校:[%s]\033[0m
                '''.center(60, '-')
                      % (i, classes_name, course_name, course_price, course_period, sum_student, school))
        else:
            print('\033[1;31m无班级信息\033[0m')
        return res

    def show_income(self):
        """计算老师收入"""
        income = 0
        if self.get_classes():
            for classes in self.get_classes():
                sum_student = len(self.get_classes()[classes]['classes'].student_list)
                price = float(self.get_classes()[classes]['course'].price)
                income += sum_student*price*float(settings.INCOME_PRO)
        else:
            print('\033[1;31m老师尚未关联班级\033[0m')
        print('\033[1;33m我的收入为[%s元]\033[0m'.center(60, '-') % str(income))

    # res_dic = {'1':{'classes': classes_obj, 'course': course_obj,'school': school_obj},.....}
    def show_students(self):
        """显示我执教班级的学生"""
        res_dic = self.show_classes()
        if res_dic:
            while True:
                choice = input('请选择需要查看的班级序号>>').strip()
                if choice in res_dic:break
            classes_obj = res_dic[choice]['classes']
            student_list = classes_obj.student_list
            if student_list:
                course_obj = res_dic[choice]['course']
                student_dic = {}  # {'1':student_obj,....}
                print('班级[%s] 开设课程[%s] 的学生列表如下'.center(60, '-') % (classes_obj.name, course_obj.name))
                for nid in student_list:
                    obj = BaseModel.get_obj_list(Student.db_path, [nid])[0]
                    student_dic[str(student_list.index(nid))] = obj
                    # self.classes_dic = {'classes_nid':{'record':None,'course':'course_nid',...},...}}
                    classes_dic = obj.classes_dic
                    record = classes_dic[classes_obj.nid]['record']
                    print('\033[1;33m序号:[%s] 姓名:[%s] 性别:[%s] 年龄:[%s] 成绩[%s]\033[0m'.center(60, '-')
                          % (str(student_list.index(nid)), obj.name, obj.sex, obj.get_age(), record))
                return student_dic, classes_obj
            else:
                print('\033[1;31m班级无学生!\033[0m')

    def alter_record(self):
        """修改学员成绩"""
        res = self.show_students()
        if res:
            student_dic, classes_obj = res
            while True:
                choice = input('请选择学生编号>>')
                if choice in student_dic:break
            student_obj = student_dic[choice]
            record = student_obj.classes_dic[classes_obj.nid]['record']
            print('需要修改成绩的学生 姓名:[%s] 性别:[%s] 年龄:[%s] 成绩:[%s]'.center(60, '-')
                  % (student_obj.name, student_obj.sex, student_obj.get_age(), record))
            while True:
                new_record = input('请输入新成绩>>').strip()
                if new_record.isdigit():break
            student_obj.classes_dic[classes_obj.nid]['record'] = new_record
            student_obj.save()
            print('成绩修改成功,最新成绩为'.center(60, '-'))
            print('\033[1;33m姓名:[%s] 性别:[%s] 年龄:[%s] 成绩:[%s]\033[0m'.center(60, '-')
                  % (student_obj.name, student_obj.sex, student_obj.get_age(), new_record))

    def to_take_lessons(self):
        """选择班级上课"""
        res = self.show_classes()
        if res:
            while True:
                choice = input('请选择班级序号开始上课>>')
                if choice in res:break
            student_list = res[choice]['classes'].student_list
            TeacherRights.to_teaching(student_list)
            print('\033[1;33m班级:[%s] 开始上课\033[0m'.center(60, '-') % res[choice]['classes'].name)


class Student(Person):
    """学生类"""
    db_path = settings.STUDENT_DB_DIR

    def __init__(self, username, password, name, sex, birthday, school_nid):
        super(Student, self).__init__(username, password, name, sex, birthday, school_nid)
        self.balance = 30000
        self.classes_dic = {}  # self.classes_dic = {'classes_nid':{'record':None,'course':'course_nid',...},...}}
        self.nid = BaseModel.create_uuid()

    def choice_classes(self):
        """学生选择班级并交学费"""
        # student_obj.classes_dic = {classes_nid:{'course_nid':course_nid,'record':record},.....}
        school_obj = BaseModel.get_obj_list(School.db_path, [self.school_nid])[0]
        school = '%s-%s校区' % (school_obj.name, school_obj.addr)
        course_list = school_obj.course_list
        if course_list:
            course_obj_list = BaseModel.get_obj_list(Course.db_path, course_list)
            print('学校[%s]课程列表如下'.center(60, '-') % school)
            course = {}
            sn = 1
            for course_obj in course_obj_list:
                course[str(sn)] = course_obj
                print('\033[1;33m序列[%s] 课程[%s] 学费[%s元]\033[0m'.center(60, '-')
                      % (str(sn), course_obj.name, course_obj.price))
                sn += 1
            while True:
                cho_course = input('请选择课程序列号>>').strip()
                if cho_course in course:break
            my_course_obj = course[cho_course]
            # 以下选择班级
            classes_list = my_course_obj.classes_list
            if classes_list:
                classes_obj_list = BaseModel.get_obj_list(Classes.db_path, my_course_obj.classes_list)
                classes = {}
                print('开设课程[%s]的所有班级如下'.center(60, '-'))
                sn_cla = 1
                for obj in classes_obj_list:
                    classes[str(sn_cla)] = obj
                    teacher_obj = BaseModel.get_obj_list(Teacher.db_path, [obj.teacher_nid])[0]
                    print('\033[1;33m序列[%s] 班级[%s] 课程[%s] 导师[%s]\033[0m'.center(60, '-')
                          % (str(sn_cla), obj.name, my_course_obj.name, teacher_obj.name))
                while True:
                    cho_classes = input('请选择班级序列号>>').strip()
                    if cho_classes in classes:break
                my_classes_obj = classes[cho_classes]
                state = int(self.balance) - int(my_course_obj.price)
                if state > 0:
                    self.balance = str(state)
                    self.classes_dic[str(my_classes_obj.nid)] = {'course_nid': my_course_obj.nid, 'record': None}
                    self.save()                         # 学生数据更新保存
                    my_classes_obj.student_list.append(self.nid)
                    my_classes_obj.save()                      # 班级数据更新保存
                    my_teacher_obj = BaseModel.get_obj_list(Teacher.db_path, [my_classes_obj.teacher_nid])[0]
                    print('\033[1;33m已选择 课程[%s] 班级[%s] 导师[%s] 学费[%s元] 所属学校[%s]\033[0m'.center(60, '-')
                          % (my_course_obj.name, my_classes_obj.name, my_teacher_obj.name, my_course_obj.price, school))
                else:
                    print('\033[1;31m余额不足!!!\033[0m')
            else:
                print('\033[1;31m课程[%s]尚未关联班级,请先关联班级!!!\033[0m')

        else:
            print('\033[1;31m学校[%s]尚未创建课程,请先创建课程!!!\033[0m' % school)

    def show_my_info(self):
        """学生查看自己信息"""
        school_obj = BaseModel.get_obj_list(School.db_path, [self.school_nid])[0]
        print('会员名:%s 姓名:%s 性别:%s 生日:%s 余额:%s 所属学校:%s-%s校区'.center(60, '-')
              % (self.username, self.name, self.sex, self.birthday, self.balance, school_obj.name, school_obj.addr))
        # student_obj.classes_dic = {classes_nid:{'course_nid':course_nid,'record':record},.....}
        if self.classes_dic:
            for classes_nid in self.classes_dic:
                my_classes_obj = BaseModel.get_obj_list(Classes.db_path, [classes_nid])[0]
                teacher_obj = BaseModel.get_obj_list(Teacher.db_path, [my_classes_obj.teacher_nid])[0]
                my_course_obj = BaseModel.get_obj_list(Course.db_path, [self.classes_dic[classes_nid]['course_nid']])[0]
                my_record = self.classes_dic[classes_nid]['record']
                print('\033[1;33m所在班级[%s] 课程[%s] 导师[%s] 我的成绩[%s]\033[0m'.center(60, '-')
                      % (my_classes_obj.name, my_course_obj.name, teacher_obj.name, my_record))
        else:
            print('\033[1;33m我尚未参加学习\033[0m')


class BaseRights(object):
    """基础操作"""
    @staticmethod
    def login(obj_list):
        """
        登录验证
        :param obj_list: 实例列表
        """
        count = 0
        while True:
            username = input('请输入用户名').strip()
            if len(username) == 0:continue
            password = input('请输入密码').strip()
            if len(password) == 0:continue
            for obj in obj_list:
                if obj.username == username and obj.password == password:
                    print('\033[1;33m登录成功\033[0m')
                    return obj
                else:
                    print('\033[1;31m用户名或密码错误\033[0m')
                    count += 1
            if count == 3:
                exit('错误次数过多,已退出!')


class Initialize(BaseRights):
    """管理员初始化"""
    @staticmethod
    def create_admin():
        """创建管理员"""
        try:
            while True:
                username = input('请输入初始化用户名>>').strip()
                if re.search('[ ]+', username):continue
                if len(username) != 0:break
            existing_username_list = [obj.username for obj in Admin.get_all_obj_list()]
            if username in existing_username_list:
                raise Exception('\033[1;31m用户名[%s]已存在!\033[0m' % username)
            while True:
                password = input('请输入初始化密码,只能是数字和字母,6-10位>>').strip()
                if re.search('[ ]+', password):continue
                if re.search('^(?!([a-zA-Z]+|\d+)$)[a-zA-Z\d]{6,10}$', password):break
            obj = Admin(username, password)
            obj.save()
            print('\033[1;33m管理员账号[%s]创建成功!!\033[0m' % username)
        except Exception as e:
            print(e)

    @staticmethod
    def del_admin():
        """删除管理员"""
        try:
            res = Admin.del_obj()
            if res[0]:
                print('\033[1;33m管理员帐户[%s]删除成功!\033[0m' % res[-1])
            else:
                raise Exception('\033[1;31m管理员帐户[%s]不存在!!\033[0m' % res[-1])
        except Exception as e:
            print(e)


class AdminRights(BaseRights):
    """管理员操作"""
    @staticmethod
    def admin_login():
        """管理员登录"""
        return BaseRights.login(Admin.get_all_obj_list())

    @staticmethod
    def create_school():
        """创建学校"""
        try:
            while True:
                name = input('请输入学校名字>>').strip()
                if len(name) == 0:continue
                addr = input('请输入学校地址>>').strip()
                if len(addr) == 0:continue
                break
            existing_schools_list = [(obj.name, obj.addr) for obj in School.get_all_obj_list()]
            if (name, addr) in existing_schools_list:
                raise Exception('\033[1;31m[%s] [%s]校区 已经存在,不可重复创建\033[0m' % (name, addr))
            obj = School(name, addr)
            obj.save()
            print('\033[1;33m[%s] [%s]校区 创建成功\033[0m' % (obj.name, obj.addr))
        except Exception as e:
            print(str(e))

    @staticmethod
    def show_school():
        """显示所有学校"""
        school_obj_list = School.get_all_obj_list()
        school_obj_dic = {}
        if school_obj_list:
            print('学校列表如下'.center(60, '-'))
            sn = 1
            for obj in School.get_all_obj_list():
                school_obj_dic[str(sn)] = obj
                print('\033[1;33m序号[%s]:学校[%s-%s校区] 创建日期[%s]\033[0m'.center(60, '-')
                      % (str(sn), obj.name, obj.addr, obj.create_time))
                sn += 1
        else:
            print('\033[1;31m学校尚未创建\033[0m'.center(60, '-'))
        return school_obj_dic

    @staticmethod
    def have_course():
        """创建课程"""
        print('开始创建课程'.center(60, '-'))
        school_obj_dic = AdminRights.show_school()
        while True:
            choice = input('请选择需要创建课程的学校序列号>>').strip()
            if choice in school_obj_dic:break
        school_obj_dic[choice].create_course()

    @staticmethod
    def show_course():
        """显示课程"""
        obj_list = Course.get_all_obj_list()
        if obj_list:
            for obj in obj_list:
                school_obj = BaseModel.get_obj_list(School.db_path, [obj.school_nid])[0]
                print('\033[1;33m课程[%s] 学费[%s元] 周期[%s月] 所属学校[%s_%s校区]\033[0m'.center(60, '-')
                      % (obj.name, obj.price, obj.period, school_obj.name, school_obj.addr))
        else:
            print('\033[1;31m课程尚未创建\033[0m'.center(60, '-'))

    @staticmethod
    def create_teacher():
        """创建老师"""
        print('开始创建教师账户'.center(60, '-'))
        while True:
            name = input('请输入教师姓名>>').strip()
            if re.search('[ ]+', name):continue
            if len(name) != 0:break
        while True:
            sex = input('请输入教师性别>>').strip()
            if re.search('^[男女]?$', sex):break
        while True:
            birthday = input('请输入教师出生年月  格式:1900年5月6日>>').strip()
            birthday = re.sub(' ', '', birthday)
            if re.search('^\d{4}年\d\d?月\d\d?日$', birthday):break
        username = name
        password = '123456'
        school_obj_dic = AdminRights.show_school()
        while True:
            choice = input('请选择所属学校的序列号>>').strip()
            if choice in school_obj_dic:break
        school_nid = school_obj_dic[choice].nid
        teacher_obj = Teacher(username, password, name, sex, birthday, school_nid)
        school_obj_dic[choice].teacher_list.append(teacher_obj.nid)
        school_obj_dic[choice].save()
        teacher_obj.save()
        print('\033[1;33m老师[%s]所属学校[%s]创建成功\033[0m' % (name, choice))

    @staticmethod
    def show_teacher():
        """显示老师"""
        obj_list = Teacher.get_all_obj_list()
        if obj_list:
            AdminRights.show(obj_list)
        else:
            print('\033[1;31m老师尚未创建\033[0m'.center(60, '-'))

    @staticmethod
    def have_classes():
        """创建班级"""
        # 第一步选择学校
        school_obj_dic = AdminRights.show_school()
        while True:
            choice = input('请选择班级所属学校的序列号>>')
            if choice in school_obj_dic:
                break
        school_obj = school_obj_dic[choice]
        print('学校[%s-%s校区]开始创建班级'.center(60, '-') % (school_obj.name, school_obj.addr))
        school_obj.create_classes()

    @staticmethod
    def show_classes():
        """显示所有班级"""
        school_obj_list = School.get_all_obj_list()
        if school_obj_list:
            for obj in school_obj_list:
                print('%s-%s校区所有班级如下'.center(60, '-') % (obj.name, obj.addr))
                if obj.classes_list:
                    classes_obj_list = BaseModel.get_obj_list(Classes.db_path, obj.classes_list)
                    for classes in classes_obj_list:
                        course_obj = BaseModel.get_obj_list(Course.db_path, [classes.course_nid])[0]
                        teacher_obj = BaseModel.get_obj_list(Teacher.db_path, [classes.teacher_nid])[0]
                        print('''\033[1;33m班级:[%s] 课程:[%s] 学费:[%s元] 导师[%s]
                        周期:[%s] 学员人数:[%s]\033[0m'''.center(60, '-')
                              % (classes.name,
                                 course_obj.name,
                                 course_obj.price,
                                 teacher_obj.name,
                                 course_obj.period,
                                 str(len(classes.student_list))))
                else:
                    print('\033[1;31m学校[%s-%s校区]尚未创建班级!!!\033[0m' % (obj.name, obj.addr))
        else:
            print('\033[1;31m学校尚未创建,先创建学校!!!\033[0m'.center(60, '-'))

    @staticmethod
    def show(obj_list):
        """
        显示学生,教师通用方法
        :param obj_list:
        """
        for obj in obj_list:
            age = obj.get_age()
            school_boj = School.get_obj_list(School.db_path, [obj.school_nid])[0]
            print('\033[1;33m姓名:%s 性别:%s 年龄:%s 所属校区:%s-%s校区 编号:%s\033[0m'.center(60, '-')
                  % (obj.name, obj.sex, age, school_boj.name, school_boj.addr, obj.nid))

    @staticmethod
    def show_student():
        """显示学生"""
        obj_list = Student.get_all_obj_list()
        if obj_list:
            AdminRights.show(obj_list)
        else:
            print('\033[1;31m学生尚未注册\033[0m'.center(60, '-'))


class TeacherRights(BaseRights):
    """老师操作"""
    @staticmethod
    def teacher_login():
        return BaseRights.login(Teacher.get_all_obj_list())


class StudentRights(BaseRights):
    """学生操作"""
    @staticmethod
    def student_login():
        return BaseRights.login(Student.get_all_obj_list())

    @staticmethod
    def student_enroll():
        """学生注册"""
        print('开始学生注册账户'.center(60, '-'))
        username_list = []
        for obj in Student.get_all_obj_list():
            username_list.append(obj.username)
        while True:
            username = input('请输入用户名>>').strip()
            if re.search('[ ]+', username):continue
            if len(username) != 0:
                if username not in username_list:
                    while True:
                        password = input('请输入密码,只能是字母和数字,6-10位>>').strip()
                        if re.search('[ ]+', password):continue
                        if re.search('^(?!([a-zA-Z]+|\d+)$)[a-zA-Z\d]{6,10}$', password):break
                    while True:
                        name = input('请输入名字>>').strip()
                        if re.search('[ ]+', name):continue
                        if len(username) != 0:break
                    while True:
                        sex = input('请输入性别>>').strip()
                        if re.search('[ ]+', sex):continue
                        if re.search('^[男女]?$', sex):break
                    while True:
                        birthday = input('请输入生日>>').strip()
                        birthday = re.sub(' ', '', birthday)
                        if re.search('^\d{4}年\d\d?月\d\d?日$', birthday):break
                    school_obj_dic = AdminRights.show_school()
                    while True:
                        choice = input('请选择学校序列号>>').strip()
                        if choice in school_obj_dic:break
                    school_obj = school_obj_dic[choice]
                    Student(username, password, name, sex, birthday, school_obj.nid).save()
                    print('\033[1;33m学生账户[%s]学生姓名[%s] 所属学校[%s-%s校区] 创建成功!\033[0m'.center(60, '-')
                          % (username, name, school_obj.name, school_obj.addr))
                    exit()
                else:
                    print('\033[1;31m用户已存在!\033[0m')
