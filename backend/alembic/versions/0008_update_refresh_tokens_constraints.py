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
    old_constraint_name = "uq_refresh_tokens_user_id"
    new_constraint_name = "uq_refresh_tokens_token_hash"

    with op.batch_alter_table("refresh_tokens") as batch_op:
        batch_op.drop_constraint(old_constraint_name, type_="unique")
        batch_op.create_unique_constraint(new_constraint_name, ["token_hash"])


def downgrade() -> None:
    old_constraint_name = "uq_refresh_tokens_user_id"
    new_constraint_name = "uq_refresh_tokens_token_hash"

    with op.batch_alter_table("refresh_tokens") as batch_op:
        batch_op.drop_constraint(new_constraint_name, type_="unique")
        batch_op.create_unique_constraint(old_constraint_name, ["user_id"])
