from flask import Flask, render_template, request, redirect, url_for
from bd import adicionar_usuario  

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/adicionar_usuario', methods=['POST'])
def adicionar_usuario_view():
    username = request.form['username']
    password = request.form['password']
    preference = request.form['preference']
    
    adicionar_usuario(username, password, preference)
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
