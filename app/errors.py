from flask import render_template
from app import app, db


@app.errorhandler(404)
def error404(error):
    print(error)
    return render_template('404.html'), 404


@app.errorhandler(500)
def error500(error):
    print(error)
    db.session.rollback()
    return render_template('505.html'), 505

