import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
from flask import make_response, request
import urllib.parse
import boto3

email_validate_key = 'ev-1ba7decf63e83a7766dd5c3d1bfbfe3e'
BASE_URL = "https://github.com/login/oauth/"
api = "https://keimui43t1.execute-api.us-east-1.amazonaws.com"
topic_arn = "arn:aws:sns:us-east-1:964216032660:oauth_sns"

oauth_info = {
    "client_id": "314cedcd6cdb2c77bdb8",
    "client_secret": "b75d75fa91cd8292422f1f1537480fe7bb1915d6",
    "redirect_uri": api + "/oauth/redirect"
}

# initialize user data
user_data = {}

url = 'mysql://root:dbuserdbuser@e6156.ck7gj29hlh1f.us-east-1.rds.amazonaws.com:3306/store_user'

pymysql.install_as_MySQLdb()

application = Flask(__name__)
# ------------------database----------------------------
application.config['SQLALCHEMY_DATABASE_URI'] = url
# 指定数据库文件
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 允许修改跟踪数据库
db = SQLAlchemy(application)


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, comment='自动递增id，唯一键')
    user_name = db.Column(db.String(40), nullable=False, comment='用户名')
    PASSWORD = db.Column(db.String(40), nullable=False, comment='密码')
    email = db.Column(db.String(10), nullable=False, comment='邮箱')
    address = db.relationship('Address', lazy=True)


class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True, comment='自动递增id，唯一键')
    linkman = db.Column(db.String(20), nullable=False, comment='联系人')
    phone = db.Column(db.String(13), nullable=False, comment='手机')
    address = db.Column(db.String(200), nullable=False, comment='地址')
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False, comment='用户id')


def verify_email(email):
    token_url = 'https://api.email-validator.net/api/verify?EmailAddress=' + email + '&APIKey=' + email_validate_key
    res = requests.post(token_url)
    if res.json().get('status') == 200:
        return True
    else:
        return False


# 添加地址
def insert_address(linkman, phone, address, user_id):
    address = Address(linkman=linkman, phone=phone, address=address, user_id=user_id)
    db.session.add_all([address])
    db.session.commit()


def select_address_by_user(user_id):
    users = User.query.get(user_id)
    if not users:
        return False
    addresses = users.address
    address_list = []
    for address in addresses:
        dic = {}
        dic['linkman'] = address.linkman
        dic['phone'] = address.phone
        dic['address'] = address.address
        dic['user_id'] = address.user_id
        address_list.append(dic)
    return address_list


def delete_address(id):
    delete_id = Address.query.get(id)
    if not delete_id:
        return False
    db.session.delete(delete_id)
    db.session.commit()


# 添加用户
def insert_user(user_name, PASSWORD, email):
    user = User(user_name=user_name, PASSWORD=PASSWORD, email=email)
    db.session.add_all([user])
    db.session.commit()


# 通过username查询
def select_user_by_username(user_name):
    user_list = select_user_all()
    for i in range(len(user_list)):
        if user_list[i]['user_name'] == user_name:
            return select_user_by_id(user_list[i]['user_id'])
    return False


# 查询所有
def select_user_all():
    user_list = []
    users = User.query.all()
    for user in users:
        dic = {}
        dic['user_id'] = user.user_id
        dic['user_name'] = user.user_name
        dic['PASSWORD'] = user.PASSWORD
        dic['email'] = user.email
        user_list.append(dic)
    return user_list


# 查询用户是否存在，根据username查询
def select_by_username(username):
    users = User.query.filter_by(user_name=username).all()
    return users


# 通过id查询
def select_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return False
    dic = {}
    dic['user_id'] = user.user_id
    dic['user_name'] = user.user_name
    dic['PASSWORD'] = user.PASSWORD
    dic['email'] = user.email
    return dic


# 通过id删除数据
def delete_user(user_id):
    # 类似于 select * from Books where id = id
    delete_id = User.query.get(user_id)
    if not delete_id:
        return False
    db.session.delete(delete_id)
    db.session.commit()
    # 提交操作到数据库


# 修改数据
def update_user(user_id, user_name='', PASSWORD='', email='', new_id=''):
    user = User.query.get(user_id)
    if not user_name == '':
        user.user_name = user_name
    if not PASSWORD == '':
        user.PASSWORD = PASSWORD
    if not email == '':
        user.email = email
    if not new_id == '':
        user.user_id = new_id
    db.session.commit()


# 解决浏览器浏览器访问输出乱码问题
application.config['JSON_AS_ASCII'] = False


