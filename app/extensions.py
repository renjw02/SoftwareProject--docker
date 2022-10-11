# -*- coding: utf-8 -*-
"""
Flask 扩展
"""
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
swagger = Swagger()
