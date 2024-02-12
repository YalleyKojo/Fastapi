"""add votes table

Revision ID: 3195e5e1db4f
Revises: 9e6b7fc75518
Create Date: 2024-02-10 15:38:58.291036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3195e5e1db4f'
down_revision: Union[str, None] = '9e6b7fc75518'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('votes',
                    sa.Column('user_id',sa.Integer(),nullable=False),
                    sa.Column('post_id',sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['post_id'],['posts.id'],ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'],['users.id'],ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id','post_id')
                    )
    


def downgrade() -> None:
    op.drop_table('votes')
    
