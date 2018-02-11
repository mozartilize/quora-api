"""create uuid-ossp extension

Revision ID: 98f1a9fe4709
Revises:
Create Date: 2018-02-12 00:33:44.075590

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '98f1a9fe4709'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text('create EXTENSION if not EXISTS "uuid-ossp";'))


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text('drop extension if exists "uuid-ossp";'))
