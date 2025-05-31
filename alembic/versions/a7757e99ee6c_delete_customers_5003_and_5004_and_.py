"""Delete customers 5003 and 5004 and cascade

Revision ID: a7757e99ee6c
Revises: 2a9140adc99f
Create Date: 2025-05-31 18:37:01.659908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7757e99ee6c'
down_revision: Union[str, None] = '2a9140adc99f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
