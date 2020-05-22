# -*- coding: utf-8 -*-
# 配置文件,开发环境下的环境配置

import os
import sys

from TeacherStudentRelationshipTree import app


# 数据库配置

# 适配OS
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

# app.root_path就是app被创建的位置(__init__.py)
dev_db=prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)


# 安全性配置
SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')


# BOOTSTRAP_SERVE_LOCAL
