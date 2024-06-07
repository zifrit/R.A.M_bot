"""rename nex_task_id > next_task_id in Tasks

Revision ID: fc43576dc878
Revises: 0bbc8ccce1b1
Create Date: 2024-06-07 15:32:49.765662

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fc43576dc878"
down_revision: Union[str, None] = "0bbc8ccce1b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "tasks", sa.Column("next_task_id", sa.Integer(), nullable=True)
    )
    op.drop_constraint("tasks_nex_task_id_fkey", "tasks", type_="foreignkey")
    op.create_foreign_key(
        None, "tasks", "tasks", ["next_task_id"], ["id"], ondelete="set null"
    )
    op.drop_column("tasks", "nex_task_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "tasks",
        sa.Column(
            "nex_task_id", sa.INTEGER(), autoincrement=False, nullable=True
        ),
    )
    op.drop_constraint(None, "tasks", type_="foreignkey")
    op.create_foreign_key(
        "tasks_nex_task_id_fkey",
        "tasks",
        "tasks",
        ["nex_task_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.drop_column("tasks", "next_task_id")
    # ### end Alembic commands ###
