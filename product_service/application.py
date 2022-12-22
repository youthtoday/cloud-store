import boto3
import pymysql
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request

search_url = "http://Cloudsearch-env.eba-gr976pa4.us-east-1.elasticbeanstalk.com/elasticsearch"
topic_arn = "arn:aws:sns:us-east-1:964216032660:6156_to_lambda"

pymysql.install_as_MySQLdb()

application = Flask(__name__)
# ------------------database----------------------------
application.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://root:dbuserdbuser@e6156.ck7gj29hlh1f.us-east-1.rds.amazonaws.com:3306' \
                                 '/store_product'
# 指定数据库文件
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 允许修改跟踪数据库
db = SQLAlchemy(application)


class Products(db.Model):
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
    __tablename__ = 'product_picture'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    product_picture = db.Column(db.String(200))
    intro = db.Column(db.Text)


class Categories(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(20))


class Carousels(db.Model):
    __tablename__ = 'carousel'
    carousel_id = db.Column(db.Integer, primary_key=True)
    img_path = db.Column(db.String(200))
    describes = db.Column(db.String(50))
    product_id = db.Column(db.Integer)
    priority = db.Column(db.Integer)


# query all carousel data
def select_all():
    carousels = Carousels.query.all()
    carousels_list = []
    for carousel in carousels:
        dic = {}
        dic['carousel_id'] = carousel.carousel_id
        dic['img_path'] = carousel.img_path
        dic['describes'] = carousel.describes
        dic['product_id'] = carousel.product_id
        dic['priority'] = carousel.priority
        carousels_list.append(dic)
    return carousels_list


# 查询所有
def select_all_products():
    product_list = []
    products = Products.query.all()
    # 类似于 select * from Books
    for s in products:
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
        product_list.append(dic)
    return product_list


def select_pictures_by_product_id(product_id):
    picture_list = []
    pictures = Pictures.query.filter_by(product_id=product_id).all()
    for s in pictures:
        dic = {}
        dic['id'] = s.id
        dic['product_id'] = s.product_id
        dic['product_picture'] = s.product_picture
        dic['intro'] = s.intro
        picture_list.append(dic)
    return picture_list


# 查询所有类别
def select_all_categories():
    category_list = []
    categories = Categories.query.all()
    for s in categories:
        dic = {}
        dic['category_id'] = s.category_id
        dic['category_name'] = s.category_name
        category_list.append(dic)
    return category_list


# 查询类别id
def select_id_by_name(category_name):
    pair = Categories.query.filter_by(category_name=category_name).first()
    return pair.category_id


# 按多类别查询
def select_all_by_categories(category_id):
    products = Products.query.filter(Products.category_id.in_(category_id)).all()
    return products


# 根据id查找
def select_by_id(product_id):
    product = Products.query.get(product_id)
    return product


# 首页类别
def select_7_by_category_name(category_name):
    products = Products.query.filter_by(category_name=category_name).order_by(-Products.product_sales).all()
    return products[0:min(7, len(products))]


# 首页热门
def select_7_by_category_names(category_names):
    products = Products.query.filter(Products.category_name.in_(category_names)).order_by(-Products.product_sales).all()
    return products[0:min(7, len(products))]


@application.route('/product/detail', methods=['POST'])
def query_by_id():
    product_id = request.get_json().get('productID')
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
    res = {
        'code': '001',
        'data': dic
    }
    return res


@application.route('/product/setNum', methods=['POST'])
def product_set_number():
    req = request.get_json()
    product_name = req.get('product_name')
    product_num = req.get('product_num')
    product_list = select_all_products()
    for p in product_list:
        if p['product_name'] == product_name:
            product = Products.query.get(p['product_id'])
    product.product_num = product_num
    db.session.commit()
    res = {'code': '001',
           'msg': 'Product number set successfully!'}
    return res


