from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users(username TEXT,password TEXT)")
        cur.execute("INSERT INTO users VALUES (?,?)",(username,password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template("register.html")

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
        user = cur.fetchone()

        conn.close()

        if user:
            return redirect('/dashboard')
        else:
            return "Invalid Login"

    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/aptitude')
def aptitude():
    return render_template("aptitude.html")
@app.route('/submit_test', methods=['POST'])
def submit_test():

    score = 0

    if request.form['q1'] == "a":
        score += 1

    if request.form['q2'] == "b":
        score += 1

    if request.form['q3'] == "c":
        score += 1

    return render_template("result.html", score=score)

@app.route('/prediction', methods=['POST'])
def prediction():

    skills = request.form['skills'].lower()

    if "coding" in skills:
        career = "Software Developer"
        course = "B.Tech Computer Science"
    elif "maths" in skills:
        career = "Data Analyst"
        course = "B.Sc Data Science"
    elif "design" in skills:
        career = "Graphic Designer"
        course = "B.Des"
    else:
        career = "Career Not Found"
        course = "Explore more skills"

    return render_template("courses.html",career=career,course=course)

@app.route('/admin')
def admin():

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    conn.close()

    return render_template("admin.html",users=users)

if __name__ == "__main__":
    app.run(debug=True)
