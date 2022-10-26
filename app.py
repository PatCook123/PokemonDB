from flask import Flask, render_template
from flask_bootstrap import Bootstrap4
app = Flask(__name__)

bootstrap = Bootstrap4(app)

@app.route('/')
def homepage():  # put application's code here
    return render_template('index.html')

@app.route('/gyms')
def gympage():
    return render_template('gyms.html')


if __name__ == '__main__':
    app.run(port=3000)
