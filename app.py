from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# --- Database Connection ---
def get_db_connection():
    connection = pymysql.connect(host='localhost',
                                 user='flaskuser',
                                 password='@Shyam22062003',
                                 database='studentdb',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

# --- Route for the main page, redirects to registration form ---
@app.route('/')
def index():
    return redirect(url_for('register'))

# --- Route for registration form (GET) and submission (POST) ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        course = request.form['course']

        # Insert into database
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO students (name, email, mobile, course) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (name, email, mobile, course))
            connection.commit()
        finally:
            connection.close()
        
        # Redirect to the list of students
        return redirect(url_for('show_students'))
        
    return render_template('register.html')

# --- Route to display all registered students ---
@app.route('/students')
def show_students():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM students"
            cursor.execute(sql)
            students_list = cursor.fetchall()
    finally:
        connection.close()
        
    return render_template('students.html', students=students_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
