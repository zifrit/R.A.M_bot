"""set default is_student and is_teacher in users

Revision ID: de97f059c9fb
Revises: d2cb2d1d6349
Create Date: 2024-05-30 19:20:05.903871

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "de97f059c9fb"
down_revision: Union[str, None] = "d2cb2d1d6349"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
