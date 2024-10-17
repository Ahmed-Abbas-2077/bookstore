from flask import Flask, jsonify, request, abort

app = Flask(__name__)

books = [
    {
        'id': 1,
        'title': '1984',
        'author': 'George Orwell',
        'genre': 'Dystopian',
        'price': 9.99
    },
    {
        'id': 2,
        'title': 'Sapiens: A Brief History of Humankind',
        'author': 'Yuval Noah Harari',
        'genre': 'History',
        'price': 12.99
    }
]


def find_book(book_id):
    return next((book for book in books if book['id'] == book_id), None)


@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({'books': books}), 200


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = find_book(book_id)
    if book:
        return jsonify(book), 200
    else:
        abort(404, description="Book not found")


@app.route('/books', methods=['POST'])
def add_book():
    if not request.json:
        abort(400, description="Request must be JSON")

    new_id = books[-1]['id'] + 1 if books else 1
    new_book = {
        'id': new_id,
        'title': request.json.get('title'),
        'author': request.json.get('author'),
        'genre': request.json.get('genre'),
        'price': request.json.get('price')
    }

    if not all([new_book['title'], new_book['author'], new_book['genre'], new_book['price']]):
        abort(400, description="Missing fields in request data")

    books.append(new_book)
    return jsonify(new_book), 201


@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = find_book(book_id)
    if not book:
        abort(404, description="Book not found")

    if not request.json:
        abort(400, description="Request must be JSON")

    book['title'] = request.json.get('title', book['title'])
    book['author'] = request.json.get('author', book['author'])
    book['genre'] = request.json.get('genre', book['genre'])
    book['price'] = request.json.get('price', book['price'])

    return jsonify(book), 200


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = find_book(book_id)
    if not book:
        abort(404, description="Book not found")

    books.remove(book)
    return jsonify({'result': True}), 200

# Error handlers


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': error.description}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': error.description}), 400


if __name__ == '__main__':
    app.run(debug=True)
