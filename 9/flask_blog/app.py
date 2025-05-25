from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html', active_page='home')

@app.route('/blog')
def blog():
    # Имитация данных блога
    blog_posts = [
        {
            'id': 1,
            'title': 'Введение в Flask',
            'content': 'Flask — это легкий фреймворк для веб-приложений Python...',
            'date': '10 мая 2023',
            'image': 'blog1.jpg'
        },
        {
            'id': 2,
            'title': 'Работа с шаблонами в Flask',
            'content': 'Шаблоны в Flask используют движок Jinja2, который позволяет...',
            'date': '15 мая 2023',
            'image': 'blog2.jpg'
        },
        {
            'id': 3,
            'title': 'Создание форм в Flask',
            'content': 'Для работы с формами в Flask можно использовать библиотеку Flask-WTF...',
            'date': '20 мая 2023',
            'image': 'blog1.jpg'
        }
    ]
    return render_template('blog.html', active_page='blog', posts=blog_posts)

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', active_page='contacts')

if __name__ == '__main__':
    app.run(debug=True)