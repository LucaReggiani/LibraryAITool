"""Changes Detected!

Revision ID: f2e2a81a13ee
Revises: f680d7d85ce2
Create Date: 2023-11-14 19:24:34.983582

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2e2a81a13ee'
down_revision: Union[str, None] = 'f680d7d85ce2'
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