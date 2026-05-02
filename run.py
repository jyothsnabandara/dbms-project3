from app import create_app, db
from app import models  # noqa: F401

app = create_app()

@app.cli.command('init-db')
def init_db():
    """Create local SQLite database tables from SQLAlchemy models."""
    db.drop_all()
    db.create_all()
    print('Database initialized successfully.')

if __name__ == '__main__':
    app.run(debug=True)
