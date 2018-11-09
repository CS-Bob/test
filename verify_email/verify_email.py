# encoding: utf-8
'''
@author: bo

@file: verify_email.py
@time: 2018/11/8/008 18:38
@desc:
'''
from flask import Flask, request, Response, session
import os
import json
from flask_mail import Mail, Message
from flask_restful import Resource, Api

# from useMyDb import users as usersTable
# 开启服务器
app = Flask(__name__)
Myemail = 'xxxxxxxx@qq.com'         # 发送者邮箱
# 配置服务器信息  这里配置邮箱服务信息
app.config.update(
    DEBUG=True,                 # Debug
    MAIL_SUPPRESS_SEND = True,  # 发送邮件，为True则不发送
    MAIL_SERVER='smtp.qq.com',  # 使用qq邮箱服务
    MAIL_PROT=465,              # 端口
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=Myemail,      # 发送者QQ邮箱
    MAIL_PASSWORD='ezeebusnvbvzbdcg',  # 开启qq邮箱smtp时生成的授权码
    MAIL_DEBUG=True)

app.debug = True    # 开启调试模式
mail = Mail(app)    # 开启邮箱服务
api = Api(app)


# 初始化服务器基本响应
@app.route("/")
def index():
    return "起始页"


# 404页面
@app.errorhandler(404)
def page_not_found(error):
    return "not Found", 404

# 使用flask-restful    send_email 接口
class user_send_email(Resource):
    def post(self):
        #获取json
        userEmail = request.form.get('email')
        userVerfication_Code = request.form.get('verification_code')
        #查询邮箱是否存在
        # user = User.query.filter(User.email == userEmail).first()
        if usersTable.select().where(
            usersTable.email == userEmail).count() > 0:
            # sender 发送方，recipients 邮件接收方列表（可以有多个）
            msg = Message(
                "Hi!这是你的验证码 ", sender=Myemail, recipients=[userEmail])
            # msg.body 邮件正文
            msg.body = "这是你的验证码"
            msg.html = '<b>请及时输入验证码</b><br>验证码为：\
            <h1 style=\'color:blue\'> ' + userVerfication_Code + '<h1>'
            mail.send(msg)
            return Response(
                json.dumps({
                    "code": 200,
                    "message": "成功发送验证码"
                }),
                mimetype='application/json')
        else:
            return Response(
                json.dumps({
                    "code": 400,
                    "message": "邮箱不存在"
                }),
                mimetype='application/json')


class user_verify_email(Resource):
    def get(self):
        return app.send_static_file('regist_code.html')
    def post(self):
        #获取用户填写的邮件验证码user_verify_code
        user_verify_code = request.form.get('verify_code')
        # 获取产生的验证码
        verification_code = session.get('img')
        if user_verify_code == verification_code:
            return Response(
                json.dumps({
                    "code": 200,
                    "message": "验证码正确"
                }),
                mimetype='application/json')

        else:
            return Response(
                json.dumps({
                    "code": 400,
                    "message": "验证码错误"
                }),
                mimetype='application/json')

# 验证路由
api.add_resource(user_verify_email, '/user/verify_email/')
api.add_resource(user_send_email, '/user/send_email/')


if __name__ == '__main__':
    app.run()
