"""remove unique from name in in_progress_lessons tabel

Revision ID: 9637e8883988
Revises: da50845f1fdd
Create Date: 2024-06-15 20:13:59.189528

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9637e8883988"
down_revision: Union[str, None] = "da50845f1fdd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "in_progress_lessons_name_key", "in_progress_lessons", type_="unique"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(
        "in_progress_lessons_name_key", "in_progress_lessons", ["name"]
    )
    # ### end Alembic commands ###
