from flask import Flask, render_template, request
from flask_login import login_required, current_user

from cs50 import SQL

app = Flask(__name__)

db = SQL("sqlite:///users.db")

@app.route("/")
def homepage():
	return render_template("homepage.html")

@app.route("/transactions")
def transactions():
	rows = db.execute("""
		SELECT info.firstName, info.lastName, info.id, actions.action, transactions.amount 
		FROM info 
		inner join transactions on info.id = transactions.id 
		inner join actions on transactions.action = actions.id
		""")	
	# print(rows)
	length = len(rows)
	return render_template("index.html", rows=rows, length=length)

@app.route("/info")
def info():
	q = request.args.get("q")
	rows = db.execute(f"""
		SELECT info.firstName, info.lastName, info.id, actions.action, transactions.amount 
		FROM info 
		inner join transactions on info.id = transactions.id 
		inner join actions on transactions.action = actions.id 
		WHERE info.id in
		(Select id FROM info where firstName like '%{q}%' or 
		lastName like '%{q}%')
		""")
	length = len(rows)
	return render_template("index.html", rows=rows, length=length)

@app.route("/registers", methods=["POST"])
def registers():
	firstName = request.form.get("firstName").lower()
	lastName = request.form.get("lastName").lower()
	email = request.form.get("email").lower()
	birthDate = request.form.get("birthDate")
	password = request.form.get("password")
	birthYear = birthDate[:4]
	db.execute(f"""
		INSERT Into Info(
		email, lastName, firstName, birthYear, password) 
		values('{email}', '{lastName}', '{firstName}', {birthYear}, '{password}'
		);
		""")
	# q = request.args.get("q", name)
	rows = db.execute("""
		SELECT info.firstName, info.lastName, info.id, actions.action, transactions.amount 
		FROM info 
		inner join transactions on info.id = transactions.id 
		inner join actions on transactions.action = actions.id
		""")	
	return render_template("index.html", rows=rows)


@app.route("/user/<int:user_id>")
def user(user_id):
	amounts = [0,0,0,0]
	# id = request.form.get("id")
	id = user_id
	users = db.execute(f"SELECT * from info WHERE id = {id};")
	action = db.execute(f"SELECT * from transactions WHERE id = {id};")
	recent = db.execute(f"SELECT * FROM transactions where id = {id} ORDER BY DATE DESC LIMIT 0,1;")
	amounts[0] = db.execute(f"select sum(amount) from transactions where action = 1 and id = {id};")
	amounts[1] = db.execute(f"select sum(amount) from transactions where action = -1 and id = {id};")
	amounts[2] = db.execute(f"select sum(amount) from transactions where action = 0 and id = {id};")
	amounts[3] = amounts[0][0]["sum(amount)"] + amounts[2][0]["sum(amount)"] - amounts[1][0]["sum(amount)"]
	return render_template("user.html", users=users, recent=recent, amounts=amounts)


@app.route("/register")
def register():
	return render_template("register.html")


@app.route("/loginPage")
def loginPage():
	return render_template("loginPage.html")	

