"""Changes Detected!

Revision ID: d6ab53a462d7
Revises: 7b68e5f46a82
Create Date: 2023-11-09 18:37:17.571402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6ab53a462d7'
down_revision: Union[str, None] = '7b68e5f46a82'
branch_labels: Union[str, Sequence[str], None] = ()
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###