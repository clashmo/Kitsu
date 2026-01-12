"""update refresh tokens constraints

Revision ID: 0008
Revises: 0007
Create Date: 2026-01-12 15:10:00.000000
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("refresh_tokens") as batch_op:
        batch_op.drop_constraint(
            op.f("uq_refresh_tokens_user_id"), type_="unique"
        )
        batch_op.create_unique_constraint(
            op.f("uq_refresh_tokens_token_hash"), ["token_hash"]
        )


def downgrade() -> None:
    with op.batch_alter_table("refresh_tokens") as batch_op:
        batch_op.drop_constraint(
            op.f("uq_refresh_tokens_token_hash"), type_="unique"
        )
        batch_op.create_unique_constraint(
            op.f("uq_refresh_tokens_user_id"), ["user_id"]
        )
