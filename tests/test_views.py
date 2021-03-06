import json


def test_root(client):
    res = client.get("/")

    assert 200 == res.status_code
    assert b"Hello World!" in res.data


def test_list_topic(client):
    res = client.get("/topics")

    assert 200 == res.status_code
    assert "3" == res.headers["Resource-Count"]
    assert [
        {
            "id": 1,
            "title": "タイトル1",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "comment_num": 3,
        },
        {
            "id": 2,
            "title": "タイトル2",
            "created_at": "2021-11-04T19:28:38",
            "deleted_at": None,
            "comment_num": 4,
        },
        {
            "id": 3,
            "title": "タイトル3",
            "created_at": "2022-11-04T19:28:38",
            "deleted_at": None,
            "comment_num": 1,
        },
    ] == json.loads(res.data)

    res = client.get("/topics?sort=-id")

    assert 200 == res.status_code
    assert [
        {
            "id": 3,
            "title": "タイトル3",
            "created_at": "2022-11-04T19:28:38",
            "deleted_at": None,
            "comment_num": 1,
        },
        {
            "id": 2,
            "title": "タイトル2",
            "created_at": "2021-11-04T19:28:38",
            "deleted_at": None,
            "comment_num": 4,
        },
        {
            "id": 1,
            "title": "タイトル1",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "comment_num": 3,
        },
    ] == json.loads(res.data)

    res = client.get("/topics?sort=-comments")

    assert 200 == res.status_code
    assert [
        {
            "id": 2,
            "title": "タイトル2",
            "created_at": "2021-11-04T19:28:38",
            "deleted_at": None,
            "comment_num": 4,
        },
        {
            "id": 1,
            "title": "タイトル1",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "comment_num": 3,
        },
        {
            "id": 3,
            "title": "タイトル3",
            "created_at": "2022-11-04T19:28:38",
            "deleted_at": None,
            "comment_num": 1,
        },
    ] == json.loads(res.data)

    res = client.get("/topics?offset=1")

    assert 200 == res.status_code
    assert [
        {
            "id": 2,
            "title": "タイトル2",
            "created_at": "2021-11-04T19:28:38",
            "deleted_at": None,
            "comment_num": 4,
        },
        {
            "id": 3,
            "title": "タイトル3",
            "created_at": "2022-11-04T19:28:38",
            "deleted_at": None,
            "comment_num": 1,
        },
    ] == json.loads(res.data)

    res = client.get("/topics?limit=1")

    assert 200 == res.status_code
    assert [
        {
            "id": 1,
            "title": "タイトル1",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "comment_num": 3,
        },
    ] == json.loads(res.data)

    res = client.get("/topics?offset=1&limit=1")

    assert 200 == res.status_code
    assert [
        {
            "id": 2,
            "title": "タイトル2",
            "created_at": "2021-11-04T19:28:38",
            "deleted_at": None,
            "comment_num": 4,
        },
    ] == json.loads(res.data)


def test_add_topic(client):
    res = client.post(
        "/topics",
        data=json.dumps(
            {
                "title": "タイトル5",
            }
        ),
        content_type="application/json",
    )

    assert 201 == res.status_code

    d = json.loads(res.data)
    assert 5 == d["id"]
    assert "タイトル5" == d["title"]
    assert d["created_at"] is not None
    assert d["deleted_at"] is None

    res = client.get("/topics/5")

    assert 200 == res.status_code

    d = json.loads(res.data)
    assert 5 == d["id"]
    assert "タイトル5" == d["title"]
    assert d["created_at"] is not None
    assert d["deleted_at"] is None


def test_detail_topic(client):
    res = client.get("/topics/1")

    assert 200 == res.status_code
    assert {
        "id": 1,
        "title": "タイトル1",
        "created_at": "2020-11-04T19:28:38",
        "deleted_at": None,
    } == json.loads(res.data)


def test_update_topic(client):
    res = client.put(
        "/topics/1",
        data=json.dumps({"title": "タイトルA"}),
        content_type="application/json",
    )
    assert 200 == res.status_code
    assert {
        "id": 1,
        "title": "タイトルA",
        "created_at": "2020-11-04T19:28:38",
        "deleted_at": None,
    } == json.loads(res.data)

    res = client.get("/topics/1")

    assert 200 == res.status_code
    assert {
        "id": 1,
        "title": "タイトルA",
        "created_at": "2020-11-04T19:28:38",
        "deleted_at": None,
    } == json.loads(res.data)


