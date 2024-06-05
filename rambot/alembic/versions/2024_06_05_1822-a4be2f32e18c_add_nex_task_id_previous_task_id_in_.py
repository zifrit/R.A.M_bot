"""add nex_task_id previous_task_id in tasks

Revision ID: a4be2f32e18c
Revises: 46168f8bf527
Create Date: 2024-06-05 18:22:27.693666

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a4be2f32e18c"
down_revision: Union[str, None] = "46168f8bf527"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "tasks", sa.Column("nex_task_id", sa.Integer(), nullable=True)
    )
    op.add_column(
        "tasks", sa.Column("previous_task_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        None, "tasks", "tasks", ["nex_task_id"], ["id"], ondelete="set null"
    )
    op.create_foreign_key(
        None,
        "tasks",
        "tasks",
        ["previous_task_id"],
        ["id"],
        ondelete="set null",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "tasks", type_="foreignkey")
    op.drop_constraint(None, "tasks", type_="foreignkey")
    op.drop_column("tasks", "previous_task_id")
    op.drop_column("tasks", "nex_task_id")
    # ### end Alembic commands ###