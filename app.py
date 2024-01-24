from flask import render_template

from app.__init__ import create_app

app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    """Handles 404 page not found errors"""
    print("404 error with info: " + e)
    return render_template('404.html', user=None)


if __name__ == "__main__":
    app.run(debug=True)
