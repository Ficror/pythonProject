import flask_login
from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.catalog import Catalog
from data.completed_orders import Completed_orders
from flask_sqlalchemy.forms.login import LoginForm
from forms.user import RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/web.db")
    app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if flask_login.current_user.is_authenticated:
        if flask_login.current_user.email == "admin@gmail.com":
            orders = db_sess.query(Completed_orders).all()
            user_id = db_sess.query(User).all()
            if orders == []:
                return render_template("empty_orders.html", flag=True)
            return render_template("admin_page.html", compl_orders=orders, adress=user_id, flag=True)
        return render_template("base.html", title="Start page")
    return render_template("base.html", title="Start page")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            address=form.address.data,
            surname=form.surname.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/<product_name>', methods=['GET', 'POST'])
def products(product_name):
    db_sess = db_session.create_session()
    names = db_sess.query(Catalog).filter(Catalog.type == product_name)
    return render_template("product_page.html", names=names)


@app.route('/in_basket/<product>')
def in_basket(product):
    db_sess = db_session.create_session()
    name = db_sess.query(Catalog).filter(Catalog.id == int(product)).first()
    name.in_basket = 1
    db_sess.commit()
    return redirect("/" + name.type)


@app.route('/basket')
def basket():
    db_sess = db_session.create_session()
    summ = 0
    names = db_sess.query(Catalog).filter(Catalog.in_basket == 1).all()
    for i in names:
        summ += int(i.price)
    if names == []:
        return render_template("empty_basket.html")
    else:
        return render_template("basket.html", names=names, summ=summ)


@app.route('/not_in_basket/<product>')
def not_in_basket(product):
    db_sess = db_session.create_session()
    name = db_sess.query(Catalog).filter(Catalog.id == int(product)).first()
    name.in_basket = 0
    db_sess.commit()
    return redirect("/basket")


@app.route('/order', methods=['GET', 'POST'])
def order():
    return render_template("basket_end.html", message="Вы не зарегистрированны")


@app.route('/order_good', methods=['GET', 'POST'])
def order_good():
    db_sess = db_session.create_session()
    names_name = []
    names = db_sess.query(Catalog).filter(Catalog.in_basket == 1).all()
    for i in names:
        names_name.append(i.name)
    names_name = ", ".join(names_name)
    for i in names:
        i.in_basket = 0
    db_sess.commit()
    user_id = flask_login.current_user.id
    compl_ord = Completed_orders(
        username=user_id,
        list_of_product=names_name
    )
    db_sess.add(compl_ord)
    db_sess.commit()
    return render_template("basket_end.html", message1="Заказ успешно оформлен",
                           message2="С вами свяжутся для уточнения деталей заказа", flag=False)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    compl_ord = db_sess.query(Completed_orders).filter(Completed_orders.id == id).first()
    if compl_ord:
        db_sess.delete(compl_ord)
        db_sess.commit()
    return redirect('/')


if __name__ == '__main__':
    main()
