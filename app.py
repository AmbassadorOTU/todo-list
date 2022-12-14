from flask import Flask, jsonify, redirect, render_template, request, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:PassWord@\
localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    todolist_id = db.Column(db.Integer, db.ForeignKey('todolists.id'),
    nullable=False)

    def __repr__(self) -> str:
        return f'<Todo {self.id} {self.description}, list {self.todolist_id}>'

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

    def __repr__(self) -> str:
        return f'<TodoList {self.id} {self.name} {self.todos}>'


# db.create_all()

@app.route('/lists/<todolist_id>')
def get_list_todos(todolist_id):
    return render_template('index.html',
    lists=TodoList.query.all(),
    active_list=TodoList.query.get(todolist_id),
    todos=Todo.query.filter_by(todolist_id=todolist_id).order_by('id').all())

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', todolist_id=1))

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        # user_input = request.form.get('description', '')
        user_input = request.get_json()['description']
        todo = Todo(description = user_input, completed = False)
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
        body['completed'] = todo.completed
        body['description'] = todo.description
        # return jsonify({
        #     'description': todo.description
        # })
        # return f"submitted successfully"
        # return redirect(url_for('index'))
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort (500)
    if not error:
        return jsonify(body)
        # return jsonify({
        #     'description': todo.description
        # })

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({ 'success': True })

if __name__ == '__main__':
    app.debug = True
    app.run(host="127.0.0.1", port=5000)
