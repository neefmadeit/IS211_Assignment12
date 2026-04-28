
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_key'
DATABASE = 'hw13.db'


def get_db():
    return sqlite3.connect(DATABASE)


def login_required(route):
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return route(*args, **kwargs)
    wrapper.__name__ = route.__name__
    return wrapper


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    students = db.execute('SELECT * FROM students').fetchall()
    quizzes = db.execute('SELECT * FROM quizzes').fetchall()
    db.close()
    return render_template('dashboard.html', students=students, quizzes=quizzes)


@app.route('/student/add', methods=['GET', 'POST'])
@login_required
def add_student():
    error = None
    if request.method == 'POST':
        first = request.form['first_name']
        last = request.form['last_name']
        if not first or not last:
            error = 'All fields required'
        else:
            db = get_db()
            db.execute('INSERT INTO students (first_name,last_name) VALUES (?,?)',(first,last))
            db.commit(); db.close()
            return redirect(url_for('dashboard'))
    return render_template('add_student.html', error=error)


@app.route('/quiz/add', methods=['GET','POST'])
@login_required
def add_quiz():
    error=None
    if request.method=='POST':
        subject=request.form['subject']
        num=request.form['num_questions']
        date=request.form['quiz_date']
        if not subject or not num or not date:
            error='All fields required'
        else:
            db=get_db()
            db.execute('INSERT INTO quizzes(subject,num_questions,quiz_date) VALUES (?,?,?)',(subject,num,date))
            db.commit(); db.close()
            return redirect(url_for('dashboard'))
    return render_template('add_quiz.html', error=error)


@app.route('/result/add', methods=['GET','POST'])
@login_required
def add_result():
    db=get_db()
    students=db.execute('SELECT * FROM students').fetchall()
    quizzes=db.execute('SELECT * FROM quizzes').fetchall()
    error=None
    if request.method=='POST':
        sid=request.form['student_id']
        qid=request.form['quiz_id']
        score=request.form['score']
        if not sid or not qid or not score:
            error='All fields required'
        else:
            db.execute('INSERT INTO results(student_id,quiz_id,score) VALUES (?,?,?)',(sid,qid,score))
            db.commit(); db.close()
            return redirect(url_for('dashboard'))
    db.close()
    return render_template('add_result.html', students=students, quizzes=quizzes, error=error)


@app.route('/student/<int:student_id>')
@login_required
def student_results(student_id):
    db=get_db()
    student=db.execute('SELECT * FROM students WHERE id=?',(student_id,)).fetchone()
    results=db.execute('SELECT quizzes.subject,quizzes.quiz_date,results.score FROM results JOIN quizzes ON results.quiz_id=quizzes.id WHERE results.student_id=?',(student_id,)).fetchall()
    db.close()
    return render_template('student_results.html', student=student, results=results)


if __name__=='__main__':
    app.run(debug=True)
