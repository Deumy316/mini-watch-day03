CREATE SEQUENCE IF NOT EXISTS posts_id_seq;

CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY DEFAULT nextval('posts_id_seq'),
    title TEXT NOT NULL,
    body TEXT NOT NULL
);

ALTER SEQUENCE posts_id_seq OWNED BY posts.id;

SELECT setval(
    'posts_id_seq',
    COALESCE((SELECT MAX(id) FROM posts), 0) + 1,
    false
);

SELECT * FROM posts;