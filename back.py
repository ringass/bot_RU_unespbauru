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
    janta = request.form.getlist('janta[]')  # Pega a lista de dias selecionados para jantar
    almoco = request.form.getlist('almoco[]')  # Pega a lista de dias selecionados para almoço
    
    print("Janta selecionada:", janta)  # Verifique o que é impresso no console
    print("Almoço selecionado:", almoco)  # Verifique o que é impresso no console
    
    inserir_usuario(username, password, preference, almoco, janta)
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
