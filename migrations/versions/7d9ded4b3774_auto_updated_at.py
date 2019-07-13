"""auto updated_at

Revision ID: 7d9ded4b3774
Revises: 748ffd4c62c2
Create Date: 2019-07-13 20:45:15.072018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7d9ded4b3774"
down_revision = "748ffd4c62c2"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(
        sa.text(
            """create or replace function update_updated_at()
        returns trigger as
        $$begin
            if old.updated_at = new.updated_at then
                new.updated_at := now();
            end if;
            return new;
        end;$$ language plpgsql;"""
        )
    )
    conn.execute(
        sa.text(
            "create trigger auto_updated_at before update on accounts "
            "for each row execute procedure update_updated_at();"
        )
    )
    conn.execute(
        sa.text(
            "create trigger auto_updated_at before update on questions "
            "for each row execute procedure update_updated_at();"
        )
    )
    conn.execute(
        sa.text(
            "create trigger auto_updated_at before update on answers "
            "for each row execute procedure update_updated_at();"
        )
    )
    conn.execute(
        sa.text(
            "create trigger auto_updated_at before update on tokens "
            "for each row execute procedure update_updated_at();"
        )
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("drop function update_updated_at() cascade;"))
