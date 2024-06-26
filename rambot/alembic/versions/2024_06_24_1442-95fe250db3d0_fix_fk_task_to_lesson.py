"""fix fk task to lesson

Revision ID: 95fe250db3d0
Revises: 94b68b51649d
Create Date: 2024-06-24 14:42:01.300930

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "95fe250db3d0"
down_revision: Union[str, None] = "94b68b51649d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "tasks", "lesson_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.drop_constraint("tasks_lesson_id_fkey", "tasks", type_="foreignkey")
    op.create_foreign_key(None, "tasks", "lessons", ["lesson_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "tasks", type_="foreignkey")
    op.create_foreign_key(
        "tasks_lesson_id_fkey",
        "tasks",
        "lessons",
        ["lesson_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.alter_column(
        "tasks", "lesson_id", existing_type=sa.INTEGER(), nullable=True
    )
    # ### end Alembic commands ###
