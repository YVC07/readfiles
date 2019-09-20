# step-1
from flask import Flask,render_template,request,flash,redirect,url_for
from db_setup import User,Post,Base
from sqlalchemy import create_engine
from sqlalchemy.orm import (sessionmaker,
scoped_session)

from flask import session as login_session
from functools import wraps


engine = create_engine("sqlite:///mydb.db")

Base.metadata.bind=engine
session = scoped_session(
	sessionmaker(bind=engine))

app = Flask(__name__)


def login_required(f):
	@wraps(f)
	def x(*args,**kwargs):
		if 'email' not in login_session:
			return redirect(url_for('login'))
		return f(*args,**kwargs)
	return x


# step-2
@app.route('/')
@app.route('/home')
def home():
	flash('avaliable posts','primary')
	posts = session.query(Post).all()
	return render_template("home.html",posts=posts)


@app.route('/post/<int:post_id>/edit',
	methods=['GET','POST'])
@login_required
def editpost(post_id):
	if request.method == 'POST':
		title = request.form['title']
		image = request.form['image']
		post = session.query(Post).filter_by(
			id=post_id).one_or_none()
		post.title = title
		post.image = image
		session.add(post)
		session.commit()
		flash('post updated successfully','success')
		return redirect(url_for('home'))
	else:
		post = session.query(Post).filter_by(
			id=post_id).one_or_none()
		return render_template('editpost.html',
			post=post)

@app.route("/post/<int:post_id>/delete",
	methods=["POST","GET"])
@login_required
def deletepost(post_id):
	post = session.query(Post).filter_by(
		id=post_id).one_or_none()
	session.delete(post)
	session.commit()#<---
	flash("post deleted successfully",
		  "success")
	return redirect("/")




@app.route("/register",
	methods=["POST","GET"])
def register():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
		user = User(name=name,
			 email=email,
			 password=password
			)
		session.add(user)
		session.commit()
		return "user created successfully"



	else:
		return render_template(
			'register.html')




@app.route('/message/<name>')
def message(name):
	# return 'hello '+name
	return render_template("message.html",name=name)

@app.route("/name/<fname>/<lname>")
def name(fname,lname):
	#implement ur code here
	return render_template("name.html",
		                   fname=fname,
		                   lname=lname)




@app.route('/add/<int:num1>/<int:num2>')
def addition(num1,num2):
	return "addition of {} and {} is {}".format(num1,num2,num1+num2)




@app.route('/<path:test>')
def test(test):
	return str(test)




@app.route('/html')
def home_html():
	return render_template('index.html')


@app.route('/numbers/<int:start>/<int:end>')
def numbers(start,end):
	L=list(range(start,end+1))
	return render_template('numbers.html',numbers=L)


@app.route('/table/<int:rows>/<int:cols>')
def table(rows,cols):
	numbers = []
	n=1
	for i in range(rows):
		t=[]
		for j in range(cols):
			t.append(n)
			n += 1
		numbers.append(t)
	print(numbers)
	return render_template(
		'table.html',
		numbers=numbers)

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=='POST':
		email = request.form['email']
		password = request.form['password'] 
		user = session.query(User).filter_by(
			email=email,password=password
			).one_or_none()
		if user==None:
			flash('Invalid credentials','danger')
			return redirect(url_for('login'))
		login_session['email'] = email
		login_session['name'] = user.name
		flash('welcome '+str(user.name),'success')
		return redirect(url_for('home'))

	return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
	del login_session['email']
	del login_session['name']
	flash(
		'logout success and visit again',
		'success')
	return redirect(url_for('home'))


@app.route('/profile',methods=['POST','GET'])
def profile():
	email = request.form['email']
	password = request.form['password']
	return render_template('profile.html',
	                       email=email)


@app.route("/newpost",methods=["POST","GET"])
@login_required
def newpost():
	if request.method == "POST":
		title = request.form["title"]
		image = request.form["image"]
		user_id = 1
		post = Post(title=title,
					image=image,
					user_id=user_id
			)
		session.add(post)
		session.commit()
		return "successfully posted.."
	else:
		return render_template("newpost.html")

# step-3
if __name__=='__main__':
	app.secret_key='!2335secretbjh'
	app.run(debug=True,port=5000,host='localhost')


