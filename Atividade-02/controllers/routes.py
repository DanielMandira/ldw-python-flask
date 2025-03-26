from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import db, Task
from sqlalchemy import func, case

def init_routes(app):
    bp = Blueprint('routes', __name__)

    @bp.route('/')
    def index():
        tasks = Task.query.order_by(Task.start_date.asc()).all()
        return render_template('tasks/index.html', tasks=tasks, now=datetime.utcnow())

    @bp.route('/task/<int:id>')
    def detail(id):
        task = Task.query.get_or_404(id)
        return render_template('tasks/detail.html', task=task)

    @bp.route('/task/create', methods=['GET', 'POST'])
    def create():
        if request.method == 'POST':
            try:
                task = Task(
                    title=request.form['title'],
                    description=request.form['description'],
                    priority=request.form['priority'],
                    status=request.form['status'],
                    start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
                    end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d') if request.form['end_date'] else None,
                    estimated_hours=float(request.form['estimated_hours']) if request.form['estimated_hours'] else None
                )
                db.session.add(task)
                db.session.commit()
                flash('Tarefa criada com sucesso!', 'success')
                return redirect(url_for('routes.index'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar tarefa: {str(e)}', 'danger')
        
        return render_template('tasks/form.html', task=None)

    @bp.route('/task/edit/<int:id>', methods=['GET', 'POST'])
    def edit(id):
        task = Task.query.get_or_404(id)
        if request.method == 'POST':
            try:
                task.title = request.form['title']
                task.description = request.form['description']
                task.priority = request.form['priority']
                task.status = request.form['status']
                task.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
                task.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d') if request.form['end_date'] else None
                task.estimated_hours = float(request.form['estimated_hours']) if request.form['estimated_hours'] else None
                db.session.commit()
                flash('Tarefa atualizada!', 'success')
                return redirect(url_for('routes.detail', id=task.id))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar: {str(e)}', 'danger')
        
        return render_template('tasks/form.html', task=task)

    @bp.route('/task/delete/<int:id>', methods=['POST'])
    def delete(id):
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        flash('Tarefa removida!', 'success')
        return redirect(url_for('routes.index'))

    @bp.route('/dashboard')
    def dashboard():
        # Estatísticas básicas
        total_tasks = Task.query.count()
        completed_tasks = Task.query.filter_by(status='completed').count()
        pending_tasks = Task.query.filter(Task.status.in_(['pending', 'in_progress'])).count()
        
        # Tarefas atrasadas (end_date < hoje e status não é completed)
        overdue_tasks = Task.query.filter(
            Task.end_date < datetime.utcnow(),
            Task.status != 'completed'
        ).count()
        
        return render_template('dashboard.html', stats={
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'overdue_tasks': overdue_tasks
        })
        
    app.register_blueprint(bp)