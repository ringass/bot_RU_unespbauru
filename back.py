from flask import Flask, render_template, request, redirect, url_for
from bd import inserir_usuario  

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/adicionar_usuario', methods=['POST'])
def adicionar_usuario_view():
    username = request.form['username']
    password = request.form['password']
    preference = request.form['preference']
    janta = request.form.getlist('janta[]')   
    almoco = request.form.getlist('almoco[]')  
    
    print("Janta selecionada:", janta)  
    print("Almoço selecionado:", almoco)  
    
    inserir_usuario(username, password, preference, janta, almoco)
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
