from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from dashboard.auth import login_required
from dashboard.db import get_db

bp = Blueprint('symptom', __name__, url_prefix='/symptom')

@bp.route('/')
def index():
    db = get_db()
    symptoms = db.execute(
        'SELECT s.id, symptom_name, s_date, severity, created, author_id, username'
        ' FROM symptom s JOIN user u ON s.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('symptom/symptomIndex.html', symptoms=symptoms)

# create
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    print (request.method)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        symptomStartDate = request.form['symptomStartDate']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO symptom (symptom_name, s_date, severity, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, symptomStartDate, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('symptom.index'))

    return render_template('symptom/symptomCreate.html')
    
# update
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT s.id, symptom_name, severity, created, author_id, username'
        ' FROM symptom s JOIN user u ON s.author_id = u.id'
        ' WHERE s.id = ?',
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
        symptomStartDate = request.form['symptomStartDate']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE symptom SET symptom_name = ?, s_date = ?, severity = ?'
                ' WHERE id = ?',
                (title, symptomStartDate, body, id)
            )
            db.commit()
            return redirect(url_for('symptom.index'))

    return render_template('symptom/symptomUpdate.html', symptom=post)

# delete
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM symptom WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('symptom.index'))