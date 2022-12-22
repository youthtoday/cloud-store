import time
import pymysql
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request

api = "https://keimui43t1.execute-api.us-east-1.amazonaws.com"

pymysql.install_as_MySQLdb()

application = Flask(__name__)
# ------------------database----------------------------
application.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql://root:dbuserdbuser@e6156.ck7gj29hlh1f.us-east-1.rds.amazonaws.com:3306/store_collect'
application.config['SQLALCHEMY_BINDS'] = {
    'product': 'mysql://root:dbuserdbuser@e6156.ck7gj29hlh1f.us-east-1.rds.amazonaws.com:3306/store_product',
    'order': 'mysql://root:dbuserdbuser@e6156.ck7gj29hlh1f.us-east-1.rds.amazonaws.com:3306/store_order',
    'cart': 'mysql://root:dbuserdbuser@e6156.ck7gj29hlh1f.us-east-1.rds.amazonaws.com:3306/store_cart'
}
# 指定数据库文件
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 允许修改跟踪数据库
db = SQLAlchemy(application)


class Collects(db.Model):
    __tablename__ = 'collect'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    collect_time = db.Column(db.Integer)


class Carts(db.Model):
    __bind_key__ = 'cart'
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    num = db.Column(db.Integer)


class Orders(db.Model):
    __bind_key__ = 'order'
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    product_num = db.Column(db.Integer)
    product_price = db.Column(db.Numeric)
    order_time = db.Column(db.Integer)


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


class Pictures(db.Model):
    __bind_key__ = 'product'
    __tablename__ = 'product_picture'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    product_picture = db.Column(db.String(200))
    intro = db.Column(db.Text)


class Categories(db.Model):
    __bind_key__ = 'product'
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(20))


def get_product_name(product_id):
    return Products.query.get(product_id).product_name


def get_product_picture(order):
    return Products.query.get(order.product_id).product_picture


def update_product_num_and_sales(product_id, num):
    product = Products.query.get(product_id)
    product.product_num -= num
    product.product_sales += num


def get_max_num(product_id):
    return Products.query.filter_by(product_id=product_id).first().product_num


# 根据id查找
def select_by_id(product_id):
    product = Products.query.get(product_id)
    return product


def create_order(user_id, products):
    order = Orders()
    order.user_id = user_id
    order.product_id = products['productID']
    order.product_num = products['num']
    order.product_price = products['price']
    order.order_time = int(time.time())
    order.order_id = int(str(user_id)+str(int(time.time())))
    db.session.add(order)
    db.session.commit()


@application.route('/order/list', methods=['POST'])
def order_list():
    user_id = request.get_json().get('user_id')
    orders = Orders.query.filter_by(user_id=user_id).all()
    s = set()
    for order in orders:
        s.add(order.order_id)
    datas = []
    for order_id in s:
        sub_orders = Orders.query.filter_by(order_id=order_id).all()
        data = []
        for order in sub_orders:
            product_id = order.product_id
            product_name = get_product_name(product_id)
            product_picture = get_product_picture(order)
            dict = {}
            dict['id'] = order.id
            dict['order_id'] = order.order_id
            dict['user_id'] = order.user_id
            dict['product_id'] = order.product_id
            dict['product_num'] = order.product_num
            dict['product_price'] = order.product_price
            dict['order_time'] = order.order_time
            dict['product_name'] = product_name
            dict['product_picture'] = product_picture
            data.append(dict)
        datas.append(data)
    dic = {'code': '001', 'data': datas}
    return jsonify(dic)


@application.route('/order/save', methods=['POST'])
def order_save():
    user_id = request.get_json().get('user_id')
    products = request.get_json().get('products')
    for product in products:
        # 保存订单
        create_order(user_id, product)
        # 清除购物车
        delete_cart(user_id, product['productID'])
        # 修改库存和销售
        update_product_num_and_sales(product['productID'], product['num'])
    dic = {'code': '001', 'msg': 'purchase success!'}
    return jsonify(dic)


@application.route('/order/remove', methods=['POST'])
def order_remove():
    order_id = request.get_json().get("order_id")
    if order_id is None or order_id == '' or not Orders.query.get(order_id):
        return {'code': '004', 'msg': 'order not exist'}
    else:
        delete_id = Orders.query.get(order_id)
        db.session.delete(delete_id)
        db.session.commit()
    dic = {'code': '001', 'msg': 'deleted'}
    return jsonify(dic)


def check_cart(user_id, product_id):
    carts = Carts.query.filter_by(user_id=user_id).filter_by(product_id=product_id).all()
    if len(carts) == 0:
        return True
    return False


def cart_add(user_id, product_id):
    cart = Carts()
    cart.user_id = user_id
    cart.product_id = product_id
    cart.num = 1
    db.session.add(cart)
    db.session.commit()


def update_cart_num_1(user_id, product_id):
    cart = Carts.query.filter_by(user_id=user_id).filter_by(product_id=product_id).first()
    max_num = get_max_num(product_id)
    if cart.num >= max_num:
        return False
    cart.num += 1
    db.session.commit()
    return True


def update_cart_num(user_id, product_id, num):
    cart = Carts.query.filter_by(user_id=user_id).filter_by(product_id=product_id).first()
    max_num = get_max_num(product_id)
    if num > max_num:
        return False
    cart.num = num
    db.session.commit()
    return True


def query_cart(user_id, product_id):
    cart = Carts.query.filter_by(user_id=user_id, product_id=product_id).first()
    return cart


def query_cart_by_user_id(user_id):
    carts = Carts.query.filter_by(user_id=user_id).all()
    return carts


