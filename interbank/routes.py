from flask import render_template,url_for,flash,redirect,request,abort
from interbank.forms import RegistrationForm,LoginForm,TransferForm
from interbank import app,db,bcrypt
from interbank.models import User,Transfer
from flask_login import login_user, current_user, logout_user, login_required
from apscheduler.schedulers.background import BackgroundScheduler
import atexit




@app.route("/")
@app.route("/home")
def home():
    # posts = Post.query.all()
    return render_template('home.html')


@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("000000000")
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        balance_amount = 10000
        print("00000011111") 
        user = User(username=form.username.data,email=form.email.data,password=hashed_password,
                    account_type=form.account_type.data,bank_name=form.bank_name.data,balance_amount=balance_amount)
        print("22222222222",user)
        db.session.add(user)
        db.session.commit()
        print("33333333")
        flash(f'Account created for {form.username.data}!',"Success")
        return redirect(url_for('login'))

    return render_template('register.html',title='Register',form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    form = TransferForm()
    if form.validate_on_submit():
        transection = Transfer(from_account=form.from_account.data,to_account=form.from_account.data,
                        amount=form.amount.data)
        db.session.add(transection)
        db.session.commit()
        flash(f'Amount transfered!',"Success")
        return redirect(url_for('home'))
    return render_template('transfer.html',form=form)





# def book_appointment(day, slot):
#     if day in available_slots and slot in available_slots[day]:
#         available_slots[day].remove(slot)
#         return True
#     return False

# @app.route('/book', methods=['POST'])
# def book():
#     day = request.form['day']
#     slot = request.form['slot']
#     if book_appointment(day, slot):
#         return f"Appointment booked for {day} at {slot}"
#     else:
#         return f"Failed to book appointment for {day} at {slot}. Slot not available."

def transection_notify():
    transections = Transfer.query.all()
    for trns in transections:
        print(f"{trns} sucessfully completed")

# Create scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=transection_notify, trigger="cron", hour=0)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())
