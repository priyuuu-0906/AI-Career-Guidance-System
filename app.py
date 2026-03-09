from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ----------------- HOME -----------------
@app.route('/')
def home():
    return render_template("home.html")

# ----------------- REGISTER -----------------
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

# ----------------- LOGIN -----------------
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

# ----------------- DASHBOARD -----------------
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

# ----------------- ADMIN VIEW -----------------
@app.route('/admin')
def admin():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    conn.close()
    return render_template("admin.html", users=users)

# ----------------- LOAD APTITUDE QUESTIONS -----------------
@app.route('/aptitude')
def aptitude():
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, answer TEXT)")
    # Uncomment next block if first time to add 10 questions
    """
    questions = [
        ("5 + 3 = ?", "8"),
        ("12 × 2 = ?", "24"),
        ("15 ÷ 3 = ?", "5"),
        ("7 × 6 = ?", "42"),
        ("9 + 8 = ?", "17"),
        ("20 − 5 = ?", "15"),
        ("3 × 7 = ?", "21"),
        ("18 ÷ 2 = ?", "9"),
        ("14 + 6 = ?", "20"),
        ("10 × 10 = ?", "100")
    ]
    cur.executemany("INSERT INTO questions (question, answer) VALUES (?,?)", questions)
    conn.commit()
    """
    cur.execute("SELECT * FROM questions")
    questions = cur.fetchall()
    conn.close()
    return render_template("aptitude.html", questions=questions)

# ----------------- SUBMIT APTITUDE TEST -----------------
@app.route('/submit_test', methods=['POST'])
def submit_test():
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions")
    questions = cur.fetchall()
    conn.close()

    score = 0
    for q in questions:
        qid = str(q[0])
        correct = q[2]
        user_answer = request.form.get("q" + qid)
        if user_answer == correct:
            score += 1

    # Eligibility based on score
    if score >= 7:
        career = "Software Developer / AI Engineer"
    elif score >= 5:
        career = "Data Analyst"
    else:
        career = "Graphic Designer"

    return render_template("result.html", score=score, career=career)

# ----------------- CAREER PREDICTION -----------------
@app.route('/prediction', methods=['POST'])
def prediction():
    skills = request.form['skills'].lower()

    if "coding" in skills or "programming" in skills:
        career = "Software Developer"
        course = "B.Tech Computer Science"

    elif "maths" in skills or "statistics" in skills:
        career = "Data Analyst"
        course = "B.Sc Data Science"

    elif "design" in skills or "drawing" in skills:
        career = "Graphic Designer"
        course = "B.Des"

    elif "biology" in skills or "medical" in skills:
        career = "Doctor"
        course = "MBBS"

    elif "business" in skills or "management" in skills:
        career = "Business Manager"
        course = "BBA / MBA"

    elif "teaching" in skills or "education" in skills:
        career = "Teacher"
        course = "B.Ed"

    else:
        career = "Career Not Found"
        course = "Explore more skills"

    return render_template("courses.html", career=career, course=course)


if __name__ == "__main__":
    app.run(debug=True)
