"""renamed tabel completed_lessons to in_progress_lessons

Revision ID: c07617185221
Revises: 2a463bbf86a2
Create Date: 2024-06-15 18:49:11.448880

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c07617185221"
down_revision: Union[str, None] = "2a463bbf86a2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("completed_lessons")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "completed_lessons",
        sa.Column(
            "name", sa.VARCHAR(length=255), autoincrement=False, nullable=False
        ),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "teacher_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "student_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column("point", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "description",
            sa.VARCHAR(length=255),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["profiles_student.id"],
            name="completed_lessons_student_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["teacher_id"],
            ["profiles_teacher.id"],
            name="completed_lessons_teacher_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id", name="completed_lessons_pkey"),
        sa.UniqueConstraint("name", name="completed_lessons_name_key"),
    )
    # ### end Alembic commands ###
