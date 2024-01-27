"""This file contains a helper table linking posts and users/authors"""

from database import db

postAuthors = db.Table(
    "postAuthors",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
)