@application.route('/user/check', methods=['POST'])
def check():
    response_object = {'code': '001', 'msg': '用户名不存在，可以注册'}
    if request.method == 'POST':
        post_data = request.get_json()
        print('调用user/check传过来的参数是', post_data)
        if post_data.get('userName') is None:
            response_object['msg'] = 'The message is null!'
            response_object["code"] = '004'
            return response_object
        user_list = select_user_all()
        name_list = []
        for i in range(len(user_list)):
            name_list.append(user_list[i]['user_name'])
        if post_data.get('userName') in name_list:
            response_object['msg'] = 'The username has been used!'
            response_object["code"] = '004'
            return response_object
        else:
            response_object['msg'] = 'The username do not exist!'
            print('The username do not exist!')
            response_object["code"] = '001'
            return response_object

    return response_object


@application.route('/user/register', methods=['POST'])
def add():
    response_object = {'code': '001', 'msg': '注册成功'}
    if request.method == 'POST':
        post_data = request.get_json()
        print('调用user/register传过来的参数是', post_data)
        user_list = select_user_all()
        name_list = []
        for i in range(len(user_list)):
            name_list.append(user_list[i]['user_name'])
        if post_data.get('userName') in name_list:
            response_object['msg'] = 'The username has been used!'
            response_object["code"] = '004'
            return response_object
        if post_data.get('userName') is None:
            response_object['msg'] = 'A username is required!'
            response_object["code"] = '004'
            return response_object
        if post_data.get('password') is None:
            response_object['msg'] = 'A password is required!'
            response_object["code"] = '004'
            return response_object
        if post_data.get('email') is None:
            response_object['msg'] = 'A phone number is required!'
            response_object["code"] = '004'
            return response_object
        username = request.get_json().get('userName'),
        password = request.get_json().get('password'),
        email = request.get_json().get('email')

        if username is None or username == '':
            response_object['msg'] = 'The username cannot be empty！'
            response_object["code"] = '004'
            return response_object
        if password is None or password == '':
            response_object['msg'] = 'The password cannot be empty！'
            response_object["code"] = '004'
            return response_object
        if email is None or email == '':
            response_object['msg'] = 'The email cannot be empty！'
            response_object["code"] = '004'
            return response_object
        if not verify_email(email):
            response_object['msg'] = 'incorrect email'
            response_object["code"] = '004'
            return response_object

        insert_user(user_name=username, PASSWORD=password, email=email)
        response_object['msg'] = 'User added successfully！'

    return response_object


@application.route('/user/login', methods=['POST'])
def login():
    response_object = {'code': '001',
                       'data': {
                           'user_id': 1,
                           'userName': 'admin'
                       },
                       'msg': '注册成功'}
    if request.method == 'POST':
        post_data = request.get_json()
        print('调用login方传过来的参数是：', post_data)
        if post_data.get('userName') is None or post_data.get('password') is None:
            response_object['msg'] = 'data missing'
            response_object['code'] = '004'
            return response_object
        username = request.get_json().get('userName')
        password = request.get_json().get('password')
        if username is None or username == '' or password is None or password == '':
            response_object['msg'] = 'data missing'
            response_object['code'] = '004'
            return response_object

        user_list = select_user_all()
        user_password_dict = {}
        user_id_dict = {}
        for i in range(len(user_list)):
            user_password_dict[user_list[i]['user_name']] = user_list[i]['PASSWORD']
            user_id_dict[user_list[i]['user_name']] = user_list[i]['user_id']
        if username in user_password_dict and user_password_dict[username] == password:
            response_object['msg'] = 'login successfully'
            response_object['code'] = '001'
            response_object['data']['user_id'] = user_id_dict[username]
            response_object['data']['userName'] = username
            return response_object
        else:
            response_object['msg'] = 'wrong username or password'
            response_object['code'] = '004'
            return response_object
    return response_object


@application.route('/user/delete', methods=['POST'])
def delete():
    response_object = {'code': '001', 'msg': '注册成功'}
    if request.method == 'POST':
        post_data = request.get_json()
        print('调用delete方传过来的参数是：', post_data)
        username = post_data.get('user_name')
        user_id = select_user_by_username(username)['user_id']
        delete_user(user_id)  # 删除方法调用

        response_object['msg'] = 'User deleted!'
    return response_object


@application.route('/user/update', methods=['POST'])
def user_update():
    response_object = {'code': '001', 'msg': '更新成功'}
    if request.method == 'POST':
        post_data = request.get_json()
        print('调用/user/update方传过来的参数是：', post_data)
        username = post_data.get('user_name')
        password = post_data.get('password')
        email = post_data.get('email')

        user_id = select_user_by_username(username)['user_id']
        user = User.query.get(user_id)
        user.PASSWORD = password
        user.email = email
        db.session.commit()

        response_object['msg'] = 'User added successfully！'

    return response_object


