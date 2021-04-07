from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from dashboard.auth import login_required
from dashboard.db import get_db

bp = Blueprint('takeout', __name__, url_prefix='/takeout')

@bp.route('/')
def index():
    db = get_db()
    takeouts = db.execute(
        'SELECT t.id, rest_name, rest_address, order_date, created, author_id, username'
        ' FROM takeout t JOIN user u ON t.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('takeout/takeoutIndex.html', takeouts=takeouts)

# create
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    print (request.method)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        takeoutOrderDate = request.form['takeoutOrderDate']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO takeout (rest_name, rest_address, order_date, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, takeoutOrderDate, g.user['id'])
            )
            db.commit()
            return redirect(url_for('takeout.index'))

    return render_template('takeout/takeoutCreate.html')
    
# update
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT t.id, rest_name, rest_address, order_date, created, author_id, username'
        ' FROM takeout t JOIN user u ON t.author_id = u.id'
        ' WHERE t.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        takeoutOrderDate = request.form['takeoutOrderDate']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE takeout SET rest_name = ?, rest_address = ?, order_date = ?'
                ' WHERE id = ?',
                (title, body, takeoutOrderDate, id)
            )
            db.commit()
            return redirect(url_for('takeout.index'))

    return render_template('takeout/takeoutUpdate.html', takeout=post)

# delete
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM takeout WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('takeout.index'))