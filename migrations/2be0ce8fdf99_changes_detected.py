"""Changes Detected!

Revision ID: 2be0ce8fdf99
Revises: e6d9f26fefdd
Create Date: 2023-11-19 17:52:23.177775

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2be0ce8fdf99'
down_revision: Union[str, None] = 'e6d9f26fefdd'
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
