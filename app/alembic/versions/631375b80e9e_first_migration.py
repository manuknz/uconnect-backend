"""First migration

Revision ID: 631375b80e9e
Revises: 
Create Date: 2023-02-25 18:06:52.190414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '631375b80e9e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('password_reset_code', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'password_reset_code')
