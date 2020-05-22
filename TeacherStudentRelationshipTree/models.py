# 数据库模型
from TeacherStudentRelationshipTree import db
from flask_login import  UserMixin



# 既能够充当数据库进行,query查询;    也能够表示当前登录对象;
# 通过is_authenticated(),is_active(),is_anonymous(),get_id()来对函数处理
class CurrentUser(UserMixin,db.Model):
    account=db.Column(db.String(10),primary_key=True)
    name=db.Column(db.String(30))
    email=db.Column(db.String(40))
    password=db.Column(db.String(16))
    id=db.Column(db.String(10))
    sex=db.Column(db.String(10))
    telephone=db.Column(db.String(11))
    google_scholar_link=db.Column(db.String(100))
    linkedin_link=db.Column(db.String(100))
    allow_modify=db.Column(db.Boolean,default=False)


    def __init__(self,account,name,password,email,id,sex,telephone,google_scholar_link,linkedin_link):
        self.account=account
        self.name=name
        self.password=password
        self.email=email
        self.id=id
        self.sex=sex
        self.telephone=telephone
        self.google_scholar_link=google_scholar_link
        self.linkedin_link=linkedin_link


    # 继承UserMixin的方法
    def get_id(self):
        return self.account

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False



# 建立师生关系表,而不是model
TeachRelation = db.Table('association',
    db.Column('teacher_account', db.String(10), db.ForeignKey('teacher.account')),
    db.Column('student_account', db.String(10), db.ForeignKey('student.account'))
)


class Teacher(db.Model):
    __tablename__='teacher'
    account=db.Column(db.String(10),primary_key=True)
    
    def __init__(self,account):
        self.account=account



class Student(db.Model):
    __tablename__='student'
    account=db.Column(db.String(10),primary_key=True)

    teachers=db.relationship('Teacher',
            secondary=TeachRelation,
            backref=db.backref('students')
	)

    def __init__(self,account):
        self.account=account

