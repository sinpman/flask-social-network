import os
from flask_sqlalchemy import SQLAlchemy
from config_sample import config, interface
from oauth import OAuthSignIn
from flask import (Flask, g, render_template, flash, redirect, url_for,
                   abort)
from flask import request
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user, UserMixin)

import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'
vipMember = '0'
DELETE_Y = int('1')
DELETE_N = int('0')
imageUpload = 'N'
image = ''

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '2117194438572671',
        'secret': '5ce1b0c811e722823a76fe1621f1cd31'
    },
    'twitter': {
        'id': '3RzWQclolxWZIMq5LJqzRZPTl',
        'secret': 'm9TEd58DSEtRrZHpz2EjrV9AhsBRxKMo8m3kuIZj3zLwzwIimt'
    }
}

app.secret_key = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    print('email:' + email)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)

    except models.DoesNotExist:
        return None
    try:
        return User.query.get(int(id))
    except:
        return None

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    print('provider--')
    print(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    print('inside call back')
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    print(username)
    if social_id is None:
        flash('Authentication failed')
        return redirect(url_for('index'))
    try:
        user = models.User.get(models.User.email == email)
    except:
        flash('Authentication failed')
        return redirect(url_for('index'))

    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Yay, you registered!", "success")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('index'))

def upload_image():
    if request.method == 'POST':
        print('me 2')
        # f = request.files['file']
        if request.files.get('file'):
            print('hello')
            f = request.files['file']
            f.save(f.filename)
        else:
            print('none')
            None
        return 'file uploaded successfully'




@app.route('/new_group', methods=('GET', 'POST'))
@login_required
def group():
    global vipMember
    global imageUpload
    global image
    form = forms.PostForm()

    if form.validate_on_submit():
        # models.Post.create(user=g.user.id,
        #                    content=form.content.data.strip(),
        #                    filename='test')
        if 'file' in request.files:
            f = request.files['file']
            print('static/img/' + current_user.username + '/' + f.filename)
            image = 'static/img/' + current_user.username + '/' + f.filename
            models.Post.create(user=g.user.id,
                               content=form.content.data.strip(),
                               filename=f.filename,
                               filepath=image)

            if not os.path.exists('static/img/'+current_user.username+'/'):
                os.makedirs('static/img/'+current_user.username+'/')
            print('post id')
            f.save(image)
            imageUpload='Y'
            flash("Message posted! Thanks!", "success")
            return redirect('/stream/' + str(current_user.username))
        else:
            models.Post.create(user=g.user.id,
                               content=form.content.data.strip())
            imageUpload='N'
            flash("Message posted! Thanks!", "success")
            return redirect('/stream/' + str(current_user.username))
    return render_template('new_group.html', form=form)





@app.route('/new_post', methods=('GET', 'POST'))
@login_required
def post():
    global vipMember
    global imageUpload
    global image
    form = forms.PostForm()

    if form.validate_on_submit():
        # models.Post.create(user=g.user.id,
        #                    content=form.content.data.strip(),
        #                    filename='test')
        if 'file' in request.files:
            f = request.files['file']
            print('static/img/' + current_user.username + '/' + f.filename)
            image = 'static/img/' + current_user.username + '/' + f.filename
            models.Post.create(user=g.user.id,
                               content=form.content.data.strip(),
                               filename=f.filename,
                               filepath=image)

            if not os.path.exists('static/img/'+current_user.username+'/'):
                os.makedirs('static/img/'+current_user.username+'/')
            print('post id')
            f.save(image)
            imageUpload='Y'
            flash("Message posted! Thanks!", "success")
            return redirect('/stream/' + str(current_user.username))
        else:
            models.Post.create(user=g.user.id,
                               content=form.content.data.strip())
            imageUpload='N'
            flash("Message posted! Thanks!", "success")
            return redirect('/stream/' + str(current_user.username))
    return render_template('post.html', form=form)

@app.route('/add_profile', methods=('GET', 'POST'))
@login_required
def addProfile():
    print('inside')
    form = forms.PostForm()
    # if form.validate_on_submit():
    if request.method == 'POST':
        print('two')
        if 'profile' in request.files:
            f = request.files['profile']
            print('img/Profile' + current_user.username + '/' + f.filename)
            image = 'img/Profile/' + current_user.username + '/' + f.filename
            models.user_profile.create(user_id=g.user.id,
                               profile_pic_path=image,
                                       id=g.user.id,
                                       username=current_user.username
                                       )
            print(image)
            if not os.path.exists('img/Profile/'+current_user.username+'/'):
                os.makedirs('img/Profile/'+current_user.username+'/')
            f.save(image)
            flash("Profile picture updated", "success")
            return redirect('/stream/' + str(current_user.username))
    return render_template('profile_pic.html', form=form)

@app.route("/makePayment")
def makePayment():
    return """
        <a href="%s">
            <img src="https://www.paypalobjects.com/en_US/i/btn/btn_xpressCheckout.gif">
        </a>
        """ % url_for('paypal_redirect')

@app.route("/paypal/redirect")
def paypal_redirect():
    kw = {
        'amt': '10.00',
        'currencycode': 'USD',
        'returnurl': url_for('paypal_confirm', _external=True),
        'cancelurl': url_for('paypal_cancel', _external=True),
        'paymentaction': 'Sale'
    }
    setexp_response = interface.set_express_checkout(**kw)
    return redirect(interface.generate_express_checkout_redirect_url(setexp_response.token))

@app.route("/paypal/confirm")
def paypal_confirm():
    getexp_response = interface.get_express_checkout_details(token=request.args.get('token', ''))

    if getexp_response['ACK'] == 'Success':
        return """
            Everything looks good! <br />
            <a href="%s">Click here to complete the payment.</a>
        """ % url_for('paypal_do', token=getexp_response['TOKEN'])
    else:
        return """
            Oh noes! PayPal returned an error code. <br />
            <pre>
                %s
            </pre>
            Click <a href="%s">here</a> to try again.
        """ % (getexp_response['ACK'], url_for('index'))

@app.route("/paypal/do/<string:token>")
def paypal_do(token):
    getexp_response = interface.get_express_checkout_details(token=token)
    kw = {
        'amt': getexp_response['AMT'],
        'paymentaction': 'Sale',
        'payerid': getexp_response['PAYERID'],
        'token': token,
        'currencycode': getexp_response['CURRENCYCODE']
    }
    interface.do_express_checkout_payment(**kw)
    return redirect(url_for('paypal_status', token=kw['token']))

@app.route("/paypal/status/<string:token>")
def paypal_status(token):
    checkout_response = interface.get_express_checkout_details(token=token)
    global vipMember
    if checkout_response['CHECKOUTSTATUS'] == 'PaymentActionCompleted':
        # vip=models.User.select().where(models.User.username ** current_user.username)
        # vip.vip_member='Y'
        vip=models.User.update(vip_member='Y').where(models.User.id == current_user.id)
        vip.execute()
        vipMember = '1'
        flash("Awesome! You have become a VIP member now.", "success")
        return redirect(url_for('index'))
    else:
        vipMember = '0'
        return """
            Oh no! PayPal doesn't acknowledge the transaction. Here's the status:
            <pre>
                %s
            </pre>
        """ % checkout_response['CHECKOUTSTATUS']

@app.route("/paypal/cancel")
def paypal_cancel():
    return redirect(url_for('index'))

@app.route('/')
def index():
    global vipMember
    user_profile = models.user_profile.select().where(
        models.user_profile.username ** 'Karan123').get()
    # a=models.User.select(models.User.vip_member).where((models.User.id == current_user.id) |
    #                                                  (models.User.vip_member.is_null(False))).get()
    #
    # print(current_user.id)
    # print('current_user')
    print(current_user)
    stream = models.Post.select().order_by(models.Post.timestamp.desc()).limit(100)
    return render_template('stream.html', stream=stream, vip=int(vipMember),user_profile=user_profile)


@app.route('/allFollowing')
def allFollowing():
    global vipMember
    stream1 = models.User.select(models.User.id).join(
        models.Relationship, on=models.Relationship.to_user
    ).where(
        models.Relationship.from_user == current_user.id
    )

    stream = models.Post.select().order_by(models.Post.timestamp.desc()).where(models.Post.user.in_(stream1))
    print(stream)
    return render_template('stream.html', stream=stream, vip=int(vipMember))

@app.route('/all_followers/<username>')
@login_required
def all_followers(username=None):
    template = 'all_followers.html'
    user = models.User.select().where(models.User.username ** username).get()
    stream = user.posts.limit(100)
    return render_template(template, stream=stream, user=user)


@app.route('/stream')
@app.route('/stream/<username>')
@login_required
def stream(username=None):
    global image
    global imageUpload
    if username and username != current_user.username:
        print('username')
        print(username)
        try:
            template = 'user_stream.html'

            Delete = DELETE_N
            user = models.User.select().where(
                models.User.username ** username).get()
            user_profile = models.user_profile.select().where(
                models.user_profile.username ** 'Karan123' ).get()
            print(user_profile)
        except models.DoesNotExist:
            abort(404)
        else:
            stream = user.posts.order_by(models.Post.timestamp.desc()).limit(100)


    if username and username == current_user.username:
        user_profile = models.user_profile.select().where(
            models.user_profile.username ** 'Karan123').get()
        print(user_profile)
        user = models.User.select().where(
            models.User.username ** username).get()
        Delete = DELETE_Y
        template = 'user_stream.html'
        stream = user.posts.order_by(models.Post.timestamp.desc()).limit(100)
        # stream = user.use.order_by(models.Post.timestamp.desc()).limit(100)
        print(stream)
    return render_template(template, stream=stream, user=user, delete=Delete, user_profile=user_profile)

#     template = 'stream.html'
#     if username and username != current_user.username:
#         try:
#             user = models.User.select().where(
#                 models.User.username ** username).get()
#         except models.DoesNotExist:
#             abort(404)
#         else:
#         else:
#             stream = user.posts.limit(100)
#     else:
#         stream = current_user.get_stream().limit(100)
#         user = current_user
#     if username:
#         template = 'user_stream.html'
#     return render_template(template, stream=stream, user=user)



@app.route('/followingPost')
@app.route('/followingPost/<username>')
@login_required
def followingPost(username=None):
    global image
    global imageUpload
    if username and username != current_user.username:
        try:
            template = 'user_stream.html'
            Delete = DELETE_N
            user = models.User.select().where(
                models.User.username ** username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            stream = user.posts.limit(100)
    if username and username == current_user.username:
        user = models.User.select().where(
            models.User.username ** username).get()
        Delete = DELETE_Y
        template = 'user_stream.html'
        stream = user.posts.limit(100)
    return render_template(template, stream=stream, user=user, delete=Delete)






@app.route('/post/<int:post_id>')
def view_post(post_id):
    posts = models.Post.select().order_by(models.Post.timestamp.desc()).where(models.Post.id == post_id)

    user_profile = models.user_profile.select().where(
        models.user_profile.user_id.in_(models.Post.select(models.Post.user_id).order_by(models.Post.timestamp.desc()).where(models.Post.id == post_id)) ).get()

    if posts.count() == 0:
        abort(404)

    # if ()
    # return render_template('stream.html', stream=posts)

    return render_template('stream.html', stream=posts, user_profile =user_profile )


@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    print(post_id)

    models.Post.get(
        id=post_id
    ).delete_instance()
    # posts = models.Post.delete().where(models.Post.id == post_id)
    flash("Post Deleted Successfully", "success")
    return redirect(url_for('stream', username=current_user.username))

    # return render_template('stream.html', stream=posts)


@app.route('/follow/<username>')
@login_required
def follow(username):
    try:
        to_user = models.User.get(models.User.username ** username)
    except models.DoesNotExist:
        abort(404)
    else:
        try:
            models.Relationship.create(
                from_user=g.user._get_current_object(),
                to_user=to_user
            )
        except models.IntegrityError:
            pass
        else:
            flash("You're now following {}!".format(to_user.username), "success")
    return redirect(url_for('stream', username=to_user.username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    try:
        to_user = models.User.get(models.User.username ** username)
    except models.DoesNotExist:
        abort(404)
    else:
        try:
            models.Relationship.get(
                from_user=g.user._get_current_object(),
                to_user=to_user
            ).delete_instance()
        except models.IntegrityError:
            pass
        else:
            flash("You've unfollowed {}!".format(to_user.username), "success")
    return redirect(url_for('stream', username=to_user.username))


@app.route('/user/<username>')
@login_required
def user(username):
    if username and username != current_user.username:
        try:
            template = 'user_stream.html'
            Delete = DELETE_N
            user = models.User.select().where(
                models.User.username ** username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            stream = user.posts.limit(100)
    if username and username == current_user.username:
        user = models.User.select().where(
            models.User.username ** username).get()
        Delete = DELETE_Y
        template = 'user_stream.html'
        stream = user.posts.limit(100)
    return render_template(template, stream=stream, user=user, delete=Delete)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='',
            email='',
            password='',
            admin=True
        ),
    except ValueError:
        pass
    db.create_all()
    app.secret_key = 'super secret key'
    app.run(debug=DEBUG, host=HOST, port=PORT)