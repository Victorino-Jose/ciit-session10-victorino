from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(200), nullable=False)
  completed = db.Column(db.Boolean, default=False)
    
with app.app_context():
  db.create_all()

@app.route('/', methods=['GET','POST'])
def home():
  if request.method == 'POST':
    task_description = request.form.get('task')
    if task_description:
      # tasks.append( {'description': task_description, 'completed': False})
      new_task = Task(description=task_description)
      db.session.add(new_task)
      db.session.commit()

      return redirect(url_for('home'))
  tasks = Task.query.all() 
  return render_template('index.html', tasks=tasks)

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
  task = Task.query.get(task_id)
  # if 0 <= task_id < len(tasks):
  #   tasks[task_id]['completed'] = True
  if task: 
    if task.completed == True:
      task.completed = False
    else: 
      task.completed = True
    db.session.commit()
  return redirect(url_for('home'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
  # if 0 <= task_id < len(tasks):
  #   tasks.pop(task_id)
  task = Task.query.get(task_id)
  if task: 
    db.session.delete(task)
    db.session.commit()
  return redirect(url_for('home'))

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
  task = Task.query.get(task_id)
  # if request.method == 'POST':
  #     new_description = request.form['description']
  #     tasks[task_id]['description'] = new_description
  #     return redirect(url_for('home'))
  # else: 
  #     task = tasks[task_id]
  #     return render_template('edit_task.html', task=task)
  if request.method == 'POST':
    new_description = request.form['description']
    if task:
      task.description = new_description
      db.session.commit()
    return redirect(url_for('home'))
  else:
    return render_template('edit_task.html', task=task)

if __name__ == '__main__':
  # app.run(debug=True)
  app.run(host='0.0.0.0', port='8080', debug=True)