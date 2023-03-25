from flask import Blueprint, render_template, request ,flash

auth = Blueprint('auth',__name__)


@auth.route('/login',methods=['GET','POST'])
def login():
    return render_template("login.html", boolean =True)


@auth.route('/logout')
def logout():
    return '<p>Log Out</p>'


@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash("Email must be greater than 4 Characters.",category='error')
        elif len(firstName) < 1:
            flash("FirstName must be greater than 1 Characters.",category='error')
        elif password1 != password2:
            flash("Passwords Don't match.",category='error')
        elif len(password1) < 7:
            flash("Password must be greater than 7+ Characters.",category='error')
        else:
            flash("Account created!",category='success')

            
    return render_template("sign_up.html")