from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from dashboard.auth import login_required
from dashboard.db import get_db

bp = Blueprint('medicine', __name__, url_prefix='/medicine')

@bp.route('/')
def index():
    db = get_db()
    medicines = db.execute(
        'SELECT m.id, med_name, direction, created, author_id, username'
        ' FROM medicine m JOIN user u ON m.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('medicine/medIndex.html', medicines=medicines)

# create
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    print (request.method)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO medicine (med_name, direction, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('medicine.index'))

    return render_template('medicine/medCreate.html')
    
# update
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT m.id, med_name, direction, created, author_id, username'
        ' FROM medicine m JOIN user u ON m.author_id = u.id'
        ' WHERE m.id = ?',
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
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE medicine SET med_name = ?, direction = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('medicine.index'))

    return render_template('medicine/medUpdate.html', medicine=post)

# delete
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM medicine WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('medicine.index'))