class Aluno:
    def __init__(self, nome, matricula, curso) -> None:
        self.nome = nome
        self.matricula = matricula
        self.curso = curso
    
alunos = [
    Aluno("André Silva", "2233", "Mecânica"), 
    Aluno("Maria Rita", "1100", "Informática"), 
    Aluno("Joseneide Pereira", "1010", "Geologia"), 
    Aluno("José Abreu", "3311", "Geologia")
]

def get_alunos():
    return alunos

def insert_aluno(aluno):
    alunos.append(aluno)

# BLOG MODEL
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now()
    )
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(User.id), index=True
    )
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return f'<Post {self.body}>'
    
def all_posts():
    query = sa.select(Post).order_by(Post.timestamp.desc())
    return db.session.scalars(query).all()

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

def get_user(username):
    return db.session.scalar(
        sa.select(User).where(User.username == username)
    )

def registrar_usuario(user):
    db.session.add(user)
    db.session.commit()

def save_post(post):
    if post.id is None:
        db.session.add(post)
    db.session.commit()