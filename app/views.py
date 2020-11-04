from flask import jsonify
from marshmallow import Schema

from app.application import app, ma
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