@application.route('/user/address/list', methods=['POST'])
def list_address():
    response_object = {'code': '001', 'data': []}
    if request.method == 'POST':
        post_data = request.get_json()
        print('调用user/register传过来的参数是', post_data)
        if post_data.get('user_id') is None or post_data.get('user_id') == "":
            response_object['msg'] = 'user_id is required!'
            response_object["code"] = '004'
            return response_object
        addresses = select_address_by_user(post_data.get('user_id'))
        if addresses is False:
            response_object["code"] = '004'
            return response_object
        response_object['data'] = addresses
        return response_object
    return response_object


@application.route('/user/address/save', methods=['POST'])
def add_address():
    response_object = {'code': '001'}
    if request.method == 'POST':
        post_data = request.get_json()

        if post_data.get('add.address') is None or post_data.get('add.linkman') is None or \
            post_data.get('add.phone') is None or post_data.get('user_id') is None:
            response_object["code"] = '004'
            return response_object

        address = post_data.get('add.address')
        linkman = post_data.get('add.linkman')
        phone = post_data.get('add.phone')
        user_id = post_data.get('user_id')

        if address == '' or linkman == '' or phone == '' or user_id == '':
            response_object["code"] = '004'
            return response_object
        insert_address(linkman, phone, address, user_id)
        response_object['msg'] = 'Address added successfully！'
        addresses = select_address_by_user(user_id)
        if addresses is False:
            response_object["code"] = '004'
            return response_object
        response_object['data'] = addresses

    return response_object


@application.route('/user/address/remove', methods=['POST'])
def remove_address():
    response_object = {'code': '001', 'msg': '删除成功'}
    if request.method == 'POST':
        post_data = request.get_json()
        print('调用address/remove方传过来的参数是：', post_data)
        if post_data.get('id') is None or post_data.get('id') == "":
            response_object['msg'] = 'id is required!'
            response_object["code"] = '004'
            return response_object
        id = post_data.get('id')
        result = delete_address(id)  # 删除方法调用
        if result is False:
            response_object['msg'] = 'Could not find the id that needs to be deleted'
            response_object["code"] = '004'
            return response_object
        else:
            response_object['msg'] = 'Address deleted!'
            return response_object


# 主页视图
@application.route('/user/oauth', methods=['GET'])
def index():
    q_string = urllib.parse.urlencode({
        "client_id": oauth_info["client_id"],
        "redirect_uri": oauth_info["redirect_uri"]
    })
    # 组装授权申请地址
    oauth_url = BASE_URL + "/authorize?" + q_string

    data = {
        "code": "001",
        "msg": "success",
        "url": oauth_url
    }

    return data


# 跳转页面视图
@application.route("/oauth/redirect")
def oauth():
    # 获取授权码
    auth_code = request.args.get("code")

    # trigger sqs
    sns_client = boto3.client('sns')
    # Publish to topic
    sns_client.publish(TopicArn=topic_arn,
                       Message=auth_code,
                       Subject="oauth")

    params = {
        "client_id": oauth_info['client_id'],
        "client_secret": oauth_info['client_secret'],
        "code": auth_code
    }
    headers = {
        "accept": "application/json",
    }
    # request token
    res = requests.post(BASE_URL+'access_token', params=params, headers=headers)
    # get token
    token = res.json().get("access_token")
    # mark token
    headers["Authorization"] = "token " + token
    # get user info, API : https://api.github.com/user
    res = requests.get("https://api.github.com/user", headers=headers)
    username = res.json().get('login')
    email = res.json().get('email')
    # 查询用户是否存在，不存在则创建
    users = select_by_username(username)
    # 用户不存在，创建
    if len(users) == 0:
        insert_user(user_name=username, PASSWORD=username, email=email)
    # 创建了，或者已存在，拿user_id
    user_id = select_user_by_username(username)
    # 封装用户信息
    global user_data
    user_data = {
        "code": "001",
        "login": username,
        "user_id": user_id
    }
    return "<h1>You can go back to login!</h1>"


@application.route("/oauth/associate")
def associate():
    username = request.get_json().get('username')
    email = request.get_json().get('email')
    # 查询用户是否存在，不存在则创建
    users = select_by_username(username)
    # 用户不存在，创建
    if len(users) == 0:
        insert_user(user_name=username, PASSWORD=username, email=email)
    # 创建了，或者已存在，拿user_id
    user_id = select_user_by_username(username)
    # 封装用户信息
    global user_data
    user_data = {
        "code": "001",
        "login": username,
        "user_id": user_id
    }
    return {'code': '001', 'data': 'ok'}


@application.route("/oauth/data")
def get_data():
    # return user_data
    global user_data
    user_name = user_data["login"]
    user_id = user_data['user_id']
    data = {
        "code": "001",
        "data": {
            "user_id": user_id,
            "userName": user_name
        },
        "msg": "login success!"
    }
    user_data = {}
    return data


if __name__ == '__main__':
    application.run(debug=True, port=8000, host='0.0.0.0')