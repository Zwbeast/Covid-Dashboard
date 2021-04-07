from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from dashboard.auth import login_required
from dashboard.db import get_db

bp = Blueprint('trip', __name__, url_prefix='/trip')

@bp.route('/')
def index():
    db = get_db()
    trips = db.execute(
        'SELECT t.id, destination, s_date, e_date, people, created, author_id, username'
        ' FROM trip t JOIN user u ON t.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('trip/tripIndex.html', trips=trips)

# create
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    print (request.method)
    if request.method == 'POST':
        title = request.form['title']
        tripStartDate = request.form['tripStartDate']
        tripEndDate = request.form['tripEndDate']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO trip (destination, s_date, e_date, people, author_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, tripStartDate, tripEndDate, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('trip.index'))

    return render_template('trip/tripCreate.html')
    
# update
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT t.id, destination, people, s_date, e_date, created, author_id, username'
        ' FROM trip t JOIN user u ON t.author_id = u.id'
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
        tripStartDate = request.form['tripStartDate']
        tripEndDate = request.form['tripEndDate']

        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE trip SET destination = ?, s_date = ?, e_date = ?, people = ?'
                ' WHERE id = ?',
                (title, tripStartDate, tripEndDate, body, id)
            )
            db.commit()
            return redirect(url_for('trip.index'))

    return render_template('trip/tripUpdate.html', trip=post)

# delete
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM trip WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('trip.index'))