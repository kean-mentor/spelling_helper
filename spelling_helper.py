from app import create_app
from app.models import populate_db


app = create_app()


if not app.config['TESTING']:
    app_context = app.app_context()
    app_context.push()
    populate_db()
    app_context.pop()
