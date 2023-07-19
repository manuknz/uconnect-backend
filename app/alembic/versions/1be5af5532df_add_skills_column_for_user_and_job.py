"""add skills column for user and job

Revision ID: 1be5af5532df
Revises: 0da0ffebab71
Create Date: 2023-07-12 01:20:39.413084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1be5af5532df"
down_revision = "0da0ffebab71"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("job", sa.Column("skill", sa.JSON, nullable=True))
    op.add_column("user", sa.Column("skill", sa.JSON, nullable=True))
    pass


def downgrade() -> None:
    op.drop_column("job", "skill")
    op.drop_column("user", "skill")
    pass
