from .forms import LoginForm,AddRelationForm,LoginModalForm,VerifyIDAccountForm,ModifyPassword,UpdateForm,SelectForm,DeleteForm
from flask import Flask,render_template,request, url_for, redirect, flash , session 
from TeacherStudentRelationshipTree import app,db,login_manager
from .models import CurrentUser,Teacher,Student,TeachRelation
from flask_login import current_user,login_user,login_required,logout_user
import random



# 10位数账号生成,首字母不为0;
def generate_account():
    a=str(random.randrange(1,10,1)) 
    for i in range(9):
        a=a+str(random.randrange(0,10,1))
    return a


# 调用current_user前,先执行user_loader,传入的数据是session中的id(唯一),将CurrentUser中对应的项作为返回值
@login_manager.user_loader
def load_user(account):
    return CurrentUser.query.get(account)


# 登录页面
@app.route('/login', methods=['GET','POST'])
def basic():
    # 如果已经登录,跳转主页
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    
    # 提交注册信息(前端已经数据验证)
    loginmodalform=LoginModalForm()
    if loginmodalform.validate_on_submit():

        password=loginmodalform.reg_password2.data
        id=loginmodalform.reg_id.data
        account=generate_account()
        while CurrentUser.query.get(account)!=None:
            account=generate_account()
        sex='男'
        google_scholar_link=""
        linkedin_link=""
        name=""
        email=""
        telephone=""

        cur=CurrentUser(account,name,password,email,id,sex,telephone,google_scholar_link,linkedin_link)
        db.session.add(cur)
        db.session.commit()

        #  redirect:重定向,可以避免表单的重复提交
        return redirect(url_for('show_account',account=account))

    
    # 提交登录信息
    loginform=LoginForm()
    if loginform.submit.data and loginform.validate():
        account=loginform.account.data.strip()  
        user=CurrentUser.query.filter_by(account=account, password=loginform.password.data).first()        
        
        # 账号不存在/密码错误
        if user is None:
            flash('username or password is not correct')
            return render_template('login.html',form=loginform,btn=loginform.submit.data)

        else:
            login_user(user)
            session['account']=user.account
            return redirect(url_for('homepage'))
            
    
    #渲染失败信息
    return render_template('login.html',btn=loginform.submit.data,num=CurrentUser.query.count(),form=loginform)




# 接收账号,显示账号
@app.route('/account/<string:account>')
def show_account(account):
    return render_template('account.html',account=account)



# 忘记密码:验证ID和account
@app.route('/forget_password', methods=['GET','POST'])
def forget_pass():
    # 如果已经登录,跳转主页
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    f=VerifyIDAccountForm()
    if  f.validate_on_submit():
        temp_account=f.account.data
        temp_id=f.id.data

        # 查询
        temp_user=CurrentUser.query.filter_by(account=temp_account).first()

        # 用户不存在
        if temp_user is None or temp_id!=temp_user.id:
            flash("account don't match with id")
            return render_template('forget_password.html',form=f)
       
        # 传递account,跳转网页
        else:
            session['temp_account']=temp_account
            return redirect(url_for('modify_password'))

    return render_template('forget_password.html',form=f)


# 修改密码
@app.route('/rewrite_password',methods=['GET','POST'])
def modify_password():
    # 如果已经登录,跳转主页
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    # 获得账号的信息
    temp_user=CurrentUser.query.get(session['temp_account'])
    
    # 修改密码
    m=ModifyPassword()
    if m.validate_on_submit():
        pass1=m.password1.data
        pass2=m.password2.data

        if pass1!=pass2:
            flash('these two password are not the same')
            return render_template('rewrite_password.html',form=m)

        elif not(len(pass1)>=6 and len(pass2)<=16):
            flash('your password length should be between 6 and 16')
            return render_template('rewrite_password.html',form=m)
        
        else:
            temp_user.password=m.password1.data
            db.session.commit()
            # 成功的时候再进行删除,否则失败的时候可能丢失
            session.pop('temp_account', None)

            return redirect(url_for('basic'))

    return render_template('rewrite_password.html',form=m)

    
# 用于传输给前端
class StudentShow():
    def __init__(self):
        account=""
        name=""
        call=""


# 先获取当前账户的account
# 在Teacher表和Student表中先找到个人的account,然后再用对应的属性查找到对应老师/学生的信息
# 获得老师和学生的账号后,可以得到在CurrentUser获得对应的信息
@app.route('/',methods=['GET','POST'])
@login_required
def homepage():
    account=session['account']
    
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    # 为主页传输老师信息
    teachers=[]     #最终的老师信息
    if Student.query.get(account) is not None:
        # 获得老师列表
        teachers_m=Student.query.get(account).teachers

        for i in teachers_m:
            temp_tea_account=i.account

            t=StudentShow()
            t.account=temp_tea_account

            temp_teacher=CurrentUser.query.get(t.account)
            t.call=temp_teacher.telephone
            t.name=temp_teacher.name

            teachers.append(t)

            # return render_template('formal.html',teachers=teachers,account=temp_tea_account,call=temp_teacher.telephone,name=temp_teacher.name)


    # 为主页传输学生信息
    students=[]     #最终的学生信息
    # 获取学生个人信息 students_all
    if Teacher.query.get(account) is not None:

        students_m=Teacher.query.get(account).students

        # 遍历获得students_m的account
        for i in range(len(students_m)):
            temp_stu_account=students_m[i].account
            
            t=StudentShow()
            t.account=temp_stu_account

            temp_student=CurrentUser.query.get(t.account)
            t.call=temp_student.telephone
            t.name=temp_student.name

            students.append(t)
        
        # students的数据不对?   是t的问题还是,关系数据的问题?
    return render_template('formal.html',students=students,teachers=teachers)


