"""create users and educations

Revision ID: c01_users_educations
Revises: 
Create Date: 2025-08-15 00:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "c01_users_educations"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password", sa.String(length=255), nullable=False),
    )

    op.create_table(
        "educations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("degree", sa.String(length=100), nullable=False),
        sa.Column("field", sa.String(length=150), nullable=False),
        sa.Column("institute", sa.String(length=200), nullable=False),
        # Comment out the next two lines if you don't want the relation:
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=True),
    )

    # Useful indexes (optional)
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_educations_user_id", "educations", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_educations_user_id", table_name="educations")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("educations")
    op.drop_table("users")
