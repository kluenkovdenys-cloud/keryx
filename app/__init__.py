from flask import Flask, render_template,redirect,url_for,request
from .form import LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import logout_user, login_required, login_user, UserMixin, LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = '1234'
db=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    finding = db.Column(db.String(26), nullable=False)

class User(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    password = db.Column(db.String(80),nullable=False)
with app.app_context():
    db.create_all()
@app.route("/", methods=["GET","POST"])
def index():
    form=LoginForm()
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return "Заполните поля регистрации"
        user_name=User.query.filter_by(username=username).first()
        if user_name:
            return "Это имя уже занято"
        print(f"username:{username}")
        print(f"password:{password}")
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("index.html",form=form)

@app.route("/login" , methods=["GET","POST"])

def login():
    form = LoginForm()
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password ==password:
            login_user(user)
            return redirect(url_for('keryx'))
        else:
            return redirect(url_for('login'))
    return render_template("login.html",form=form)

@app.route("/keryx")
def keryx():
    return render_template("keryx.html")

@app.route("/search")
def search_user():
    username = request.args.get('username', "").strip()
    username = username.replace("@", "")
    user = User.query.filter(User.username.ilike(username)).first()
    if user:
        return redirect (url_for('profile', user_id=user.id))
    return "Пользователь не найден."
@app.route("/profile/<int:user_id>")
def profile(user_id):
    user=User.query.get_or_404(user_id)
    return render_template("keryx.html",user=user)