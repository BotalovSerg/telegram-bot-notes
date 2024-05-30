"""init

Revision ID: 6de0da2c697a
Revises: 
Create Date: 2024-05-30 20:42:30.410413

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "6de0da2c697a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("telegram_id", sa.BIGINT(), nullable=False),
        sa.Column("fullname", sa.TEXT(), nullable=False),
        sa.Column(
            "registered_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("telegram_id"),
    )
    op.create_table(
        "notes",
        sa.Column("note_id", sa.UUID(), nullable=False),
        sa.Column("note", sa.TEXT(), nullable=False),
        sa.Column("date", sa.TEXT(), nullable=False),
        sa.Column("telegram_id", sa.BIGINT(), nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["telegram_id"], ["users.telegram_id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("note_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("notes")
    op.drop_table("users")
    # ### end Alembic commands ###
