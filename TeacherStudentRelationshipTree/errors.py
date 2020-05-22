# 错误处理
from flask import render_template
from TeacherStudentRelationshipTree import app

# 通过errorhandler来捕获错误,并且返回错误页面以及错误代码
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
    