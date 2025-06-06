from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []
next_id = 1

@app.route('/', methods=['GET', 'POST'])
def index():
    global next_id
    if request.method == 'POST':
        task_content = request.form.get('task')
        if task_content:
            tasks.append({'id': next_id, 'content': task_content})
            next_id += 1
        return redirect(url_for('index'))
    return render_template('index.html', tasks=tasks)

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return "Task not found", 404

    if request.method == 'POST':
        new_content = request.form.get('content')
        if new_content:
            task['content'] = new_content
        return redirect(url_for('index'))

    return render_template('edit.html', task=task)

@app.route('/delete/<int:task_id>')
def delete(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)