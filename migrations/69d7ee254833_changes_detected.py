"""Changes Detected!

Revision ID: 69d7ee254833
Revises: 74b0e0758508
Create Date: 2023-11-15 00:22:31.951082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '69d7ee254833'
down_revision: Union[str, None] = '74b0e0758508'
branch_labels: Union[str, Sequence[str], None] = ()
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User', sa.Column('lastname', sa.String(length=55), nullable=False))
    op.drop_column('User', 'surname')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User', sa.Column('surname', mysql.VARCHAR(length=55), nullable=False))
    op.drop_column('User', 'lastname')
    # ### end Alembic commands ###
