from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from dashboard.auth import login_required
from dashboard.db import get_db

bp = Blueprint('doctor', __name__, url_prefix='/doctor')

@bp.route('/')
def index():
    db = get_db()
    doctors = db.execute(
        'SELECT d.id, doc_type, doc_address, doc_date, created, author_id, username'
        ' FROM doctor d JOIN user u ON d.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('doctor/doctorIndex.html', doctors=doctors)

# create
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    print (request.method)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        dDate = request.form['dDate']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO doctor (doc_type, doc_address, doc_date, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, dDate, g.user['id'])
            )
            db.commit()
            return redirect(url_for('doctor.index'))

    return render_template('doctor/doctorCreate.html')
    
# update
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT d.id, doc_type, doc_address, doc_date, created, author_id, username'
        ' FROM doctor d JOIN user u ON d.author_id = u.id'
        ' WHERE d.id = ?',
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
        dDate = request.form['dDate']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE doctor SET doc_type = ?, doc_address = ?, doc_date = ?'
                ' WHERE id = ?',
                (title, body, dDate, id)
            )
            db.commit()
            return redirect(url_for('doctor.index'))

    return render_template('doctor/doctorUpdate.html', doctor=post)

# delete
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM doctor WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('doctor.index'))