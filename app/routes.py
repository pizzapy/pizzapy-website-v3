from flask import render_template, request
# filepath: c:\Projects\pizzapy-website-v3\app\routes.py

def configure_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/about')
    def about():
        return render_template('about.html')