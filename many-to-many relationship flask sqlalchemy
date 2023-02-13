from flask import Flask, jsonify , request , make_response
from flask_restful import Resource, Api 
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__ ) 
api = Api(app)

db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DatabaseNhap.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

orders = db.Table('orders', 
                db.Column('user_id', db.Integer , db.ForeignKey('users.user_id')) , 
                db.Column('book_id', db.Integer , db.ForeignKey('books.book_id'))
                )

class Users(db.Model) : 
    user_id = db.Column(db.Integer, primary_key=True, autoincrement = True )
    user_name = db.Column(db.String(50), nullable = False )
    address = db.Column(db.String(80))
    phone_number = db.Column(db.String(12))
    email = db.Column(db.String(100)) 

    mybooks = db.relationship('Books', secondary = orders , backref = 'users') 

    def __init__ (self, user_name, address , phone_number , email ) : 
        self.user_name = user_name 
        self.address = address 
        self.phone_number = phone_number 
        self.email = email 

    def __repr__(self) : 
        return f"user_id: {self.user_id} user_name: {self.user_name}"  

class Books(db.Model) : 
    book_id = db.Column(db.Integer, primary_key=True, autoincrement = True )
    book_name = db.Column(db.String(50), nullable = False )
    author = db.Column(db.String(50), nullable = False ) 
    publication_date = db.Column(db.DateTime, default=datetime.now )
    genre= db.Column(db.String(100)) 

    myusers = db.relationship('Users', secondary = orders , backref = 'books') 

    def __init__ (self, book_name, author , genre ) : 
        self.book_name = book_name 
        self.author = author 
        self.genre = genre 

    def __repr__(self) : 
        return f"book_id: {self.book_id} book_name: {self.book_name}"

with app.app_context():
    db.create_all()
#------------------------------------------------------------------------------------------------------------------------
class UsersList(Resource) : 
    def get(self): 
        users = Users.query.all() 
        output = []
        for user in users : 
            user_data = {} 
            user_data['user_id'] = user.user_id
            user_data['user_name'] = user.user_name
            user_data['address'] = user.address
            user_data['phone_number'] = user.phone_number
            user_data['email'] = user.email 
            output.append(user_data)
        if len(output) > 0 : return jsonify({'users': output}) 
        else : return jsonify({'message': 'None'})

    def post(self): 
        data = request.get_json()
        new_user = Users(data['user_name'] , data['address'], data['phone_number'] , data['email']) 
        db.session.add(new_user)
        db.session.commit() 
        return jsonify({'message':'New user has been created'})

class UserById(Resource): 
    def get(self,id): 
        user = Users.query.get_or_404(int(id)) 
        user_data = {} 
        user_data['user_id'] = user.user_id
        user_data['user_name'] = user.user_name
        user_data['address'] = user.address
        user_data['phone_number'] = user.phone_number
        user_data['email'] = user.email 
        return jsonify({'user': user_data})

    def delete(self,id):
        user = Users.query.get_or_404(int(id)) 
        db.session.delete(user) 
        db.session.commit() 
        return jsonify({'message': 'The user has been deleted'})

    def put(self,id): 
        user = Users.query.get_or_404(int(id)) 
        if not user : return jsonify({'message': 'Not found'}), 404
        data = request.get_json() 
        user.user_name = data['user_name']
        user.address = data['address']
        user.phone_number = data['phone_number']
        user.email = data['email']
        db.session.commit()
        return jsonify({'massage' : 'The changes have been saved'})
#------------------------------------------------------------------------------------------------------------------------
class BooksList(Resource) : 
    def get(self): 
        books = Books.query.all() 
        output = []
        for book in books : 
            book_data = {} 
            book_data['book_id'] = book.book_id
            book_data['book_name'] = book.book_name
            book_data['author'] = book.author
            book_data['publication_date'] = book.publication_date
            book_data['genre'] = book.genre 
            output.append(book_data)
        if len(output) > 0 : return jsonify({'books': output}) 
        else : return jsonify({'message': 'None'})

    def post(self): 
        data = request.get_json()
        new_book = Books(data['book_name'] ,data['author'],data['genre']) 
        db.session.add(new_book)
        db.session.commit() 
        return jsonify({'message':'New book has been created'})