def test_delete_topic(client):
    res = client.delete("/topics/1")

    assert 204 == res.status_code
    assert b"" == res.data

    res = client.get("/topics/1")

    assert 404 == res.status_code
    assert b"404" in res.data


def test_list_comment(client):
    res = client.get("/comments")

    assert 200 == res.status_code
    assert "7" == res.headers["Resource-Count"]
    assert [
        {
            "id": 1,
            "topic_id": 1,
            "text": "コメント1-1",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 100,
                "dislikes": 1,
            },
        },
        {
            "id": 2,
            "topic_id": 1,
            "text": "コメント1-2",
            "created_at": "2021-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
        {
            "id": 3,
            "topic_id": 1,
            "text": "コメント1-3",
            "created_at": "2022-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
        {
            "id": 4,
            "topic_id": 2,
            "text": "コメント2-1",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 1,
                "dislikes": 1,
            },
        },
        {
            "id": 5,
            "topic_id": 2,
            "text": "コメント2-2",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
        {
            "id": 6,
            "topic_id": 2,
            "text": "コメント2-3",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
        {
            "id": 7,
            "topic_id": 2,
            "text": "コメント2-4",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
    ] == json.loads(res.data)

    res = client.get("/comments?reply_to_comment_id=1")
    assert 200 == res.status_code
    assert [
        {
            "id": 2,
            "topic_id": 1,
            "text": "コメント1-2",
            "created_at": "2021-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
        {
            "id": 3,
            "topic_id": 1,
            "text": "コメント1-3",
            "created_at": "2022-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
    ] == json.loads(res.data)

    res = client.get("/comments?reply_to_comment_id=2")
    assert 200 == res.status_code
    assert [] == json.loads(res.data)

    res = client.get("/comments?sort=-id")

    assert 200 == res.status_code
    assert [
        {
            "id": 7,
            "topic_id": 2,
            "text": "コメント2-4",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
        {
            "id": 6,
            "topic_id": 2,
            "text": "コメント2-3",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
        {
            "id": 5,
            "topic_id": 2,
            "text": "コメント2-2",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
        {
            "id": 4,
            "topic_id": 2,
            "text": "コメント2-1",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 1,
                "dislikes": 1,
            },
        },
        {
            "id": 3,
            "topic_id": 1,
            "text": "コメント1-3",
            "created_at": "2022-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
        {
            "id": 2,
            "topic_id": 1,
            "text": "コメント1-2",
            "created_at": "2021-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
        {
            "id": 1,
            "topic_id": 1,
            "text": "コメント1-1",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 100,
                "dislikes": 1,
            },
        },
    ] == json.loads(res.data)

    res = client.get("/comments?offset=1")

    assert 200 == res.status_code
    assert [
        {
            "id": 2,
            "topic_id": 1,
            "text": "コメント1-2",
            "created_at": "2021-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
        {
            "id": 3,
            "topic_id": 1,
            "text": "コメント1-3",
            "created_at": "2022-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
        {
            "id": 4,
            "topic_id": 2,
            "text": "コメント2-1",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 1,
                "dislikes": 1,
            },
        },
        {
            "id": 5,
            "topic_id": 2,
            "text": "コメント2-2",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
        {
            "id": 6,
            "topic_id": 2,
            "text": "コメント2-3",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
        {
            "id": 7,
            "topic_id": 2,
            "text": "コメント2-4",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
    ] == json.loads(res.data)

    res = client.get("/comments?limit=1")

    assert 200 == res.status_code
    assert [
        {
            "id": 1,
            "topic_id": 1,
            "text": "コメント1-1",
            "created_at": "2020-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 100,
                "dislikes": 1,
            },
        },
    ] == json.loads(res.data)

    res = client.get("/comments?offset=1&limit=1")

    assert 200 == res.status_code
    assert [
        {
            "id": 2,
            "topic_id": 1,
            "text": "コメント1-2",
            "created_at": "2021-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
    ] == json.loads(res.data)


def test_add_comment(client):
    res = client.post(
        "/comments",
        data=json.dumps(
            {
                "topic_id": 1,
                "text": "コメント1-4",
            }
        ),
        content_type="application/json",
    )

    assert 201 == res.status_code

    d = json.loads(res.data)
    assert 9 == d["id"]
    assert 1 == d["topic_id"]
    assert "コメント1-4" == d["text"]
    assert d["created_at"] is not None
    assert d["deleted_at"] is None

    res = client.get("/comments/9")
    d = json.loads(res.data)

    assert 9 == d["id"]
    assert 1 == d["topic_id"]
    assert "コメント1-4" == d["text"]
    assert d["created_at"] is not None
    assert d["deleted_at"] is None


def test_detail_comment(client):
    res = client.get("/comments/1")

    assert 200 == res.status_code
    assert {
        "id": 1,
        "topic_id": 1,
        "text": "コメント1-1",
        "created_at": "2020-11-04T19:28:38",
        "deleted_at": None,
        "popularity": {
            "likes": 100,
            "dislikes": 1,
        },
    } == json.loads(res.data)


def test_update_comment(client):
    res = client.put(
        "/comments/1",
        data=json.dumps(
            {
                "id": 1,
                "topic_id": 3,
                "text": "コメント3-1",
                "created_at": "2020-11-04T19:28:38",
                "deleted_at": None,
                # "popularity": {
                #    "likes": 100,
                #    "dislikes": 1,
                # },
            }
        ),
        content_type="application/json",
    )
    assert 200 == res.status_code
    assert {
        "id": 1,
        "topic_id": 3,
        "text": "コメント3-1",
        "created_at": "2020-11-04T19:28:38",
        "deleted_at": None,
        "popularity": {
            "likes": 100,
            "dislikes": 1,
        },
    } == json.loads(res.data)

    res = client.get("/comments/1")

    assert 200 == res.status_code
    assert {
        "id": 1,
        "topic_id": 3,
        "text": "コメント3-1",
        "created_at": "2020-11-04T19:28:38",
        "deleted_at": None,
        "popularity": {
            "likes": 100,
            "dislikes": 1,
        },
    } == json.loads(res.data)


def test_delete_comment(client):
    res = client.delete("/comments/1")

    assert 204 == res.status_code
    assert b"" == res.data

    res = client.get("/comments/1")

    assert 404 == res.status_code
    assert b"404" in res.data


def test_like_comment(client):
    res = client.post(
        "/comments/1/like",
        data=json.dumps({}),
        content_type="application/json",
    )

    assert 200 == res.status_code
    assert {
        "id": 1,
        "topic_id": 1,
        "text": "コメント1-1",
        "created_at": "2020-11-04T19:28:38",
        "deleted_at": None,
        "popularity": {
            "likes": 101,
            "dislikes": 1,
        },
    } == json.loads(res.data)


def test_dislike_comment(client):
    res = client.post(
        "/comments/1/dislike",
        data=json.dumps({}),
        content_type="application/json",
    )

    assert 200 == res.status_code
    assert {
        "id": 1,
        "topic_id": 1,
        "text": "コメント1-1",
        "created_at": "2020-11-04T19:28:38",
        "deleted_at": None,
        "popularity": {
            "likes": 100,
            "dislikes": 2,
        },
    } == json.loads(res.data)


def test_reply_comment(client):
    # 返信の時はtopic_id いらないよね
    res = client.post(
        "/comments/1/reply",
        data=json.dumps(
            {
                # "topic_id": 1,
                "text": "コメント1-4",
            }
        ),
        content_type="application/json",
    )

    assert 201 == res.status_code

    d = json.loads(res.data)
    assert 9 == d["id"]
    assert 1 == d["topic_id"]
    assert "コメント1-4" == d["text"]
    assert d["created_at"] is not None
    assert d["deleted_at"] is None

    res = client.get("/comments?reply_to_comment_id=1")

    assert 200 == res.status_code
    assert [
        {
            "id": 2,
            "topic_id": 1,
            "text": "コメント1-2",
            "created_at": "2021-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
        {
            "id": 3,
            "topic_id": 1,
            "text": "コメント1-3",
            "created_at": "2022-11-04T19:28:38",
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
        {
            "id": 9,
            "topic_id": 1,
            "text": "コメント1-4",
            "created_at": d["created_at"],
            "deleted_at": None,
            "popularity": {
                "likes": 0,
                "dislikes": 0,
            },
        },
    ] == json.loads(res.data)
