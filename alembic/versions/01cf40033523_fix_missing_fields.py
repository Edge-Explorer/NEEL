"""fix_missing_fields

Revision ID: 01cf40033523
Revises: b94d612fa042
Create Date: 2026-02-14 18:21:57.808227

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01cf40033523'
down_revision: Union[str, Sequence[str], None] = 'b94d612fa042'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
