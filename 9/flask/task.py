from flask import Flask, render_template

app = Flask(__name__)

# @app.route("/")
# @app.route("/<name>/")
# def hello_world(name="незнакомец"):
#     return f"Привет, {name}"

# @app.route("/")
# @app.route("/<password>/")
# def hello_world(password=None):
#     if password == "1234":
#         return f"Доступ разрешён"
#     else:
#         return f"Доступ запрещён"

# @app.route("/")
# def hello_world():
#     html = """
#     <h1>Тестовый запуск локального сервера</h1>
#     <p>А это просто текст</p>
#     """
#     return html

# @app.route("/")
# def hello_world():
#     return flask.render_template() # Внутри () пишем название html-файла в кавычках

@app.route("/")
def hello_world():
    return render_template("index.html") # Внутри () пишем название html-файла в кавычках


if __name__ == "__main__":
    app.run()