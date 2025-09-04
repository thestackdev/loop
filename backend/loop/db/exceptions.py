"""Database exception handling utilities."""
from typing import Any

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError


class DatabaseErrorHandler:
    """Handles database constraint violations and converts them to HTTP exceptions."""

    @staticmethod
    def handle_constraint_error(error: IntegrityError, operation: str = "operation") -> HTTPException:
        """
        Convert SQLAlchemy IntegrityError to appropriate HTTPException.

        Args:
            error: The IntegrityError from SQLAlchemy
            operation: Description of the operation that failed

        Returns:
            HTTPException with appropriate status code and message
        """
        if isinstance(error.orig, UniqueViolationError):
            return DatabaseErrorHandler._handle_unique_violation(error.orig, operation)
        elif isinstance(error.orig, ForeignKeyViolationError):
            return DatabaseErrorHandler._handle_foreign_key_violation(error.orig, operation)
        else:
            return HTTPException(
                status_code=400,
                detail=f"Database constraint violation during {operation}"
            )

    @staticmethod
    def _handle_unique_violation(error: UniqueViolationError, operation: str) -> HTTPException:
        """Handle unique constraint violations."""
        constraint_name = getattr(error, 'constraint_name', 'unknown')

        # Map specific constraints to user-friendly messages
        constraint_messages = {
            'uq_topic_subtopic_order': 'A subtopic with this order already exists for this topic',
            'uq_topic_name': 'A topic with this name already exists',
            'uq_user_topic': 'User is already subscribed to this topic',
            'uq_subtopic_name_topic': 'A subtopic with this name already exists for this topic',
        }

        # Also check the error detail for specific constraint patterns
        error_detail = str(error)
        if 'topic_id, order_index' in error_detail:
            constraint_name = 'uq_topic_subtopic_order'

        message = constraint_messages.get(constraint_name, f'Duplicate entry detected during {operation}')

        return HTTPException(
            status_code=409,  # Conflict
            detail=message
        )

    @staticmethod
    def _handle_foreign_key_violation(error: ForeignKeyViolationError, operation: str) -> HTTPException:
        """Handle foreign key constraint violations."""
        return HTTPException(
            status_code=400,
            detail=f"Referenced resource not found during {operation}"
        )


def handle_db_errors(operation: str = "database operation"):
    """
    Decorator to handle database errors in DAO methods.

    Args:
        operation: Description of the operation for error messages
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except IntegrityError as e:
                raise DatabaseErrorHandler.handle_constraint_error(e, operation)
        return wrapper
    return decorator
