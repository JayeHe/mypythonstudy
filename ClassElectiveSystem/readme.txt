____author___JayeHe

博客地址:http://www.cnblogs.com/JayeHe/p/7062078.html

程序功能介绍:
一.初始化管理员账号
        1.创建管理员账号
        2.删除管理员账号
        3.退出

二.管理员登录操作
        1.创建学校
        2.查看学校
        3.创建课程
        4.查看课程
        5.创建老师      # 创建老师默认密码是123456
        6.查看老师
        7.创建班级      # 以创建时间为参数自动生成班级名'classes-创建时间'
        8.查看班级
        9.查看学生
        10退出

三.老师登录操作
        1.选择班级上课
        2.查看我的学员
        3.修改学员成绩
        4.查看我的收入
        5.修改密码
        6.退出

四.学生注册

五.学生登录操作
        1.选择班级交学费
        2.查看我的信息
        3.修改密码
        4.退出




\ClassElectiveSystem
│  readme.txt
│  __init__.py
│
├─bin
│  │  start.py        # 程序开始入口
│  └─__init__.py
│
├─conf
│  │  settings.py     # 程序配置
│  └─__init__.py
│
├─core
│  │  main.py         # 主程序
│  └─__init__.py
│
├─db
│  │  __init__.py
│  │
│  ├─admin           # 存管理员实例
│  │
│  ├─classes         # 存班级实例
│  │
│  ├─course          # 存课程实例
│  │
│  ├─school          # 存学校实例
│  │
│  ├─student         # 存学生实例
│  │
│  └─teacher         # 存老师实例
│
├─lib
│  │  role_module.py  # 角色类和功能类
│  └─__init__.py
│
├─log
│      __init__.py
│
└─test
        __init__.py


已创建管理员账号
    用户名:hejie
    密码:hejie88
已经创建的学校
    老男孩 北京校区
    老男孩 上海校区
已经创建的课程
    老男孩 北京校区---Python, Linux
    老男孩 上海校区---Go
已创建老师
    用户名:alex
    密码:alex88      
已注册学生
    用户名:koko
    密码:koko88
已创建班级
    班级:[classes-20170619223428]  
    课程:[Python]
    学费:[9800元]
    导师[alex]
    周期:[12]
    学员人数:[1]