# 功能:从表单获取数据,并进行验证;
# 验证条件:看关系是否在数据库关系表中,如果存在,那么无法添加
# 添加时:如果没有重复,那么需要在Student和Teacher中建立对应的item,并且在Student/Teacher的teachers/students中添加对应的item(暂时只添加一项)
@app.route('/add',methods=['GET','POST'])
@login_required
def add():
    account=session['account']
    add_form=AddRelationForm()

    if add_form.validate_on_submit():
        # 获得对方账号
        temp_account=add_form.account.data

        is_repeat=False

        # 判别输入账户是否在数据库中存在  
        op_user=CurrentUser.query.get(temp_account)
        if op_user is None:
            flash('there is no user matching with your input account')
            return redirect(url_for('add'))

        # 检验对方用户是否为自己的老师
        stu=Student.query.get(account)
        if stu is not None:
            for i in stu.teachers:
                if i.account==temp_account:
                    is_repeat=True
                    break

        # 重复存在 , 跳转到该网页 , 弹出模态框 , 然后在前端进行跳转到Homepage
        if is_repeat==True:
            flash('the relation has been exist')
            return redirect(url_for('add'))
            
        # 检验account的老师清单
        tea=Teacher.query.get(account)
        if tea is not None:
            for i in tea.students:
                if i.account==temp_account:
                    is_repeat=True
                    break
        
        if is_repeat==True:
            flash('the relation has been exist')
            return redirect(url_for('add'))


        # 需要先检查学生和老师是否在Student/Teacher中,如果在,只需要append,如果不在,则需要在Student/Teacher中增加该项
        # 如果对方是你的teacher,先在Student和Teacher中建立你的学生项和老师项,先单方面试试效果
        if add_form.T_or_S.data == 'teacher':
            s=Student.query.get(account)
            t=Teacher.query.get(temp_account)

            # 直接append
            if s is not None and t is not None:
                s.teachers.append(t)
                db.session.commit()

            elif s is not None and t is None:
                temp_tea=Teacher(temp_account)
                s.teachers.append(temp_tea)
                db.session.add(temp_tea)
                db.session.commit()
            
            elif s is None and t is not None:
                temp_stu=Student(account)
                t.students.append(temp_stu)
                db.session.add(temp_stu)
                db.session.commit()
            
            else:
                temp_tea=Teacher(temp_account)
                temp_stu=Student(account)
                temp_stu.teachers.append(temp_tea)
                db.session.add(temp_stu)
                db.session.add(temp_tea)
                db.session.commit()
           
            
        else:
            s=Student.query.get(temp_account)
            t=Teacher.query.get(account)

            # 直接append
            if s is not None and t is not None:
                s.teachers.append(t)

            elif s is not None and t is None:
                temp_tea=Teacher(account)
                s.teachers.append(temp_tea)
                db.session.add(temp_tea)
                db.session.commit()
            
            elif s is None and t is not None:
                temp_stu=Student(temp_account)
                t.students.append(temp_stu)
                db.session.add(temp_stu)
                db.session.commit()
            
            else:
                temp_tea=Teacher(account)
                temp_stu=Student(temp_account)
                temp_stu.teachers.append(temp_tea)
                db.session.add(temp_stu)
                db.session.add(temp_tea)
                db.session.commit()
           
        flash('add success')
        return redirect(url_for('add'))
    
    return render_template('add.html',form=add_form)



# 功能:提交表单,并且修改个人的信息
@app.route('/update',methods=['GET','POST'])
@login_required
def update():
    m=UpdateForm()
    account=session['account']

    cur=CurrentUser.query.get(account)

    if m.validate_on_submit():
        
        cur.name=m.name.data
        cur.email=m.email.data
        cur.telephone=m.phone.data
        cur.sex=m.sex.data

        db.session.commit()

        flash('update success')
        return redirect(url_for('update'))

    return render_template('update.html',form=m,user=cur)
        


# 功能:输入对方的账号,进行搜索并且返回结果   可能出现结果不存在,那么需要弹出提示框
@app.route('/select',methods=['GET','POST'])
@login_required
def select():
    f=SelectForm()

    if f.validate_on_submit():
        account=f.account.data

        cur=CurrentUser.query.get(account)
        
        if cur is None:
            flash('Your input account is None')
            return redirect(url_for('select'))
        
        else:
            return render_template('select.html',form=f,user=cur)
    
    return render_template('select.html',form=f,user=[])



# 功能:输入对方的账号,如果存在关系,那么就删除关系,并且弹出删除成功的提示   ,否则弹出关系不存在的提示
# 关系是删除双方?
@app.route('/delete',methods=['GET','POST'])
@login_required
def delete():
    f=DeleteForm()
    account=session['account']  

    if f.validate_on_submit():
        # 对方账号,查看是否在自己的关系表中
        op_account=f.account.data

        if Student.query.get(account) is not None:

            teacher=Student.query.get(account)
            # 寻找自己的老师列表
            for i in teacher.teachers:
                # 找到,删除,弹出提示,跳转
                if i.account==op_account:
                    teacher.teachers.remove(i)
                    db.session.commit()
                    flash('delete successful')
                    return redirect(url_for('delete'))
        
        if Teacher.query.get(account) is not None:

            student=Teacher.query.get(account)
        
            for i in student.students:
                # 找到,删除,弹出提示,跳转
                if i.account==op_account:
                    student.students.remove(i)
                    db.session.commit()
                    flash('delete successful')
                    return redirect(url_for('delete'))
        
        flash('delete failure,because of none relation')
        return redirect(url_for('delete'))
    
    return render_template('delete.html',form=f)


@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    session.pop('account')
    return redirect(url_for('basic'))
	
	
@app.route('/readme',methods=['GET','POST'])
def readme():
	return render_template('readme.html')