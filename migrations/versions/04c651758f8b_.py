"""empty message

Revision ID: 04c651758f8b
Revises: 0cb12390f384
Create Date: 2018-05-13 10:14:12.081640

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '04c651758f8b'
down_revision = '0cb12390f384'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activities', sa.Column('capacity', sa.INTEGER(), nullable=True))
    op.drop_column('images', 'linked')
    op.drop_column('images', 'creator_id')
    op.drop_column('images', 'created_at')
    op.add_column('users', sa.Column('salt', sa.TEXT(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'salt')
    op.add_column('images', sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.add_column('images', sa.Column('creator_id', postgresql.UUID(), autoincrement=False, nullable=False))
    op.add_column('images', sa.Column('linked', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False))
    op.drop_column('activities', 'capacity')
    # ### end Alembic commands ###
