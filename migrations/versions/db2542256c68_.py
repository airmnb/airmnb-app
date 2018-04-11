"""empty message

Revision ID: db2542256c68
Revises: 2c4144d75645
Create Date: 2018-04-06 21:52:42.693290

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'db2542256c68'
down_revision = '2c4144d75645'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('locations',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('langitude', postgresql.DOUBLE_PRECISION(), nullable=False),
    sa.Column('latitude', postgresql.DOUBLE_PRECISION(), nullable=False),
    sa.Column('addr1', sa.TEXT(), nullable=False),
    sa.Column('addr2', sa.TEXT(), nullable=True),
    sa.Column('addr3', sa.TEXT(), nullable=True),
    sa.Column('city', sa.TEXT(), nullable=False),
    sa.Column('state', sa.TEXT(), nullable=False),
    sa.Column('country', sa.TEXT(), nullable=False),
    sa.Column('postcode', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activities',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('name', sa.TEXT(), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('location_id', postgresql.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['location_id'], [u'locations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('babies',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('family_name', sa.TEXT(), nullable=False),
    sa.Column('given_name', sa.TEXT(), nullable=False),
    sa.Column('gender', sa.TEXT(), nullable=True),
    sa.Column('dob', sa.DATE(), nullable=False),
    sa.Column('parent_id', postgresql.UUID(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], [u'users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column(u'users', 'avartar',
               existing_type=postgresql.BYTEA(),
               nullable=True)
    op.alter_column(u'users', 'source_type',
               existing_type=sa.TEXT(),
               nullable=True)
    op.drop_constraint(u'users_avartar_key', 'users', type_='unique')
    op.drop_constraint(u'users_created_at_key', 'users', type_='unique')
    op.drop_constraint(u'users_dob_key', 'users', type_='unique')
    op.drop_constraint(u'users_email_key', 'users', type_='unique')
    op.drop_constraint(u'users_source_type_key', 'users', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(u'users_source_type_key', 'users', ['source_type'])
    op.create_unique_constraint(u'users_email_key', 'users', ['email'])
    op.create_unique_constraint(u'users_dob_key', 'users', ['dob'])
    op.create_unique_constraint(u'users_created_at_key', 'users', ['created_at'])
    op.create_unique_constraint(u'users_avartar_key', 'users', ['avartar'])
    op.alter_column(u'users', 'source_type',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column(u'users', 'avartar',
               existing_type=postgresql.BYTEA(),
               nullable=False)
    op.drop_table('babies')
    op.drop_table('activities')
    op.drop_table('locations')
    # ### end Alembic commands ###