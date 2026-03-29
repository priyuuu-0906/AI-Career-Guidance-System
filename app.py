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

# 🔥 MAIN LOGIC (UPDATED WITH COLLEGE)
@app.route('/submit_test', methods=['POST'])
def submit_test():
    score = 0
    ability = []
    weakness = []

    correct_answers = {
        'q1': 'a', 'q2': 'b', 'q3': 'a', 'q4': 'a', 'q5': 'a',
        'q6': 'a', 'q7': 'a', 'q8': 'a', 'q9': 'a', 'q10': 'a'
    }

    for q, correct in correct_answers.items():
        user_ans = request.form.get(q)

        if user_ans == correct:
            score += 1
        else:
            if q in ['q1','q3','q4','q5']:
                weakness.append("Technical Skills")
            elif q in ['q2','q9','q10']:
                weakness.append("General Knowledge")
            elif q in ['q6','q7','q8']:
                weakness.append("Personal Skills")

    # Ability
    if score >= 8:
        ability = ["Strong Technical Skills", "Good Problem Solving"]
    elif score >= 6:
        ability = ["Average Technical Skills"]
    else:
        ability = ["Creative Thinking"]

    # Career + Course + College
    if score >= 8:
        career = "Software Developer / AI Engineer"
        course = "B.Tech / B.Sc Computer Science / AI & ML"
        college = "Anna University, SSN College of Engineering, Sri Sairam Engineering College"

    elif score >= 6:
        career = "Data Analyst"
        course = "B.Sc Data Science / Statistics"
        college = "Loyola College, Madras Christian College"

    elif score >= 4:
        career = "Business Manager"
        course = "BBA / MBA"
        college = "Stella Maris College, Guru Nanak College"

    else:
        career = "Graphic Designer"
        course = "B.Des / Visual Communication"
        college = "NIFT Chennai, Loyola College"

    return render_template("result.html",
                           score=score,
                           ability=ability,
                           weakness=weakness,
                           career=career,
                           course=course,
                           college=college)

@app.route('/admin')
def admin():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    conn.close()
    return render_template("admin.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)

