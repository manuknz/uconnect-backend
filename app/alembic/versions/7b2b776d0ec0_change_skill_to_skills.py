"""change skill to skills

Revision ID: 7b2b776d0ec0
Revises: 49738f5e8e2b
Create Date: 2023-11-15 02:28:10.534766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7b2b776d0ec0"
down_revision = "49738f5e8e2b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("job", "skill", new_column_name="skills")
    op.alter_column("user", "skill", new_column_name="skills")
    pass


def downgrade() -> None:
    op.alter_column("job", "skills", new_column_name="skill")
    op.alter_column("user", "skills", new_column_name="skill")
    pass
