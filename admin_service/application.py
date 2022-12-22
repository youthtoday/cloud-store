import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
from flask import request
import time

api = "https://keimui43t1.execute-api.us-east-1.amazonaws.com"
email_validate_key = 'ev-1ba7decf63e83a7766dd5c3d1bfbfe3e'
user_url = 'mysql://root:dbuserdbuser@e6156.ck7gj29hlh1f.us-east-1.rds.amazonaws.com:3306/store_user'
product_url = 'mysql://root:dbuserdbuser@e6156.ck7gj29hlh1f.us-east-1.rds.amazonaws.com:3306/store_product'
order_url = 'mysql://root:dbuserdbuser@e6156.ck7gj29hlh1f.us-east-1.rds.amazonaws.com:3306/store_order'
user_service_url = api
product_service_url = api
order_service_url = api

pymysql.install_as_MySQLdb()


application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = user_url
application.config['SQLALCHEMY_BINDS'] = {
    'product': product_url,
    'order': order_url
}

db = SQLAlchemy(application)


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, comment='自动递增id，唯一键')
    user_name = db.Column(db.String(40), nullable=False, comment='用户名')
    PASSWORD = db.Column(db.String(40), nullable=False, comment='密码')
    email = db.Column(db.String(10), nullable=False, comment='邮箱')


class Products(db.Model):
    __bind_key__ = 'product'
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    category_id = db.Column(db.Integer)
    product_title = db.Column(db.Text)
    product_intro = db.Column(db.Text)
    product_picture = db.Column(db.String(200))
    product_price = db.Column(db.Numeric)
    product_selling_price = db.Column(db.Numeric)
    product_num = db.Column(db.Integer)
    product_sales = db.Column(db.Integer)
    category_name = db.Column(db.String(100))


class Orders(db.Model):
    __bind_key__ = 'order'
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    product_num = db.Column(db.Integer)
    product_price = db.Column(db.Float)
    order_time = db.Column(db.Integer)


def verify_email(email):
    token_url = 'https://api.email-validator.net/api/verify?EmailAddress=' + email + '&APIKey=' + email_validate_key
    res = requests.post(token_url)
    if res.json().get('status') == 200:
        return True
    else:
        return False


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


def select_user_by_username(user_name):
    user_list = select_user_all()
    for i in range(len(user_list)):
        if user_list[i]['user_name'] == user_name:
            return select_user_by_id(user_list[i]['user_id'])
    return False


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


def check_username(username):
    username_list = []
    users = User.query.all()
    for user in users:
        username_list.append(user.user_name)
    return username in username_list


def check_productid(product_id):
    return Products.query.get(product_id)


def check_productname(productname):
    productname_list = []
    products = Products.query.all()
    for product in products:
        productname_list.append(product.product_name)
    return productname in productname_list


@application.route('/admin/user/update', methods=['POST'])
def update_user():
    response_object = {'code': '004', 'msg': '更新失败'}
    if request.method == 'POST':
        post_data = request.get_json()
        print('调用/admin/user/update传过来的参数是', post_data)
        token = post_data.get('token')
        username = post_data.get('user_name')
        password = post_data.get('password')
        email = post_data.get('email')

        if token is None or token != '6156':
            response_object['msg'] = 'wrong token'
            response_object["code"] = '004'
            return response_object
        if username is None or username == '' or password is None or password == '' or email is None or email == '':
            response_object['msg'] = 'missing data'
            response_object["code"] = '004'
            return response_object
        if not verify_email(email):
            response_object['msg'] = 'invalid email'
            response_object["code"] = '004'
            return response_object
        if not check_username(username):
            response_object['msg'] = 'user not exist'
            response_object["code"] = '004'
            return response_object

        data = {
            "user_name": username,
            "password": password,
            "email": email
        }

        response = requests.post(user_service_url+'/user/update', json=data)

        print(response.status_code)
        if response.status_code == 200:
            response_object['msg'] = '更新成功'
            response_object["code"] = '001'
        else:
            response_object['msg'] = 'user service has a problem!'
            response_object["code"] = '004'
        return response_object
    return response_object


