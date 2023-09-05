"""add users column for job

Revision ID: 49738f5e8e2b
Revises: 1be5af5532df
Create Date: 2023-09-05 01:45:56.867299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "49738f5e8e2b"
down_revision = "1be5af5532df"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("job", sa.Column("user", sa.JSON, nullable=True))


def downgrade() -> None:
    op.drop_column("job", "user")
