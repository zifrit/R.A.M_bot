"""lesson_id > completed_lesson_id in completed_tasks

Revision ID: 578dd1ba72f6
Revises: ee009a465ae2
Create Date: 2024-05-31 17:23:55.892951

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "578dd1ba72f6"
down_revision: Union[str, None] = "ee009a465ae2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "completed_tasks",
        sa.Column("completed_lesson_id", sa.Integer(), nullable=False),
    )
    op.drop_constraint(
        "completed_tasks_lesson_id_fkey", "completed_tasks", type_="foreignkey"
    )
    op.create_foreign_key(
        None,
        "completed_tasks",
        "completed_lessons",
        ["completed_lesson_id"],
        ["id"],
    )
    op.drop_column("completed_tasks", "lesson_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "completed_tasks",
        sa.Column(
            "lesson_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
    )
    op.drop_constraint(None, "completed_tasks", type_="foreignkey")
    op.create_foreign_key(
        "completed_tasks_lesson_id_fkey",
        "completed_tasks",
        "lessons",
        ["lesson_id"],
        ["id"],
    )
    op.drop_column("completed_tasks", "completed_lesson_id")
    # ### end Alembic commands ###
