from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from dashboard.auth import login_required
from dashboard.db import get_db

bp = Blueprint('news', __name__, url_prefix='/news')

@bp.route('/')
def index():
    db = get_db()
    newss = db.execute(
        'SELECT n.id, people, covid_test, created, author_id, username'
        ' FROM news n JOIN user u ON n.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('news/newsIndex.html', newss=newss)

# create
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    print (request.method)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        closeContact = request.form['closeContact']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO news (people, covid_test, close_contact, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, closeContact, g.user['id'])
            )
            db.commit()
            return redirect(url_for('news.index'))

    return render_template('news/newsCreate.html')
    
# update
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT n.id, people, covid_test, close_contact, created, author_id, username'
        ' FROM news n JOIN user u ON n.author_id = u.id'
        ' WHERE n.id = ?',
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
        closeContact = request.form['closeContact']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE news SET people = ?, covid_test = ?, close_contact = ?'
                ' WHERE id = ?',
                (title, body, closeContact, id)
            )
            db.commit()
            return redirect(url_for('news.index'))

    return render_template('news/newsUpdate.html', news=post)

# delete
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM news WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('news.index'))