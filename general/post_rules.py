def validate_post(title, body):
    title = title.strip()
    body = body.strip()

    if not title:
        return title, body, "제목을 입력해 주세요."

    if not body:
        return title, body, "내용을 입력해 주세요."

    return title, body, None
