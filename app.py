from flask import Flask, render_template, request, redirect, url_for
from models import db, User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Ensure tables are created before the first request is handled
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        user = User(first_name=first_name, last_name=last_name, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', action='Add', user={})

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    user = User.query.get(id)
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', action='Edit', user=user)

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,port=5001)
