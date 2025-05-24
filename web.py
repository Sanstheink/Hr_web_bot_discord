from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100))
    status = db.Column(db.String(100), default="รอรับรองคำขอเข้าเป็นพนักงาน")
    department = db.Column(db.String(100))
    position = db.Column(db.String(100))
    checkin_times = db.Column(db.Text, default="")
    checkout_times = db.Column(db.Text, default="")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def dashboard():
    employees = Employee.query.all()
    return jsonify([{
        'user_id': e.user_id,
        'name': e.name,
        'status': e.status,
        'department': e.department,
        'position': e.position
    } for e in employees])

@app.route('/api/push', methods=['POST'])
def push():
    data = request.json
    emp = Employee.query.filter_by(user_id=data['user_id']).first()
    if not emp:
        emp = Employee(user_id=data['user_id'], name=data['name'])
        db.session.add(emp)
    if data['action'] == 'checkin':
        emp.checkin_times += f"{data['timestamp']}\n"
    elif data['action'] == 'checkout':
        emp.checkout_times += f"{data['timestamp']}\n"
    db.session.commit()
    return jsonify({'message': 'Success'})

@app.route('/api/employee/set_status', methods=['POST'])
@login_required
def set_status():
    data = request.json
    emp = Employee.query.filter_by(user_id=data['user_id']).first()
    if emp:
        emp.status = data['status']
        emp.department = data['department']
        emp.position = data['position']
        db.session.commit()
        return jsonify({'message': 'Updated'})
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/employee/get/<user_id>')
@login_required
def get_employee(user_id):
    emp = Employee.query.filter_by(user_id=user_id).first()
    if emp:
        return jsonify({
            'user_id': emp.user_id,
            'name': emp.name,
            'status': emp.status,
            'department': emp.department,
            'position': emp.position,
            'checkin_times': emp.checkin_times,
            'checkout_times': emp.checkout_times
        })
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=10000)
