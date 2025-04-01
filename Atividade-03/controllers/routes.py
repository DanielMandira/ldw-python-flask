from flask import render_template, request, redirect, url_for, flash
import os
from models.database import db
from models.car import Car
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_app(app):
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    @app.route('/')
    def galeria():
        cars = Car.query.all()
        return render_template('index.html', cars=cars)

    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():
        if request.method == 'POST':
            marca = request.form.get('marca')
            modelo = request.form.get('modelo')
            ano = request.form.get('ano')
            descricao = request.form.get('descricao')
            potencia = request.form.get('potencia')
            categoria = request.form.get('categoria')
            file = request.files.get('foto')
            
            if not (marca and modelo and ano and file and categoria):
                flash("Preencha todos os campos obrigatórios e selecione uma foto", "danger")
                return redirect(request.url)
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                novo_carro = Car(
                    marca=marca,
                    modelo=modelo,
                    ano=ano,
                    descricao=descricao,
                    potencia=potencia,
                    categoria=categoria,
                    foto=filename
                )
                db.session.add(novo_carro)
                db.session.commit()
                flash("Carro cadastrado com sucesso!", "success")
                return redirect(url_for('galeria'))
            else:
                flash("Formato de arquivo inválido. Use apenas PNG, JPG, JPEG ou GIF", "danger")
                return redirect(request.url)
        
        return render_template('cadastro.html')
