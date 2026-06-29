"""
Logging utility for EnterpriseQA.
Logs to server/logs/ directory with daily rotation.
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

_qa_logger = None
_upload_logger = None
_action_logger = None


def _get_logger(name, filename, level=logging.INFO):
    """Get or create a named logger with file handler."""
    logger = logging.getLogger("enterprise_qa." + name)
    if logger.handlers:
        return logger
    logger.setLevel(level)
    logger.propagate = False

    path = os.path.join(LOG_DIR, filename)
    handler = RotatingFileHandler(path, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8")
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    return logger


def get_qa_logger():
    """Logger for Q&A requests."""
    global _qa_logger
    if _qa_logger is None:
        _qa_logger = _get_logger("qa", "qa.log")
    return _qa_logger


def get_upload_logger():
    """Logger for document uploads."""
    global _upload_logger
    if _upload_logger is None:
        _upload_logger = _get_logger("upload", "upload.log")
    return _upload_logger


def get_action_logger():
    """Logger for user actions (login, logout, etc)."""
    global _action_logger
    if _action_logger is None:
        _action_logger = _get_logger("action", "action.log")
    return _action_logger


def log_qa(user_id, username, question, answer_preview, sources_count, elapsed_ms):
    """Log a Q&A interaction."""
    get_qa_logger().info(
        "user=%s(%d) | q=%s | sources=%d | elapsed=%dms | answer=%.100s",
        username, user_id, question[:60], sources_count, elapsed_ms, answer_preview
    )


def log_upload(user_id, username, filename, file_type, file_size, status):
    """Log a document upload."""
    get_upload_logger().info(
        "user=%s(%d) | file=%s | type=%s | size=%d | status=%s",
        username, user_id, filename, file_type, file_size, status
    )


def log_action(user_id, username, action, detail=""):
    """Log a user action."""
    get_action_logger().info(
        "user=%s(%d) | action=%s | detail=%s",
        username, user_id, action, detail
    )