class BookById(Resource): 
    def get(self,id): 
        book = Books.query.get_or_404(int(id)) 
        book_data = {} 
        book_data['book_id'] = book.book_id
        book_data['book_name'] = book.book_name
        book_data['author'] = book.author
        book_data['publication_date'] = book.publication_date
        book_data['genre'] = book.genre 

        return jsonify({'book': book_data})

    def delete(self,id):
        book = Books.query.get_or_404(int(id)) 
        db.session.delete(book) 
        db.session.commit() 
        return jsonify({'message': 'The book has been deleted'})

    def put(self,id): 
        book = Books.query.get_or_404(int(id)) 
        if not book : return jsonify({'message': 'Not found'}), 404
        data = request.get_json() 
        book.book_name = data['book_name']
        book.author = data['author']
        book.publication_date = datetime.utcnow()
        book.genre = data['genre']
        db.session.commit()
        return jsonify({'massage' : 'The changes have been saved'})
#------------------------------------------------------------------------------------------------------------------------
class Order(Resource) : 

    def post(self) :
        data = request.get_json() 
        user = Users.query.get_or_404(int(data['user_id'])) 
        book = Books.query.get_or_404(int(data['book_id']))
        user.mybooks.append(book) 
        db.session.add(user) 
        db.session.commit()

        return jsonify({'message': 'OK'}) 

class User_Order(Resource) : 
    def get(self, id) : 
        # Sach nguoi dung <id> da doc
        user_book = Users.query.get_or_404(int(id)) 
        user_data = {} 
        user_data['user_id'] = user_book.user_id
        user_data['user_name'] = user_book.user_name
        user_data['address'] = user_book.address
        user_data['phone_number'] = user_book.phone_number
        user_data['email'] = user_book.email 
        user_data['mybooks'] = []
        for book in user_book.mybooks : 
            book_data = {} 
            book_data['book_id'] = book.book_id
            book_data['book_name'] = book.book_name
            book_data['author'] = book.author
            book_data['publication_date'] = book.publication_date
            book_data['genre'] = book.genre 
            user_data['mybooks'].append(book_data)

        return jsonify({'user' : user_data})

class Book_Order(Resource) : 
    def get(self, id) : 
        # Sach co nhung nguoi dung <id> da doc 
        book_user  = Books.query.get_or_404(int(id)) 
        book_data = {} 
        book_data['book_id'] = book_user.book_id
        book_data['book_name'] = book_user.book_name
        book_data['author'] = book_user.author
        book_data['publication_date'] = book_user.publication_date
        book_data['genre'] = book_user.genre 
        book_data['myusers'] = []
        for user in book_user.myusers : 
            user_data = {} 
            user_data['user_id'] = user.user_id
            user_data['user_name'] = user.user_name
            user_data['address'] = user.address
            user_data['phone_number'] = user.phone_number
            user_data['email'] = user.email 
            book_data['myusers'].append(user_data)

        return jsonify({'book' : book_data})
#------------------------------------------------------------------------------------------------------------------------
api.add_resource(UsersList, '/users')
api.add_resource(UserById, '/user/<int:id>')
api.add_resource(BooksList, '/books')
api.add_resource(BookById, '/book/<int:id>')
api.add_resource(Order, '/orders') 
api.add_resource(User_Order, '/user/<int:id>/order') 
api.add_resource(Book_Order,'/book/<int:id>/order')
#------------------------------------------------------------------------------------------------------------------------
@app.errorhandler(404) 
def error_405(_error): 
    return make_response(jsonify({'error': 'Not Found'}), 404 )
@app.errorhandler(405) 
def error_405(_error): 
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405 )
    
#------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__": 
    app.run(debug = True)
