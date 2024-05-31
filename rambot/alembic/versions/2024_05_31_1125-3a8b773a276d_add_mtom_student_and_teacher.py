"""add mtom student and teacher

Revision ID: 3a8b773a276d
Revises: 346f2e6cf390
Create Date: 2024-05-31 11:25:25.293697

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3a8b773a276d"
down_revision: Union[str, None] = "346f2e6cf390"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "association_student_teacher",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("profiles_student_id", sa.Integer(), nullable=False),
        sa.Column("profiles_teacher_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["profiles_student_id"],
            ["profiles_student.id"],
        ),
        sa.ForeignKeyConstraint(
            ["profiles_teacher_id"],
            ["profiles_teacher.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "profiles_student_id",
            "profiles_teacher_id",
            name="idx_unique_student_teacher",
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("association_student_teacher")
    # ### end Alembic commands ###