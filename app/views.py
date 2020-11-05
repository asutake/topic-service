from http import HTTPStatus

from flask import jsonify, request
from marshmallow import Schema, fields
from sqlalchemy import desc, func

from app.application import app, ma, db
from app.models import Topic, Comment, CommentPopularity, CommentReply


class TopicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Topic
        load_instance = True
        include_relationships = True

    id = ma.auto_field()
    title = ma.auto_field()
    created_at = ma.auto_field()
    deleted_at = ma.auto_field()


class CommentPopularitySchema(ma.SQLAlchemySchema):
    class Meta:
        model = CommentPopularity
        load_instance = True
        include_relationships = True

    comment_id = ma.auto_field()
    likes = ma.auto_field()
    dislikes = ma.auto_field()


class CommentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Comment
        load_instance = True
        include_relationships = True
        include_fk = True

    id = ma.auto_field()
    topic_id = ma.auto_field()
    text = ma.auto_field()
    created_at = ma.auto_field()
    deleted_at = ma.auto_field()

    popularity = fields.Nested(
        CommentPopularitySchema(only=(
            'likes',
            'dislikes',
        )),
        dump_only=True,
    )


@app.route('/')
def hello():
    return "Hello World!"


@app.route("/topics", methods=["GET"])
def list_topic():
    q = Topic.query

    sort = request.args.get('sort', '')
    if sort == '-id':
        q = q.order_by(desc(Topic.id))
    if sort == '-comments':
        q = q.outerjoin(Comment).group_by(Topic.id)
        q = q.order_by(desc(func.count(Topic.id)))

    return jsonify(
        TopicSchema(many=True).dump(
            q \
            .offset(request.args.get('offset', 0))
            .limit(request.args.get('limit', 20))
            .all())
    )


@app.route("/topics", methods=["POST"])
def add_topic():
    topic = TopicSchema().load(request.json)

    db.session.add(topic)
    db.session.commit()

    return jsonify(TopicSchema().dump(topic)), HTTPStatus.CREATED


@app.route("/topics/<id>", methods=["GET"])
def detail_topic(id):
    return jsonify(TopicSchema().dump(Topic.query.get_or_404(id)))


@app.route("/topics/<id>", methods=["PUT"])
def update_topic(id):
    data = TopicSchema().load(request.json)

    topic = Topic.query.get_or_404(id)
    topic.title = data.title

    db.session.add(topic)
    db.session.commit()

    return jsonify(TopicSchema().dump(topic))


@app.route("/topics/<id>", methods=["DELETE"])
def delete_topic(id):
    topic = Topic.query.get_or_404(id)

    db.session.delete(topic)
    db.session.commit()

    return jsonify({}), HTTPStatus.NO_CONTENT


@app.route("/comments", methods=["GET"])
def list_comment():
    q = Comment.query
    sort = request.args.get('sort', '')
    if sort == '-id':
        q = q.order_by(desc(Comment.id))

    reply_to_comment_id = request.args.get('reply_to_comment_id', None)
    if reply_to_comment_id:
        q = q.outerjoin(CommentReply,
                        Comment.id == CommentReply.comment_id).filter_by(
                            reply_to_comment_id=1)

    return jsonify(
        CommentSchema(many=True).dump(
            q \
            .offset(request.args.get('offset', 0))
            .limit(request.args.get('limit', 20))
            .all())
    )


@app.route("/comments", methods=["POST"])
def add_comment():
    comment = CommentSchema().load(request.json)

    db.session.add(comment)
    db.session.commit()

    return jsonify(CommentSchema().dump(comment)), HTTPStatus.CREATED


@app.route("/comments/<id>", methods=["GET"])
def detail_comment(id):
    return jsonify(CommentSchema().dump(Comment.query.get_or_404(id)))


@app.route("/comments/<id>", methods=["PUT"])
def update_comment(id):
    data = CommentSchema().load(request.json)

    comment = Comment.query.get_or_404(id)
    comment.topic_id = data.topic_id
    comment.text = data.text

    db.session.add(comment)
    db.session.commit()

    return jsonify(CommentSchema().dump(comment))


@app.route("/comments/<id>", methods=["DELETE"])
def delete_comment(id):
    comment = Comment.query.get_or_404(id)

    db.session.delete(comment)
    db.session.commit()

    return jsonify({}), HTTPStatus.NO_CONTENT
