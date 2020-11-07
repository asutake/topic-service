from datetime import datetime
from sqlalchemy.orm import backref
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP

from app.application import db


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    created_at = db.Column(TIMESTAMP,
                           nullable=False,
                           server_default=func.now())
    deleted_at = db.Column(TIMESTAMP)

    def __init__(self, title):
        self.title = title

    def delete(self):
        self.deleted_at = datetime(2012, 3, 3, 10, 10, 10)
        db.session.add(self)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    text = db.Column(db.String(200), nullable=False)
    created_at = db.Column(TIMESTAMP,
                           nullable=False,
                           server_default=func.now())
    deleted_at = db.Column(TIMESTAMP)

    topic = db.relationship("Topic",
                            backref=backref("_comments", lazy='dynamic'))

    def __init__(self, topic_id, text):
        self.topic_id = topic_id
        self.text = text

    @property
    def popularity(self):
        if not self._popularity:
            self._popularity = CommentPopularity(self.id)
        return self._popularity

    def reply(self, comment):
        if self.topic_id != comment.topic_id:
            raise Exception('あとで')

        db.session.add(comment)
        db.session.flush()
        db.session.add(CommentReply(comment.id, self.id))


class CommentPopularity(db.Model):
    comment_id = db.Column(db.Integer,
                           db.ForeignKey('comment.id'),
                           primary_key=True)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)

    comment = db.relationship(
        "Comment",
        backref=backref(
            "_popularity",
            uselist=False,
            cascade="all, delete-orphan",
            lazy='joined',  # for N+1
        ))

    def __init__(self, comment_id, likes=0, dislikes=0):
        self.comment_id = comment_id
        self.likes = likes
        self.dislikes = dislikes

    def like(self):
        self.likes += 1
        db.session.add(self)

    def dislike(self):
        self.dislikes += 1
        db.session.add(self)


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
                                       backref=backref("_replies",
                                                       lazy='dynamic'),
                                       foreign_keys=[reply_to_comment_id])

    def __init__(self, comment_id, reply_to_comment_id):
        self.comment_id = comment_id
        self.reply_to_comment_id = reply_to_comment_id
