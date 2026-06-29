from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.chat import Conversation, Message
from models.user import User

qa_bp = Blueprint("qa", __name__)

@qa_bp.route("/conversations", methods=["GET"])
@jwt_required()
def list_conversations():
    user_id = int(get_jwt_identity())
    conversations = Conversation.query.filter_by(user_id=user_id).order_by(Conversation.updated_at.desc()).all()
    return jsonify({"code": 200, "data": [c.to_dict() for c in conversations]})

@qa_bp.route("/conversations", methods=["POST"])
@jwt_required()
def create_conversation():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    title = data.get("title", "New conversation")
    conv = Conversation(user_id=user_id, title=title)
    db.session.add(conv)
    db.session.commit()
    return jsonify({"code": 200, "msg": "Created", "data": conv.to_dict()})

@qa_bp.route("/conversations/<int:conv_id>", methods=["GET"])
@jwt_required()
def get_conversation(conv_id):
    user_id = int(get_jwt_identity())
    conv = Conversation.query.filter_by(id=conv_id, user_id=user_id).first()
    if not conv:
        return jsonify({"code": 404, "msg": "Conversation not found"}), 200
    messages = Message.query.filter_by(conversation_id=conv_id).order_by(Message.created_at).all()
    return jsonify({"code": 200, "data": {"conversation": conv.to_dict(), "messages": [m.to_dict() for m in messages]}})

@qa_bp.route("/conversations/<int:conv_id>/messages", methods=["GET"])
@jwt_required()
def get_messages(conv_id):
    user_id = int(get_jwt_identity())
    conv = Conversation.query.filter_by(id=conv_id, user_id=user_id).first()
    if not conv:
        return jsonify({"code": 404, "msg": "Conversation not found"}), 200
    messages = Message.query.filter_by(conversation_id=conv_id).order_by(Message.created_at).all()
    return jsonify({"code": 200, "data": [m.to_dict() for m in messages]})

@qa_bp.route("/conversations/<int:conv_id>", methods=["DELETE"])
@jwt_required()
def delete_conversation(conv_id):
    user_id = int(get_jwt_identity())
    conv = Conversation.query.filter_by(id=conv_id, user_id=user_id).first()
    if not conv:
        return jsonify({"code": 404, "msg": "Conversation not found"}), 200
    Message.query.filter_by(conversation_id=conv_id).delete()
    db.session.delete(conv)
    db.session.commit()
    return jsonify({"code": 200, "msg": "Deleted"})

@qa_bp.route("/ask", methods=["POST"])
@jwt_required()
def ask_question():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    question = data.get("question", "").strip()
    conversation_id = data.get("conversation_id")

    if not question:
        return jsonify({"code": 400, "msg": "Question cannot be empty"}), 200

    if conversation_id:
        conv = Conversation.query.filter_by(id=conversation_id, user_id=user_id).first()
        if not conv:
            return jsonify({"code": 404, "msg": "Conversation not found"}), 200
    else:
        conv = Conversation(user_id=user_id, title=question[:50])
        db.session.add(conv)
        db.session.flush()

    user_msg = Message(conversation_id=conv.id, role="user", content=question)
    db.session.add(user_msg)
    db.session.flush()

    try:
        from services.rag_service import RAGService
        rag = RAGService()
        result = rag.ask(question)
        answer = result["answer"]
        sources = result["sources"]
    except Exception as e:
        answer = f"Error processing question: {str(e)}"
        sources = []

    assistant_msg = Message(
        conversation_id=conv.id,
        role="assistant",
        content=answer,
        sources=str(sources) if sources else None
    )
    db.session.add(assistant_msg)
    db.session.commit()

    return jsonify({
        "code": 200,
        "data": {
            "conversation_id": conv.id,
            "question": user_msg.to_dict(),
            "answer": assistant_msg.to_dict()
        }
    })