@application.route('/cart/list', methods=['POST'])
def cart_list():
    # 查询用户对应的购物车数据
    # 查询购物车对应的商品数据
    # 进行数据封装
    # 返回结果即可
    user_id = request.get_json().get('user_id')
    carts = query_cart_by_user_id(user_id)
    cart_list = []
    for cart in carts:
        product_id = cart.product_id
        num = cart.num
        s = select_by_id(product_id)
        cart_id = query_cart(user_id, product_id).id
        dic = {}
        dic['id'] = cart_id
        dic['productID'] = s.product_id
        dic['productName'] = s.product_name
        dic['productImg'] = s.product_picture
        dic['price'] = s.product_selling_price
        dic['num'] = num
        dic['maxNum'] = s.product_num
        dic['check'] = False
        cart_list.append(dic)
    res = {'code': '001', 'data': cart_list}
    return jsonify(res)


def delete_cart(user_id, product_id):
    cart = Carts.query.filter_by(user_id=user_id).filter_by(product_id=product_id).first()
    if not cart:
        return False
    db.session.delete(cart)
    db.session.commit()


@application.route('/cart/update', methods=['POST'])
def cart_update():
    product_id = request.get_json().get('product_id')
    user_id = request.get_json().get('user_id')
    num = request.get_json().get('num')
    status = update_cart_num(user_id, product_id, num)
    if not status:
        dic = {'code': '004', 'msg': 'number is larger than stock'}
        return jsonify(dic)
    dic = {'code': '001', 'msg': 'modify number success!'}
    return jsonify(dic)


@application.route('/cart/remove', methods=['POST'])
def cart_remove():
    product_id = request.get_json().get('product_id')
    user_id = request.get_json().get('user_id')
    delete_cart(user_id, product_id)
    dic = {'code': '001', 'msg': 'remove cart success!'}
    return jsonify({'code': '001', 'msg': 'remove cart success!'})


@application.route('/cart/save', methods=['POST'])
def cart_save():
    # 进行购物车数据保存
    # 初次保存，返回的数量为1
    # 非初次保存，返回002状态码即可，提示已经添加过，前端会自动化数量 + 1
    # 如果超出购物买数量，返回003！
    user_id = request.get_json().get('user_id')
    product_id = request.get_json().get('product_id')
    is_empty = check_cart(user_id, product_id)
    if is_empty:
        cart_add(user_id, product_id)
        s = select_by_id(product_id)
        cart_id = query_cart(user_id, product_id).id
        dic = {}
        dic['id'] = cart_id
        dic['productID'] = s.product_id
        dic['productName'] = s.product_name
        dic['productImg'] = s.product_picture
        dic['price'] = s.product_selling_price
        dic['num'] = 1
        dic['maxNum'] = s.product_num
        dic['check'] = False
        res = {'code': '001', 'data': dic, 'msg': 'add to cart success!'}
        return jsonify(res)
    else:
        status = update_cart_num_1(user_id, product_id)
        if status:
            dic = {'code': '002', 'msg': 'This product was in your cart, number + 1!'}
            return jsonify(dic)
        else:
            dic = {'code': '003', 'msg': 'Can not add, stock is not enough!'}
            return jsonify(dic)


def check_collect(product_id, user_id):
    lists = Collects.query.filter_by(product_id=product_id).filter_by(user_id=user_id).all()
    if len(lists) == 0:
        return True
    return False


def save_collect(product_id, user_id):
    collect = Collects()
    collect.user_id = user_id
    collect.product_id = product_id
    collect.collect_time = int(time.time())
    db.session.add(collect)
    db.session.commit()


def select_collect_by_user(user_id):
    collects = Collects.query.filter_by(user_id=user_id)
    return collects


@application.route('/collect/save', methods=['POST'])
def collect_save():
    product_id = request.get_json().get('product_id')
    user_id = request.get_json().get('user_id')
    # 判断是否存在收藏
    isCheck = check_collect(product_id, user_id)
    # 存在，提示对应的错误
    if not isCheck:
        res = {'code': '004', 'msg': 'You have collected this product!'}
        return res
    # 不存在，添加，并且提示添加成功即可
    save_collect(product_id, user_id)
    res = {'code': '001', 'msg': 'Collect Success!'}
    return jsonify(res)


@application.route('/collect/list', methods=['POST'])
def collect_list():
    user_id = request.get_json().get('user_id')
    collects = select_collect_by_user(user_id)
    collect_list = []
    for collect in collects:
        product_id = collect.product_id
        s = select_by_id(product_id)
        dic = {}
        dic['product_id'] = s.product_id
        dic['product_name'] = s.product_name
        dic['category_id'] = s.category_id
        dic['product_title'] = s.product_title
        dic['product_intro'] = s.product_intro
        dic['product_picture'] = s.product_picture
        dic['product_price'] = s.product_price
        dic['product_selling_price'] = s.product_selling_price
        dic['product_num'] = s.product_num
        dic['product_sales'] = s.product_sales
        dic['category_name'] = s.category_name
        collect_list.append(dic)
    res = {
        'code': '001',
        'data': collect_list
    }
    return jsonify(res)


def remove_collect_by_pair(user_id, product_id):
    collect = Collects.query.filter_by(user_id=user_id).filter_by(product_id=product_id).first()
    db.session.delete(collect)
    db.session.commit()


@application.route('/collect/remove', methods=['POST'])
def collect_remove():
    user_id = request.get_json().get('user_id')
    product_id = request.get_json().get('product_id')
    remove_collect_by_pair(user_id, product_id)
    res = {
        'code': '001',
        'msg': 'remove success!'
    }
    return jsonify(res)


if __name__ == '__main__':
    application.run(port=8000, host='0.0.0.0')
