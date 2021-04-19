from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from dashboard.auth import login_required
from dashboard.db import get_db

bp = Blueprint('indicator', __name__, url_prefix='/indicator')


@bp.route('/')
def index():
    db = get_db()

    doctors_counts = db.execute(
        'SELECT COUNT(*) FROM doctor'
    ).fetchall()

    trip_counts = db.execute(
        'SELECT COUNT(*) FROM trip'
    ).fetchall()

    medicine_counts = db.execute(
        'SELECT COUNT(*) FROM medicine'
    ).fetchall()

    symptom_counts = db.execute(
        'SELECT COUNT(*) FROM symptom'
    ).fetchall()

    takeout_counts = db.execute(
        'SELECT COUNT(*) FROM takeout'
    ).fetchall()

    indicators = doctors_counts[0][0] + trip_counts[0][0] + medicine_counts[0][0] \
                 + symptom_counts[0][0] + takeout_counts[0][0]

    score = scores(doctors_counts[0][0], trip_counts[0][0], medicine_counts[0][0], symptom_counts[0][0],
                   takeout_counts[0][0])

    possibility = evaluation(score)

    return render_template('Indicator/indicatorIndex.html',
                           indicators=indicators,
                           doctors_counts=doctors_counts,
                           trip_counts=trip_counts,
                           medicine_counts=medicine_counts,
                           symptom_counts=symptom_counts,
                           takeout_counts=takeout_counts,
                           possibility=possibility
                           )


def scores(doctor, trip, medicine, symptom, takeout):
    scores = 0
    if doctor:
        scores += doctor * 15
    if trip:
        scores += trip * 20
    if medicine:
        scores -= medicine * 5
    if symptom:
        scores += symptom * 40
    if takeout:
        scores += takeout * 5

    return scores


def evaluation(scores):
    if 0 <= scores < 10:
        return 'very low'
    elif 10 <= scores < 20:
        return 'low'
    elif 20 <= scores < 30:
        return 'medium'
    elif 30 <= scores < 50:
        return 'high'
    elif scores > 50:
        return 'very high'
    elif scores > 100:
        return 'extremely high'

