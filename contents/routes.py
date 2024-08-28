from flask import make_response, request, abort, jsonify
from flask_restful import Resource

from .models import db, Post, Comment, Contact
from .serializer import posts_serializer, post_serializer


class PostListView(Resource):
    def get(self):
        posts = Post.query.filter_by(publish=True).order_by(Post.created_at.desc())
        return posts_serializer.dump(posts), 201


class PostDetailView(Resource):
    def get(self, slug):
        post = Post.query.get_or_404(slug)
        if post.publish:
            post.views += 1
            db.session.commit()
            return post_serializer.dump(post), 201
        else:
            abort(404)

    def post(self, slug):
        post = Post.query.get_or_404(slug)
        if post:
            data = request.get_json()
            new_comment = Comment(
                post_slug=post.slug,
                name=data["name"],
                message=data["message"]
            )
            db.session.add(new_comment)
            db.session.commit()
            return jsonify({"message": "Merci pour votre commentaire."})
        else:
            abort(404)


class ContactView(Resource):
    def post(self):
        data = request.get_json()
        new_contact = Contact(
            name=data["name"],
            email=data["email"],
            message=data["message"]
        )
        db.session.add(new_contact)
        db.session.commit()
        return make_response({"message": "Message envoyé avec succès."})