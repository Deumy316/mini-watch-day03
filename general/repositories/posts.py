from db import connect_db


def find_all_posts():
    with connect_db() as conn:
        return conn.execute("""
            SELECT id, title, body
            FROM posts
            ORDER BY id ASC
            """).fetchall()


def find_post(post_id):
    with connect_db() as conn:
        return conn.execute(
            """
            SELECT id, title, body
            FROM posts
            WHERE id = %s
            """,
            (post_id,),
        ).fetchone()


def create_post(title, body):
    with connect_db() as conn:
        post = conn.execute(
            """
            INSERT INTO posts (title, body)
            VALUES (%s, %s)
            RETURNING id, title, body
            """,
            (title, body),
        ).fetchone()

        conn.commit()
        return post


def update_post(post_id, title, body):
    with connect_db() as conn:
        post = conn.execute(
            """
            UPDATE posts
            SET title = %s,
                body = %s
            WHERE id = %s
            RETURNING id, title, body
            """,
            (title, body, post_id),
        ).fetchone()

        conn.commit()
        return post


def delete_post(post_id):
    with connect_db() as conn:
        post = conn.execute(
            """
            DELETE FROM posts
            WHERE id = %s
            RETURNING id, title, body
            """,
            (post_id,),
        ).fetchone()

        conn.commit()
        return post
