"""add_job_city_file_tables

Revision ID: 0da0ffebab71
Revises: 08f965154163
Create Date: 2023-04-12 03:30:32.128993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0da0ffebab71'
down_revision = '08f965154163'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('city',
                    sa.Column('id', sa.BigInteger, primary_key=True, index=True),
                    sa.Column('name', sa.String, nullable=False))
    op.create_table('file',
                    sa.Column('id', sa.BigInteger, primary_key=True, index=True),
                    sa.Column('content_type', sa.String, nullable=False),
                    sa.Column('file_name', sa.String, nullable=False),
                    sa.Column('file_data', sa.LargeBinary, nullable=False))
    op.create_table('job',
                    sa.Column('id', sa.BigInteger, primary_key=True, index=True),
                    sa.Column('description', sa.String, nullable=False),
                    sa.Column('job_type', sa.String, nullable=False),
                    sa.Column('active', sa.Boolean, nullable=False),
                    sa.Column('creation_date', sa.Date, nullable=False),
                    sa.Column('company_id', sa.Integer, sa.ForeignKey('company.id'), nullable=False),
                    sa.Column('career_id', sa.Integer, sa.ForeignKey('career.id'), nullable=False),
                    sa.Column('city_id', sa.Integer, sa.ForeignKey('city.id'), nullable=False),
                    sa.Column('file_id', sa.Integer, sa.ForeignKey('file.id'), nullable=False))
    op.add_column('users', sa.Column('file_id', sa.Integer(), sa.ForeignKey('file.id'), nullable=True))
    op.rename_table('users', 'user')

def downgrade() -> None:
    op.drop_table('city')
    op.drop_table('file')
    op.drop_table('job')
    op.drop_column('user', 'file_id')
