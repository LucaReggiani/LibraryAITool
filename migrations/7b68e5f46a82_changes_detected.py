"""Changes Detected!

Revision ID: 7b68e5f46a82
Revises: b1a58aba11c5
Create Date: 2023-11-09 18:36:45.825835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b68e5f46a82'
down_revision: Union[str, None] = 'b1a58aba11c5'
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