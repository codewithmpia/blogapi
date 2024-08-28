from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_cors import CORS

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    static_folder=BASE_DIR / "assets/static",
    template_folder=BASE_DIR / "assets/templates"
)

# Secret key
app.config["SECRET_KEY"] = "ht#0^i&uq2i9-i0hj)m(*7npzq8mxfd(!sr=g&0%1(krjx*f"

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASE_DIR}/db.sqlite3"
db = SQLAlchemy(app)

# Api
api = Api(app)

# Marshmallow
ma = Marshmallow(app)

# Cors
CORS(app)

# Admin 
from .models import Post, Comment, Contact
from .admin import PostAdminView, CommentAdminView, ContactAdminView

admin = Admin(app, name="Admin")

admin.add_views(
    PostAdminView(Post, db.session),
    CommentAdminView(Comment, db.session),
    ContactAdminView(Contact, db.session)
)

# Routes
from .routes import PostListView, PostDetailView, ContactView

api.add_resource(PostListView, "/api/posts")
api.add_resource(PostDetailView, "/api/posts/<string:slug>")
api.add_resource(ContactView, "/api/contact")