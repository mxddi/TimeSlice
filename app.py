from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'ThisIsSecret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testproject.db'

db = SQLAlchemy(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.String(200), nullable=False)
#     lastname = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(200), nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow())

##########################################################

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     time_blocks = db.relationship('TimeBlock', backref='user', lazy=True)

class TimeBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)
    activity = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)


#########################################

@app.route('/', methods=['POST', 'GET'])
def retrieveTimeblock():

    allTimeblocks = TimeBlock.query.all()  # look for all

    print(allTimeblocks)

    return render_template("index.html", allTimeblocks=allTimeblocks)



@app.route('/show/<int:id>')
def show(id):
    time_block = TimeBlock.query.get(id)

    return render_template("show.html", time_block = time_block)


@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    time_block = TimeBlock.query.get(id)
    if (request.method == 'POST'):
        time_block.activity = request.form['activity']
        time_block.start_time = request.form['start_time']
        start_time = request.form['end_time']

        db.session.commit()
        return redirect('/')
    return render_template("edit.html", time_block = time_block)


@app.route('/delete/<int:id>')
def delete(id):
    event_to_delete = TimeBlock.query.get_or_404(id)
    db.session.delete(event_to_delete)
    db.session.commit()
    return redirect('/')


########################################################

@app.route('/time_block', methods=['POST', 'GET'])
def create_time_block():
    if request.method == 'POST':
        
        data = request.get_json()

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        activity = request.form['activity']

        time_block = TimeBlock( username = username, email = email, password =password, start_time=start_time, end_time=end_time, activity=activity)
        db.session.add(time_block)
        db.session.commit()

        return jsonify(data), 200

    else:
    
        return render_template("createtimeblock.html")

#This is a test!

app.app_context().push()
db.create_all()
app.run(debug=True)
