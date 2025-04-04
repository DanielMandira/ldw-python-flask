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
        query = Car.query
        
        # Filtros
        categoria = request.args.get('categoria')
        marca = request.args.get('marca')
        ano = request.args.get('ano')
        
        if categoria:
            query = query.filter(Car.categoria == categoria)
        if marca:
            query = query.filter(Car.marca.ilike(f'%{marca}%'))
        if ano:
            query = query.filter(Car.ano == ano)
        
        cars = query.all()
        return render_template('index.html', cars=cars)

    @app.route('/carro/<int:id>')
    def carro(id):
        car = Car.query.get_or_404(id)
        return render_template('carro.html', car=car)

    @app.route('/carro/<int:id>/editar', methods=['GET', 'POST'])
    def editar_carro(id):
        car = Car.query.get_or_404(id)
        
        if request.method == 'POST':
            car.marca = request.form.get('marca')
            car.modelo = request.form.get('modelo')
            car.ano = request.form.get('ano')
            car.descricao = request.form.get('descricao')
            car.potencia = request.form.get('potencia')
            car.categoria = request.form.get('categoria')
            
            file = request.files.get('foto')
            if file and allowed_file(file.filename):
                # Remove a foto antiga
                if car.foto:
                    old_file = os.path.join(app.config['UPLOAD_FOLDER'], car.foto)
                    if os.path.exists(old_file):
                        os.remove(old_file)
                
                # Salva a nova foto
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                car.foto = filename
            
            db.session.commit()
            flash("Carro atualizado com sucesso!", "success")
            return redirect(url_for('carro', id=car.id))
        
        return render_template('editar_carro.html', car=car)

    @app.route('/carro/<int:id>/excluir', methods=['POST'])
    def excluir_carro(id):
        car = Car.query.get_or_404(id)
        
        # Remove a foto do carro
        if car.foto:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], car.foto)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        db.session.delete(car)
        db.session.commit()
        flash("Carro excluído com sucesso!", "success")
        return redirect(url_for('galeria'))

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
