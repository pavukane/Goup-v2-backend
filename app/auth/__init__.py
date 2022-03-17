from flask import Blueprint

# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__
)


from app.auth import routes