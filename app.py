# 因為 Heroku 存取 url 需要使用環境變數，所以import os
import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
print('0003')
app = Flask(__name__)

# 把原本的SQLite換成 PostgresSQL， 因為Heroku上，每隔一段時間它會結束應用，所以建立的資料都不會留下
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# 這段將會去問運作系統 有沒有DATABASE_URL 這個參數，如果我們正在運行Heroku，將會為我們連結上postgre app
# 為了讓在本地端開發的時候 還是可以使用sqlite ，所以把sqlite 的參數放在第二個，如果第一個讀不到才會找第二個）

# 注意: 使用 PostgresSQL 和 原先使用SQLLite 有一個很大的差異，就是使用SQLLite 時 產生的item 所決定歸屬的 store 即便還沒有生成，
# Postman也不會報錯，等到該store 被生成時，之前產生的item 會自動被加進去
# 但是PostgresSQL 並不會，所以在產生item (無論是POST 或 PUT) ，都應該先產生item 將歸屬的 store ，否則Postman會報錯
# 補充 產生的第一個 store 就是id = 1 , 產生的第二個 store 就是id = 2, 以此類推....，所以要產生一個item 設定它 item = 3 ， 必須先新增 Store 三次

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True


# Flask中有个配置属性叫做SECRET_KEY,其作用是：
# Flask（以及相关的扩展extension）需要进行加密
# 所以需要这个密钥SECRET_KEY
# －》之所以需要加密，是因为有些涉及到安全的东西，需要加密
app.secret_key = 'jose'
api = Api(app)

# @app.route('/', methods=['GET', 'POST'])
# def create():
#     return "1234567890", 200


#
# @app.before_first_request
# def create_tables():
#
#     db.create_all()

jwt = JWT(app, authenticate, identity)


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    print('0004')
    db.init_app(app)
    app.run(port=5000, debug=True)
