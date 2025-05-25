from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
    # Получение текущей даты и времени
    current_datetime = datetime.now()

    # Форматирование даты и времени для отображения
    formatted_date = current_datetime.strftime('%d.%m.%Y')
    formatted_time = current_datetime.strftime('%H:%M:%S')

    # Передача данных в шаблон
    return render_template('form.html',
                           date=formatted_date,
                           time=formatted_time)


if __name__ == '__main__':
    app.run(debug=True)