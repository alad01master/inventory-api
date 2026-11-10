"""baseline existing schema

Revision ID: f2074a37288b
Revises: 981e4935a9fe
Create Date: 2026-11-10 15:19:04.814489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2074a37288b'
down_revision: Union[str, Sequence[str], None] = '981e4935a9fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
