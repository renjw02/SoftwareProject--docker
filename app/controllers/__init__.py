# -*- coding: utf-8 -*-

from app.controllers import hello, post, user

blueprints = [
    user.bp,
    hello.bp,
    post.bp
]
