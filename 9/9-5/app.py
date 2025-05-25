# app.py
from flask import Flask, render_template

# Создаем экземпляр Flask приложения
app = Flask(__name__)

# Маршрут для главной страницы
@app.route('/')
def home():
    return render_template('home.html')

# Маршрут для страницы "О нас"
@app.route('/about')
def about():
    return render_template('about.html')

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)  # debug=True для автоперезагрузки при изменениях