@application.route('/product/bycategory', methods=['POST'])
def query_product_bycategory():
    req = request.get_json()
    category_ids = req.get('categoryID')
    current_page = req.get('currentPage')
    page_size = req.get('pageSize')
    products = select_all_by_categories(category_ids)
    total = len(products)
    products = products[(current_page - 1) * page_size: min(current_page * page_size, len(products))]

    product_list = []
    for s in products:
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
        product_list.append(dic)

    response = {'code': '001'}
    response['data'] = product_list
    response['total'] = total
    return response


@application.route('/product/hots', methods=['POST'])
def query_7_hot():
    category_names = request.get_json().get('categoryName')
    products = select_7_by_category_names(category_names)
    product_list = []
    for s in products:
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
        product_list.append(dic)
    res = {'code': '001',
           'data': product_list}
    return res


@application.route('/product/category/list', methods=['POST'])
def product_category_list():
    categories = select_all_categories()
    response = {"code": "001",
                'data': categories}
    return response


@application.route('/product/promo', methods=['POST'])
def query_7():
    category_name = request.get_json().get('categoryName')
    products = select_7_by_category_name(category_name)
    product_list = []
    for s in products:
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
        product_list.append(dic)
    res = {'code': '001',
           'data': product_list}
    return res


@application.route('/category/list', methods=['GET'])
def query_all_categories():
    categories = select_all_categories()
    response = {"code": "001",
                'data': categories}
    return response


@application.route('/category/<categoryName>', methods=['GET'])
def query_category_by_name(categoryName):
    category_name = categoryName
    # category_name = request.get_json().get('categoryName')
    category_id = select_id_by_name(category_name)
    response = {"code": '001'}
    data = {'category_id': category_id,
            'category_name': category_name}
    response['data'] = data
    return response


@application.route('/category/names', methods=['POST'])
def multi_category():
    name_list = request.get_json().get('categoryName')
    id_list = []
    for name in name_list:
        id = select_id_by_name(name)
        id_list.append(id)
    response = {'code': '001',
                'data': id_list}
    return response


@application.route('/product/all', methods=['POST'])
def query_all():
    request_data = request.get_json()
    category_ids = request_data.get('categoryID')
    current_page = request_data.get('currentPage')
    page_size = request_data.get('pageSize')
    products = []
    if len(category_ids) == 0:
        products = Products.query.all()
    else:
        products = select_all_by_categories(category_ids)
    total = len(products)
    products = products[(current_page - 1) * page_size: min(current_page * page_size, len(products))]
    product_list = []
    for s in products:
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
        product_list.append(dic)

    response = {'code': '001'}
    response['data'] = product_list
    response['total'] = total
    return response


@application.route('/product/pictures', methods=['POST'])
def query_pictures():
    response = {'code': '001'}
    product_id = request.get_json().get('productID')
    pictures = select_pictures_by_product_id(product_id)
    response['data'] = pictures
    return response


@application.route('/carousel/list', methods=['POST'])
def query_carousel():
    data = select_all()
    res = {
        'code': '001',
        'data': data
    }
    return res


@application.route('/product/search', methods=['POST'])
@application.route('/search/product', methods=['POST'])
def product_search():
    keyword = request.get_json().get('search')
    current_page = request.get_json().get('currentPage')
    page_size = request.get_json().get('pageSize')
    params = {"key": keyword}
    response = requests.post(search_url, json=params)
    print(response)
    print(response.text)
    id_list = response.json()['body']
    print(id_list)
    total = len(id_list)
    id_list = id_list[(current_page-1)*page_size: min(page_size*current_page, len(id_list))]
    data = []
    for id in id_list:
        s = select_by_id(id)
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
        data.append(dic)
    return {'code': '001', 'data': data, 'total': total}


@application.route('/feedback', methods=['POST'])
def send_email():
    feedback = request.get_json().get('msg')
    if len(feedback) == 0:
        return {'code': '004', 'msg': 'bad'}

    sns_client = boto3.client('sns')
    # Publish to topic
    sns_client.publish(TopicArn=topic_arn,
                       Message=feedback,
                       Subject="Feedback from An User")
    return {'code': '001', 'msg': 'send success!'}


if __name__ == '__main__':
    application.run(debug=True, port=8000, host='0.0.0.0')
