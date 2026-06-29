"""
System initialization script.
Run once to set up database and verify dependencies.
Usage: python scripts/init_system.py
"""
import os
import sys
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models.user import User


def init_database():
    """Create all tables and seed admin user."""
    with app.app_context():
        db.create_all()
        print("[OK] Database tables created.")

        admin = User.query.filter_by(username="admin").first()
        if admin:
            print("[OK] Admin user already exists (id=%d, role=%s)." % (admin.id, admin.role))
            if admin.role != "admin":
                admin.role = "admin"
                db.session.commit()
                print("[OK] Admin user role upgraded to admin.")
        else:
            pw = hashlib.md5("123456".encode()).hexdigest()
            u = User(username="admin", password=pw, email="admin@company.com",
                     real_name="System Admin", role="admin", status=1)
            db.session.add(u)
            db.session.commit()
            print("[OK] Admin user created (admin / 123456).")


def check_ollama():
    """Check if Ollama is running and required models are available."""
    import urllib.request
    import json
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags")
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read().decode())
        models = {m["name"].split(":")[0] for m in data.get("models", [])}
        needed = {"nomic-embed-text", "qwen3.5-4b"}
        found = models & needed
        missing = needed - models
        if found:
            print("[OK] Ollama models found: %s" % ", ".join(sorted(found)))
        if missing:
            print("[WARN] Missing models: %s. Run: ollama pull %s" %
                  (", ".join(missing), " ".join(missing)))
    except Exception as e:
        print("[WARN] Ollama not reachable at localhost:11434 (%s)" % e)


def check_chroma():
    """Verify Chroma vector store is accessible."""
    try:
        from services.embedding_service import EmbeddingService
        es = EmbeddingService()
        count = es.vector_store._collection.count()
        print("[OK] Chroma connected, %d vectors stored." % count)
    except Exception as e:
        print("[WARN] Chroma check failed: %s" % e)


if __name__ == "__main__":
    print("=== EnterpriseQA System Initialization ===\n")
    init_database()
    check_ollama()
    check_chroma()
    print("\n=== Done ===")
