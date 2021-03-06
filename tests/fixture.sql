INSERT INTO
    topic (id, title, created_at, deleted_at)
VALUES
    (1, 'タイトル1', '2020-11-04 19:28:38', null),
    (2, 'タイトル2', '2021-11-04 19:28:38', null),
    (3, 'タイトル3', '2022-11-04 19:28:38', null),
    (
        4,
        'タイトル4',
        '2022-11-04 19:28:38',
        '2022-11-04 19:28:38'
    );

INSERT INTO
    comment (id, topic_id, text, created_at, deleted_at)
VALUES
    (1, 1, 'コメント1-1', '2020-11-04 19:28:38', null),
    (2, 1, 'コメント1-2', '2021-11-04 19:28:38', null),
    (3, 1, 'コメント1-3', '2022-11-04 19:28:38', null),
    (4, 2, 'コメント2-1', '2020-11-04 19:28:38', null),
    (5, 2, 'コメント2-2', '2020-11-04 19:28:38', null),
    (6, 2, 'コメント2-3', '2020-11-04 19:28:38', null),
    (7, 2, 'コメント2-4', '2020-11-04 19:28:38', null),
    (
        8,
        1,
        'コメント1-4',
        '2020-11-04 19:28:38',
        '2020-11-04 19:28:38'
    );

INSERT INTO
    comment_popularity (comment_id, likes, dislikes)
VALUES
    (1, 100, 1),
    (2, 0, 0),
    (4, 1, 1);

INSERT INTO
    comment_reply (comment_id, reply_to_comment_id)
VALUES
    (2, 1),
    (3, 1);
