"""nullable pw_hash

Revision ID: f8325c4f3c77
Revises: eb37f51d95d3
Create Date: 2018-08-29 10:11:09.927659

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f8325c4f3c77'
down_revision = 'eb37f51d95d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accounts', 'pw_hash',
               existing_type=postgresql.BYTEA(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accounts', 'pw_hash',
               existing_type=postgresql.BYTEA(),
               nullable=False)
    # ### end Alembic commands ###
