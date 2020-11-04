from http import HTTPStatus

from flask import jsonify, request
from marshmallow import Schema
from sqlalchemy import desc

from app.application import app, ma, db
from app.models import Topic


class TopicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Topic
        load_instance = True
        include_relationships = True

    id = ma.auto_field()
    title = ma.auto_field()
    created_at = ma.auto_field()
    deleted_at = ma.auto_field()


@app.route('/')
def hello():
    return "Hello World!"


@app.route("/topics", methods=["GET"])
def list_topic():
    q = Topic.query
    sort = request.args.get('sort', '')
    if sort == '-id':
        q = q.order_by(desc(Topic.id))

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
