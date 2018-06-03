"""empty message

Revision ID: dc0f76ba52fe
Revises: b4fdfae9c436
Create Date: 2018-06-03 16:07:49.260525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc0f76ba52fe'
down_revision = 'b4fdfae9c436'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activities', sa.Column('time_offset', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('activities', 'time_offset')
    # ### end Alembic commands ###
