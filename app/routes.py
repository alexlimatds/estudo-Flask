from app import app
from flask import render_template, flash, redirect, url_for, request
from app import model, forms
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/aluno", methods=['GET', 'POST'])
def aluno():
    form = forms.AlunoForm()
    if form.validate_on_submit(): # validação só ocorre para POST
        aluno = model.Aluno(None, None, None)
        form.populate_obj(aluno)
        model.insert_aluno(aluno)
        flash(f'Aluno cadastrado com sucesso!')
        return redirect(url_for('aluno'))
    return render_template("aluno.html", form=form)

@app.route("/aluno2", methods=['GET', 'POST'])
def aluno2():
    form = forms.AlunoForm()
    if form.validate_on_submit(): # validação só ocorre para POST
        aluno = model.Aluno(None, None, None)
        form.populate_obj(aluno)
        model.insert_aluno(aluno)
        flash(f'Aluno cadastrado com sucesso!')
        return redirect(url_for('alunos'))
    return render_template("aluno2.html", form=form)

@app.route("/alunos")
def alunos():
    lista = model.get_alunos()
    return render_template("alunos.html", alunos=lista)

@app.route("/submit_aluno", methods=['POST'])
def submit_aluno():
    lista = model.get_alunos()
    return render_template("alunos.html", alunos=lista)

# BLOG ROUTES
@app.route('/blog/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('all_posts'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = model.get_user(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Credenciais inválidas')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('all_posts')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/blog/logout')
def logout():
    logout_user()
    return redirect(url_for('all_posts'))

@app.route("/blog/all_posts")
@app.route("/blog")
def all_posts():
    lista = model.all_posts()
    return render_template("all_posts.html", posts=lista)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('all_posts'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = model.User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        model.registrar_usuario(user)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/blog/post', methods=['GET', 'POST'])
@app.route('/blog/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id=None):
    form = forms.PostForm()
    if form.validate_on_submit(): # POST
        # Edição
        if post_id is not None:
            post = model.Post.query.get(post_id)
            if current_user.id != post.user_id:
                raise ValueError('Usuário corrente não é o autor da postagem')
            post.body = form.body.data
        # Novo post
        else:
            post = model.Post(
                body=form.body.data, 
                user_id=current_user.id
            )
        model.save_post(post)
        flash('You have posted!')
        return redirect(url_for('all_posts'))
    # GET
    if post_id is not None:
        post = model.Post.query.get(post_id)
        if current_user.id != post.user_id:
            raise ValueError('Usuário corrente não é o autor da postagem')
        form.id.data = post.id
        form.body.data = post.body
    return render_template('post.html', form=form)

@app.route("/error_test")
def error_test():
    raise Exception('Exception test')