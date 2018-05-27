"""empty message

Revision ID: 4d6dd59e7aaa
Revises: efd80a36c8b2
Create Date: 2018-05-22 22:49:19.172490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d6dd59e7aaa'
down_revision = 'efd80a36c8b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('activities', 'status',
               existing_type=sa.SMALLINT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('activities', 'status',
               existing_type=sa.SMALLINT(),
               nullable=False)
    # ### end Alembic commands ###