"""empty message

Revision ID: 6f3d6e6616ad
Revises: e3d0dfb4cc2c
Create Date: 2018-05-07 23:13:01.339618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f3d6e6616ad'
down_revision = 'e3d0dfb4cc2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('babies', 'dob',
               existing_type=sa.DATE(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('babies', 'dob',
               existing_type=sa.DATE(),
               nullable=False)
    # ### end Alembic commands ###