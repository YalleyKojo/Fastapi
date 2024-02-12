"""add post table

Revision ID: b334ba77e93f
Revises: 6a70aa610612
Create Date: 2024-02-07 14:55:15.182762

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b334ba77e93f'
down_revision: Union[str, None] = '6a70aa610612'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',
        sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
        sa.Column('title',sa.String(),nullable=False),
        sa.Column('content',sa.String(),nullable=False),
        sa.Column('published',sa.Boolean(),nullable=False,server_default='True'),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')),
        sa.Column('owner_id',sa.Integer(),nullable=False),
        
       
        )
    op.create_foreign_key('posts_users_fk',source_table="posts",referent_table="users",
                          local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('posts_usrs_fk',table_name='posts')
    op.drop_table('posts')
    pass