@application.route('/admin/user/remove', methods=['POST'])
def delete_user():
    response_object = {'code': '004', 'msg': '删除失败'}
    if request.method == 'POST':
        post_data = request.get_json()
        print('调用/admin/user/update传过来的参数是', post_data)
        token = post_data.get('token')
        username = post_data.get('user_name')
        if token is None or token != '6156':
            response_object['msg'] = 'wrong token'
            response_object["code"] = '004'
            return response_object
        if username is None or username == '':
            response_object['msg'] = 'missing data'
            response_object["code"] = '004'
            return response_object
        if not check_username(username):
            response_object['msg'] = 'user not exist'
            response_object["code"] = '004'
            return response_object

        data = {
            "user_name": username
        }

        response = requests.post(user_service_url + '/user/delete', json=data)
        print(response.status_code)
        if response.status_code == 200:
            response_object['msg'] = '删除成功'
            response_object["code"] = '001'
        else:
            response_object['msg'] = 'user service has a problem!'
            response_object["code"] = '004'
        return response_object
    return response_object


@application.route('/admin/product/setNum', methods=['POST'])
def set_product_number():
    response_object = {'code': '004', 'msg': '添加失败'}
    if request.method == 'POST':
        post_data = request.get_json()
        print('调用/admin/product/setNum传过来的参数是', post_data)
        token = post_data.get('token')
        product_name = post_data.get('product_name')
        product_num = post_data.get('product_num')
        if token is None or token != '6156':
            response_object['msg'] = 'wrong token'
            response_object["code"] = '004'
            return response_object
        if product_name is None or product_name == '' or product_num is None or product_num < 0:
            response_object['msg'] = 'missing data'
            response_object["code"] = '004'
            return response_object
        if not check_productname(product_name):
            response_object['msg'] = 'product not exist'
            response_object["code"] = '004'
            return response_object

        data = {
            "product_name": product_name,
            "product_num": product_num
        }

        response = requests.post(product_service_url + '/product/setNum', json=data)
        print(response.status_code)
        if response.status_code == 200:
            response_object['msg'] = 'setting num of'+product_name+'to'+str(product_num)+', success!'
            response_object["code"] = '001'
        else:
            response_object['msg'] = 'product service has a problem!'
            response_object["code"] = '004'
        return response_object
    return response_object


@application.route('/admin/product/categories', methods=['GET'])
def get_products_categories():
    response_object = {'code': '004', 'data': []}
    if request.method == 'GET':
        response = requests.post(product_service_url + '/product/category/list')
        result = response.json()
        print(response.status_code)
        if response.status_code == 200:
            response_object['data'] = result['data']
            response_object["code"] = '001'
        else:
            response_object['msg'] = 'product service has a problem!'
            response_object["code"] = '004'
        return response_object


@application.route('/admin/order/create', methods=['POST'])
def create_order():
    response_object = {'code': '004', 'msg': 'fail'}
    if request.method == 'POST':
        post_data = request.get_json()
        print('调用/admin/order/create传过来的参数是', post_data)
        username = post_data.get('username')
        product_id = post_data.get('product_id')
        product_num = post_data.get('product_num')

        if username is None or username == '' or product_id is None or product_num is None or product_num < 0:
            response_object['msg'] = 'missing data'
            response_object["code"] = '004'
            return response_object
        if not check_username(username):
            response_object['msg'] = 'user not exist'
            response_object["code"] = '004'
            return response_object
        if not check_productid(product_id):
            response_object['msg'] = 'product not exist'
            response_object["code"] = '004'
            return response_object

        user_id = select_user_by_username(username)['user_id']
        product = Products.query.get(product_id)
        data = {
            "user_id": user_id,
            "products": [{
                "id": int(str(user_id)+str(int(time.time()))),
                "productID": product_id,
                "productName": product.product_name,
                "productImg": product.product_picture,
                "price": product.product_price,
                "num": product_num,
                "maxNum": product.product_num,
                "check": True
            }]
        }

        response = requests.post(order_service_url + '/order/save', json=data)
        print(response.status_code)
        if response.status_code == 200:
            response_object['msg'] = 'success!'
            response_object["code"] = '001'
        else:
            response_object['msg'] = 'order service has a problem!'
            response_object["code"] = '004'
        return response_object
    return response_object


@application.route('/admin/order/remove', methods=['POST'])
def delete_order():
    response_object = {'code': '004', 'msg': 'fail'}
    if request.method == 'POST':
        post_data = request.get_json()
        print('调用/admin/order/remove传过来的参数是', post_data)
        order_id = post_data.get('order_id')

        data = {
            "order_id": order_id
        }

        response = requests.post(order_service_url + '/order/remove', json=data)
        result = response.json()
        print(response.status_code)
        if response.status_code == 200 and result['code'] == '001':
            response_object['msg'] = 'success!'
            response_object["code"] = '001'
        else:
            response_object['msg'] = 'order service has a problem!'
            response_object["code"] = '004'
        return response_object
    return response_object


if __name__ == '__main__':
    application.run(debug=True, port=8000, host='0.0.0.0')
