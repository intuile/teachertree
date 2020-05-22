from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


app=Flask('TeacherStudentRelationshipTree')


# 配置
app.config.from_pyfile('settings.py')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager=LoginManager()


# 配置LoginManager, use login manager to manage session
login_manager.session_protection = 'basic'
login_manager.login_view = 'basic'
login_manager.login_message = u"请先登录"
login_manager.init_app(app)


csrf=CSRFProtect()
csrf.init_app(app)



from TeacherStudentRelationshipTree import views
from TeacherStudentRelationshipTree import errors