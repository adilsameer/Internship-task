from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

class CreateUserForm(FlaskForm):
    name = StringField("Your Full Name", validators=[DataRequired()])
    email = StringField("Your Email Address", validators=[DataRequired()])
    date_of_birth = StringField("Your Date Of Birth", validators=[DataRequired()])
    gender = StringField("Your Gender", validators=[DataRequired()])

class UpdateUserForm(FlaskForm):
    name = StringField("Your Full Name", validators=[DataRequired()])
    email = StringField("Your Email Address", validators=[DataRequired()])
    date_of_birth = StringField("Your Date Of Birth", validators=[DataRequired()])
    gender = StringField("Your Gender", validators=[DataRequired()])

@app.route("/add_user", methods=['GET', 'POST'])
def add_user():
    form = CreateUserForm()

    if form.validate_on_submit():
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('user_list'))

    return render_template('add_user.html', form=form)

@app.route("/update_user/<int:user_id>", methods=['GET', 'POST'])
def update_user(user_id):
    selected_user = User.query.get_or_404(user_id)
    form = UpdateUserForm(obj=selected_user)

    if form.validate_on_submit():
        selected_user.name = form.name.data
        selected_user.email = form.email.data
        selected_user.date_of_birth = form.date_of_birth.data
        selected_user.gender = form.gender.data

        db.session.commit()

        return redirect(url_for('user_list'))

    return render_template('update_user.html', form=form, selected_user=selected_user)

@app.route("/user_list")
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route("/delete_user/<int:user_id>", methods=['GET', 'POST'])
def delete_user(user_id):
    selected_user = User.query.get_or_404(user_id)

    db.session.delete(selected_user)
    db.session.commit()

    return redirect(url_for('user_list'))

if __name__ == "__main__":
    app.run(debug=True)
