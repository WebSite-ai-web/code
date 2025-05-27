import os
from flask import Flask, request, render_template_string, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Подключаем базу из переменной окружения DATABASE_URL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
    users = User.query.all()
    return render_template_string('''
        <h1>Добавить пользователя</h1>
        <form method="post">
            <input name="name" placeholder="Введите имя" required>
            <button type="submit">Добавить</button>
        </form>
        <h2>Пользователи:</h2>
        <ul>
        {% for user in users %}
            <li>{{ user.name }}</li>
        {% else %}
            <li>Пользователей нет</li>
        {% endfor %}
        </ul>
    ''', users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)