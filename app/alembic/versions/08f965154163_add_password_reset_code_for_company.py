"""add password_reset_code for company

Revision ID: 08f965154163
Revises: 631375b80e9e
Create Date: 2023-03-05 19:54:27.402120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08f965154163'
down_revision = '631375b80e9e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('company', sa.Column('password_reset_code', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('company', 'password_reset_code')
