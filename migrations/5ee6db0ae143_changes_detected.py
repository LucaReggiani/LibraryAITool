"""Changes Detected!

Revision ID: 5ee6db0ae143
Revises: a69721d2dd38
Create Date: 2023-11-17 16:30:38.961661

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ee6db0ae143'
down_revision: Union[str, None] = 'a69721d2dd38'
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
