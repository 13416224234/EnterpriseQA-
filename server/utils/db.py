from extensions import db

def init_db():
    db.create_all()
    print("Database tables created successfully")

def reset_db():
    db.drop_all()
    db.create_all()
    print("Database reset successfully")