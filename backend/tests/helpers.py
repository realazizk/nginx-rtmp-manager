from flask import url_for


def login(ctx, user):
    resp = ctx.post_json(url_for('users.login'), {
        'username': user.username,
        'password': 'myprecious'
    })
    return resp.json['id_token']
