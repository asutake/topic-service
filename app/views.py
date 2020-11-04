from http import HTTPStatus

from flask import jsonify, request
from marshmallow import Schema

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
    return jsonify(TopicSchema(many=True).dump(Topic.query.all()))


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
