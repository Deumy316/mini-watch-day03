from flask import Blueprint, render_template, request, redirect, url_for

from post_rules import validate_post
from repositories.posts import (
    find_all_posts,
    find_post,
    create_post,
    update_post,
    delete_post,
)

posts_bp = Blueprint("posts", __name__)


@posts_bp.get("/")
def index():
    posts = find_all_posts()

    return render_template(
        "index.html",
        posts=posts,
    )


@posts_bp.get("/board/<int:post_id>")
def detail(post_id):
    post = find_post(post_id)

    if post is None:
        return (
            render_template(
                "error.html",
                message="게시글을 찾을 수 없습니다.",
            ),
            404,
        )

    return render_template(
        "detail.html",
        post=post,
    )


@posts_bp.route("/board/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template(
            "new.html",
            title="",
            body="",
            error=None,
        )

    title = request.form.get("title", "")
    body = request.form.get("body", "")

    title, body, error = validate_post(title, body)

    if error is not None:
        return (
            render_template(
                "new.html",
                title=title,
                body=body,
                error=error,
            ),
            400,
        )

    post = create_post(title, body)

    return redirect(
        url_for("posts.detail", post_id=post["id"]),
        code=303,
    )


@posts_bp.route("/board/<int:post_id>/edit", methods=["GET", "POST"])
def edit(post_id):
    post = find_post(post_id)

    if post is None:
        return (
            render_template(
                "error.html",
                message="게시글을 찾을 수 없습니다.",
            ),
            404,
        )

    if request.method == "GET":
        return render_template(
            "edit.html",
            post=post,
            title=post["title"],
            body=post["body"],
            error=None,
        )

    title = request.form.get("title", "")
    body = request.form.get("body", "")

    title, body, error = validate_post(title, body)

    if error is not None:
        return (
            render_template(
                "edit.html",
                post=post,
                title=title,
                body=body,
                error=error,
            ),
            400,
        )

    updated_post = update_post(post_id, title, body)

    if updated_post is None:
        return (
            render_template(
                "error.html",
                message="게시글을 찾을 수 없습니다.",
            ),
            404,
        )

    return redirect(
        url_for("posts.detail", post_id=post_id),
        code=303,
    )


@posts_bp.route("/board/<int:post_id>/delete", methods=["GET", "POST"])
def delete(post_id):
    post = find_post(post_id)

    if post is None:
        return (
            render_template(
                "error.html",
                message="게시글을 찾을 수 없습니다.",
            ),
            404,
        )

    if request.method == "GET":
        return render_template(
            "delete.html",
            post=post,
        )

    deleted_post = delete_post(post_id)

    if deleted_post is None:
        return (
            render_template(
                "error.html",
                message="게시글을 찾을 수 없습니다.",
            ),
            404,
        )

    return redirect(
        url_for("posts.index"),
        code=303,
    )
