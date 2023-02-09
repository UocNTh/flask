from flask import Flask, jsonify , request , make_response
from flask_restful import Resource, Api 
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__ ) 
api = Api(app)

db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class Users(db.Model) : 
    user_id = db.Column(db.Integer, primary_key=True, autoincrement = True )
    user_name = db.Column(db.String(20), nullable = False )
    address = db.Column(db.String(80))
    phone_number = db.Column(db.String(15))
    email = db.Column(db.String(50)) 

class Books(db.Model) : 
    book_id = db.Column(db.Integer, primary_key=True, autoincrement = True )
    book_name = db.Column(db.String(20), nullable = False )
    author = db.Column(db.String(20), nullable = False ) 
    publication_date = db.Column(db.DateTime, default=datetime.now )
    genre= db.Column(db.String(50)) 

with app.app_context():
    db.create_all()
# ------------------------------------------------------------------------------------------------------------------------

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
        new_user = Users(user_name = data['user_name'] , address = data['address'], phone_number = data['phone_number'] , email = data['email']) 
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
# ------------------------------------------------------------------------------------------------------------------------

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
        new_book = Books(book_name = data['book_name'] , author = data['author'], genre = data['genre']) 
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


api.add_resource(UsersList, '/user')
api.add_resource(UserById, '/user/<int:id>')
api.add_resource(BooksList, '/book')
api.add_resource(BookById, '/book/<int:id>')

@app.errorhandler(404) 
def error_405(_error): 
    return make_response(jsonify({'error': 'Not Found'}), 404 )
@app.errorhandler(405) 
def error_405(_error): 
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405 )

if __name__ == "__main__": 
    app.run(debug = True)