"""Add country and municipality to accounts

Revision ID: 37f4d9b2dd64
Revises: 68b55600e39b
Create Date: 2025-05-24 01:56:46.443626

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37f4d9b2dd64'
down_revision: Union[str, None] = '68b55600e39b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add columns 'country' and 'municipality' to 'accounts' table
    op.add_column('accounts', sa.Column('country', sa.String(), nullable=True))
    op.add_column('accounts', sa.Column('municipality', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove columns 'country' and 'municipality' from 'accounts' table
    op.drop_column('accounts', 'country')
    op.drop_column('accounts', 'municipality')
