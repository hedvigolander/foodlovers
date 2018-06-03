# project/users/views.py
from flask import render_template, Blueprint, request, redirect, url_for, flash, abort
from project.models import User
from .forms import RegisterForm, LoginForm, EmailForm, PasswordForm
from sqlalchemy.exc import IntegrityError
from project import db, mail, app
from flask_login import login_user, current_user, login_required, logout_user, fresh_login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from threading import Thread
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime


users_blueprint = Blueprint('users', __name__)

def send_async_email(msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, html_body):
    msg = Message(subject, recipients=recipients)
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[msg])
    thr.start()

def send_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    confirm_url = url_for(
        'users.confirm_email',
        token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
        _external=True)

    html = render_template('email_confirmation.html',confirm_url=confirm_url)

    send_email('Confirm Your Email Address', [user_email], html)

def send_password_reset_email(user_email):
    password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    password_reset_url = url_for(
        'users.reset_with_token',
        token = password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
        _external=True)

    html = render_template(
        'reset_password.html',
        password_reset_url=password_reset_url)

    send_email('Password Reset Requested', [user_email], html)

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.username.data, form.email.data, generate_password_hash(form.password.data), 'user')
                new_user.authenticated = True
                db.session.add(new_user)
                db.session.commit()
                #login_user(new_user)
                send_confirmation_email(new_user.email)
                new_user.email_confirmation_sent_on=datetime.now()
                flash('Thanks for registering!  Please check your email to confirm your email address.', 'success')
                return redirect(url_for('home.index'))
            except IntegrityError:
                db.session.rollback()
                flash('ERROR! Email ({}) already exists.'.format(form.email.data), 'error')
    return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.is_correct_password(form.password.data) and user.is_confirmed():
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash('Thanks for logging in, {}'.format(current_user.email))
                return redirect(url_for('home.index'))
            else:
                flash('ERROR! Incorrect login credentials! Are you sure you have confirmed your email?', 'error')
    return render_template('login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('Goodbye!', 'info')
    return redirect(url_for('home.index'))

@users_blueprint.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except:
        flash('The confirmation link is invalid or has expired.', 'error')
        return redirect(url_for('users.login'))

    user = User.query.filter_by(email=email).first()

    if user.email_confirmed:
        flash('Account already confirmed. Please login.', 'info')
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Thank you for confirming your email address!')

    return redirect(url_for('users.login'))

@users_blueprint.route('/reset', methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first_or_404()
        except:
            flash('Invalid email address!', 'error')
            return render_template('password_reset_email.html', form=form)

        if user.email_confirmed:
            send_password_reset_email(user.email)
            flash('Please check your email for a password reset link.', 'success')
        else:
            flash('Your email address must be confirmed before attempting a password reset.', 'error')
        return redirect(url_for('users.login'))

    return render_template('password_reset_email.html', form=form)

@users_blueprint.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('users.login'))

    form = PasswordForm()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=email).first_or_404()
        except:
            flash('Invalid email address!', 'error')
            return redirect(url_for('users.login'))

        user.password = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_password_with_token.html', form=form, token=token)

@users_blueprint.route('/user')
@login_required
def user_profile():
    return render_template('user_profile.html')

@users_blueprint.route('/admin')
@login_required
def admin_view_users():
    if current_user.role != 'admin':
        return render_template('403.html')

    else:
        users = User.query.order_by(User.id).all()
        return render_template('admin.html', users=users)
    return redirect(url_for('users.login'))
