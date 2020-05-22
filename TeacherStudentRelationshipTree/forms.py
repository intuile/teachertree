# 表单信息
from flask_wtf import FlaskForm
# 表单由若干输入字段组成,每种字段用一种类接收,组成一种类,每种字段作为组合类的一种属性;
from wtforms import StringField, PasswordField, BooleanField, IntegerField, TextAreaField, SubmitField, MultipleFileField ,SelectField,RadioField
from wtforms.validators import DataRequired, Length, ValidationError, Email,InputRequired,NumberRange


# 表单信息要求name相同,而不是同id
# 登录界面的登录登录字段组合形成的类
class LoginForm(FlaskForm):
    account=StringField('Account',validators=[DataRequired()])   # 文本字段
    password=PasswordField('Password',validators=[DataRequired()])   # 密码字段
    submit=SubmitField('Log in')   #提交按钮字段


# 登录界面弹出的注册框
class LoginModalForm(FlaskForm):
    reg_password1=PasswordField('Password1',validators=[DataRequired()])
    reg_password2=PasswordField('Password2',validators=[DataRequired()])
    reg_id=StringField('ID',validators=[DataRequired()])
    reg_btn=SubmitField('Submit')


# 找回密码：验证ID和账号
class VerifyIDAccountForm(FlaskForm):
    account=StringField('Account',validators=[DataRequired()])
    id=StringField('ID',validators=[DataRequired()])
    submit=SubmitField('Submit')


# 修改密码
class ModifyPassword(FlaskForm):
    password1=PasswordField('Password1',validators=[DataRequired()])
    password2=PasswordField('Password2',validators=[DataRequired()])
    submit=SubmitField('Submit')


class AddRelationForm(FlaskForm):
    account=StringField('Account',validators=[DataRequired()])
    T_or_S=RadioField('Relations',choices=[('teacher','teacher'),('student','student')],validators=[DataRequired()])
    submit=SubmitField('Submit')



class UpdateForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    sex=RadioField('Sex',choices=[('man','man'),('woman','woman')])
    phone=StringField('Phone',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired()])
    submit=SubmitField('Submit')



class SelectForm(FlaskForm):
    account=StringField('Account',validators=[DataRequired()])
    submit=SubmitField('Submit')


class DeleteForm(FlaskForm):
    account=StringField('Account',validators=[DataRequired()])
    submit=SubmitField('Submit')