"""fix answer right_answer

Revision ID: 0bbc8ccce1b1
Revises: a4be2f32e18c
Create Date: 2024-06-05 18:25:22.164323

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0bbc8ccce1b1"
down_revision: Union[str, None] = "a4be2f32e18c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "in_progress_tasks",
        "right_answer",
        existing_type=sa.BOOLEAN(),
        type_=sa.String(),
        existing_nullable=False,
    )
    op.alter_column(
        "in_progress_tasks",
        "student_answer",
        existing_type=sa.BOOLEAN(),
        type_=sa.String(),
        existing_nullable=True,
    )
    op.add_column(
        "tasks", sa.Column("right_answer", sa.String(), nullable=False)
    )
    op.alter_column(
        "tasks",
        "answer",
        existing_type=postgresql.JSON(astext_type=sa.Text()),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "tasks",
        "answer",
        existing_type=postgresql.JSON(astext_type=sa.Text()),
        nullable=True,
    )
    op.drop_column("tasks", "right_answer")
    op.alter_column(
        "in_progress_tasks",
        "student_answer",
        existing_type=sa.String(),
        type_=sa.BOOLEAN(),
        existing_nullable=True,
    )
    op.alter_column(
        "in_progress_tasks",
        "right_answer",
        existing_type=sa.String(),
        type_=sa.BOOLEAN(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
