"""empty message

Revision ID: d20d36b3543e
Revises: 6a1d150a2788
Create Date: 2018-06-02 21:56:18.524069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd20d36b3543e'
down_revision = '6a1d150a2788'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activities', sa.Column('max_age', sa.SMALLINT(), nullable=True))
    op.add_column('activities', sa.Column('min_age', sa.SMALLINT(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('activities', 'min_age')
    op.drop_column('activities', 'max_age')
    # ### end Alembic commands ###
