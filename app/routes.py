from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        # Process the order
        pass
    return render_template('order.html')


if __name__ == '__main__':
    app.run(debug=True)
