"""add description in lesson and completed_lessons

Revision ID: 8ff77bf79aa7
Revises: b7537b297bce
Create Date: 2024-06-10 16:46:56.479312

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8ff77bf79aa7"
down_revision: Union[str, None] = "b7537b297bce"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "completed_lessons",
        sa.Column("description", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "lessons",
        sa.Column("description", sa.String(length=255), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("lessons", "description")
    op.drop_column("completed_lessons", "description")
    # ### end Alembic commands ###
