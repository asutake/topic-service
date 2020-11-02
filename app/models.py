from datetime import datetime
from sqlalchemy.orm import backref

from app.application import db


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    def __init__(self, title):
        self.title = title


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    text = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    topic = db.relationship("Topic",
                            backref=backref("_comments", lazy='dynamic'))

    def __init__(self, topic_id, text):
        self.topic_id = topic_id
        self.text = text


class CommentPopularity(db.Model):
    comment_id = db.Column(db.Integer,
                           db.ForeignKey('comment.id'),
                           primary_key=True)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)

    comment = db.relationship("Comment",
                              backref=backref("_popularity",
                                              uselist=False,
                                              cascade="all, delete-orphan"))

    def __init__(self, comment_id, likes=0, dislikes=0):
        self.comment_id = comment_id
        self.likes = likes
        self.dislikes = dislikes


class CommentReply(db.Model):
    comment_id = db.Column(db.Integer,
                           db.ForeignKey('comment.id'),
                           primary_key=True)
    reply_to_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    comment = db.relationship("Comment",
                              backref=backref("_reply",
                                              uselist=False,
                                              cascade="all, delete-orphan"),
                              foreign_keys=[comment_id])
    reply_to_comment = db.relationship("Comment",
                                       backref="_replies",
                                       foreign_keys=[reply_to_comment_id])

    def __init__(self, comment_id, reply_to_comment_id):
        self.comment_id = comment_id
        self.reply_to_comment_id = reply_to_comment_id
