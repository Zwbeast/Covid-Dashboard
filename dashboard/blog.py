from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from dashboard.auth import login_required
from dashboard.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    medicines = db.execute(
        'SELECT p.id, med_name, direction, created, author_id, username'
        ' FROM medicine p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    trips = db.execute(
        'SELECT t.id, destination, people, s_date, e_date, created, author_id, username'
        ' FROM trip t JOIN user u ON t.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    takeouts = db.execute(
        'SELECT t.id, rest_name, rest_address, order_date, created, author_id, username'
        ' FROM takeout t JOIN user u ON t.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    doctors = db.execute(
        'SELECT d.id, doc_type, doc_address, doc_date, created, author_id, username'
        ' FROM doctor d JOIN user u ON d.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    newss = db.execute(
        'SELECT n.id, people, covid_test, close_contact, created, author_id, username'
        ' FROM news n JOIN user u ON n.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    symptoms = db.execute(
        'SELECT s.id, symptom_name, s_date, severity, created, author_id, username'
        ' FROM symptom s JOIN user u ON s.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('blog/index.html', 
                            posts=posts, 
                            medicines=medicines, 
                            trips=trips, 
                            takeouts=takeouts,
                            doctors=doctors,
                            newss=newss,
                            symptoms=symptoms)

# create
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
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
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')
    
# update
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
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
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

# delete
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))