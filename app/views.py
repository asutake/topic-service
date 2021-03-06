from http import HTTPStatus

from flask import jsonify, request, make_response
from marshmallow import fields
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
    comment_num = fields.Int()


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
        CommentPopularitySchema(
            only=(
                "likes",
                "dislikes",
            )
        ),
        dump_only=True,
    )


class TopicCreateSchema(ma.SQLAlchemySchema):
    title = fields.String()
    text = fields.String()


class CommentReplySchema(ma.SQLAlchemySchema):
    text = fields.String()


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/topics", methods=["GET"])
def list_topic():
    q = (
        db.session.query(
            Topic.id,
            Topic.title,
            Topic.created_at,
            Topic.deleted_at,
            func.count(Topic.id),
        )
        .filter_by(deleted_at=None)
        .outerjoin(Comment)
        .group_by(Topic.id)
        .filter_by(deleted_at=None)
    )

    sort = request.args.get("sort", "")
    if sort == "-id":
        q = q.order_by(desc(Topic.id))
    if sort == "-comments":
        q = q.order_by(desc(func.count(Topic.id)))

    rows = (
        q.offset(request.args.get("offset", 0))
        .limit(request.args.get("limit", 20))
        .all()
    )

    res = make_response(
        jsonify(
            TopicSchema(many=True).dump(
                map(
                    lambda x: dict(
                        zip(
                            [
                                "id",
                                "title",
                                "created_at",
                                "deleted_at",
                                "comment_num",
                            ],
                            x,
                        )
                    ),
                    rows,
                )
            )
        )
    )

    # for dashboard
    res.headers["Resource-Count"] = q.count()

    return res


@app.route("/topics", methods=["POST"])
def add_topic():
    topic = TopicSchema().load(request.json)

    db.session.add(topic)
    db.session.commit()

    return jsonify(TopicSchema().dump(topic)), HTTPStatus.CREATED


@app.route("/topics/create", methods=["POST"])
def create_topic():
    data = TopicCreateSchema().load(request.json)

    topic = Topic.create(
        data["title"],
        data["text"],
    )

    db.session.commit()

    return jsonify(TopicSchema().dump(topic)), HTTPStatus.CREATED


@app.route("/topics/<id>", methods=["GET"])
def detail_topic(id):
    return jsonify(
        TopicSchema().dump(
            Topic.query.filter_by(id=id, deleted_at=None).first_or_404()
        )
    )


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

    topic.delete()
    db.session.commit()

    return jsonify({}), HTTPStatus.NO_CONTENT


@app.route("/comments", methods=["GET"])
def list_comment():
    q = Comment.query.filter_by(deleted_at=None)
    topic_id = request.args.get("topic_id", "")
    if topic_id:
        q = q.filter_by(topic_id=topic_id)

    sort = request.args.get("sort", "")
    if sort == "-id":
        q = q.order_by(desc(Comment.id))

    reply_to_comment_id = request.args.get("reply_to_comment_id", None)
    if reply_to_comment_id:
        q = q.outerjoin(
            CommentReply, Comment.id == CommentReply.comment_id
        ).filter_by(reply_to_comment_id=reply_to_comment_id)

    res = make_response(
        jsonify(
            CommentSchema(many=True).dump(
                q.offset(request.args.get("offset", 0))
                .limit(request.args.get("limit", 20))
                .all()
            )
        )
    )

    # for dashboard
    res.headers["Resource-Count"] = q.count()

    return res


@app.route("/comments", methods=["POST"])
def add_comment():
    comment = CommentSchema().load(request.json)

    db.session.add(comment)
    db.session.commit()

    return jsonify(CommentSchema().dump(comment)), HTTPStatus.CREATED


@app.route("/comments/<id>", methods=["GET"])
def detail_comment(id):
    return jsonify(
        CommentSchema().dump(
            Comment.query.filter_by(id=id, deleted_at=None).first_or_404()
        )
    )


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

    comment.delete()
    db.session.commit()

    return jsonify({}), HTTPStatus.NO_CONTENT


@app.route("/comments/<id>/like", methods=["POST"])
def like_comment(id):
    comment = Comment.query.get_or_404(id)

    comment.popularity.like()
    db.session.commit()

    return jsonify(CommentSchema().dump(comment))


@app.route("/comments/<id>/dislike", methods=["POST"])
def dislike_comment(id):
    comment = Comment.query.get_or_404(id)

    comment.popularity.dislike()
    db.session.commit()

    return jsonify(CommentSchema().dump(comment))


@app.route("/comments/<id>/reply", methods=["POST"])
def reply_comment(id):
    data = CommentReplySchema().load(request.json)

    reply_to_comment = Comment.query.get_or_404(id)
    comment = Comment(reply_to_comment.topic_id, data["text"])
    reply_to_comment.reply(comment)

    db.session.commit()

    return jsonify(CommentSchema().dump(comment)), HTTPStatus.CREATED


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
    )
    response.headers.add("Content-Type", "application/json")
    response.headers.add("Access-Control-Expose-Headers", "Resource-Count")

    return response
