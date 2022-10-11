# -*- coding: utf-8 -*-

from curses.ascii import isalpha, isdigit, islower, isupper
import re


def register_params_check(content):
    """
    TODO: 进行参数检查
    username : 必填，⽤户账号
    password : 必填，⽤户密码 
    nickname : 必填，⽤户昵称 
    url : 必填，⽤户个⼈地址链接 
    mobile : 必填，⼿机号 
    magic_number : 选填，⽤户喜欢的幸运数字
    """
    # 需要解决参数缺失问题
    # username
    if content.get('username', 0):
        username = content['username']
        length = len(username)
        if not (length >= 5 and length <= 12):
            return "wrong username", False
        
        str = r'^[A-Za-z]+\d+$'
        if not re.match(str, username):
            return "wrong username", False 
    else:
        return "can not find username", False

    # password
    if content.get('password', 0):
        password = content['password']
        length = len(password)
        if length >= 8 and length <= 15:
            has_upper = False
            has_lower = False
            has_num = False
            has_sign = False
            for c in password:
                # 是大写
                if isupper(c):
                    if not has_upper:
                        has_upper = True
                # 是小写
                elif islower(c):
                    if not has_lower:
                        has_lower = True
                # 是数字
                elif isdigit(c):
                    if not has_num:
                        has_num = True
                # 是符号
                elif c in ['-', '_', '*', '^']:
                    if not has_sign:
                        has_sign = True
                # 未知符号
                else:
                    return "wrong password", False
            # 四种不全
            if not (has_upper and has_lower and has_num and has_sign):
                return "wrong password", False
        # 长度不对
        else:
            return "wrong password", False
    else:
        return "can not find password", False
    
    # nickname
    if content.get('nickname', 0):
        nickname = content['nickname']
    else:
        return "can not find nickname", False
    

    # url
    if content.get('url', 0):
        url = content['url']
        length = len(url)
        if length > 48:
            return "wrong url", False

        str = r"^(http://|https://)([A-Za-z0-9][A-Za-z0-9-]*[A-Za-z0-9].|[A-Za-z0-9].)+([A-Za-z0-9][A-Za-z0-9-]*[A-Za-z0-9]|[A-Za-z0-9])$"
        if not re.match(str, url):
            return "wrong url", False 
        
        # 最后一段
        sign = url.split('.')[-1]
        if sign[0] == '-' or sign[-1] == '-':
            return "wrong url", False
        has_alpha = False
        for c in sign:
            if isalpha(c):
                has_alpha = True
            elif isdigit(c):
                continue
            elif c == '-':
                continue
            else:
                return "wrong url", False
        if not has_alpha:
            return "wrong url", False
    else:
        return "can not find url", False
        
    # mobile
    if content.get('mobile', 0):
        mobile = content['mobile']
        area_code = mobile[1:3]
        phone_number = mobile[4:]
        if len(phone_number) != 12:
            return "wrong mobile", False
        # + 和 .
        if mobile[0] == '+' and mobile[3] == '.':
            for i in area_code:
                if not isdigit(i):
                    return "wrong mobile", False
            for i in phone_number:
                if not isdigit(i):
                    return "wrong mobile", False
        else:
            return "wrong mobile", False
    else:
        # mobile 缺失
        return "can not find mobile", False
    
    # magic_number
    if content.get('magic_number', 0):
        magic_number = content['magic_number']
    else:
        content['magic_number'] = 0


    return "ok", True


# test = {
#     'username': "a2322002",
#     'password': "6018As00_",
#     'nickname': "gw",
#     'url': "http://192.23.4s2",
#     'mobile': "+86.123482974401",
#     'magic_number': 12
# }

# print (register_params_check(test))