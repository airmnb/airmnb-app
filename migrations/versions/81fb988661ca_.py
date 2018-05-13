"""empty message

Revision ID: 81fb988661ca
Revises: 
Create Date: 2018-05-10 21:35:08.603171

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '81fb988661ca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), autoincrement=False, nullable=False),
    sa.Column('account_name', sa.TEXT(), nullable=True),
    sa.Column('password', sa.BYTEA(), nullable=True),
    sa.Column('source', sa.SMALLINT(), nullable=False),
    sa.Column('email', sa.TEXT(), nullable=True),
    sa.Column('phone', sa.TEXT(), nullable=True),
    sa.Column('family_name', sa.TEXT(), nullable=True),
    sa.Column('given_name', sa.TEXT(), nullable=True),
    sa.Column('full_name', sa.TEXT(), nullable=True),
    sa.Column('gender', sa.BOOLEAN(), nullable=True),
    sa.Column('dob', sa.DATE(), nullable=True),
    sa.Column('last_access_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('account_name')
    )
    op.create_table('wechat_users',
    sa.Column('wechat_user_id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), autoincrement=False, nullable=False),
    sa.Column('open_id', sa.TEXT(), nullable=False),
    sa.Column('avatar_url', sa.TEXT(), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('wechat_user_id')
    )
    op.create_table('images',
    sa.Column('image_id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('blob', postgresql.BYTEA(), nullable=False),
    sa.Column('mime', sa.TEXT(), nullable=True),
    sa.Column('creator_id', postgresql.UUID(), nullable=False),
    sa.Column('linked', sa.BOOLEAN(), server_default=sa.text('False'), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('image_id')
    )
    op.create_table('providers',
    sa.Column('provider_id', postgresql.UUID(), nullable=False),
    sa.Column('certificates', sa.TEXT(), nullable=True),
    sa.Column('info', sa.TEXT(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('provider_id')
    )
    op.create_table('sessions',
    sa.Column('session_id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('session_expires_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(), nullable=True),
    sa.Column('access_token', sa.TEXT(), nullable=True),
    sa.Column('access_token_expires_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('refresh_token', sa.TEXT(), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('session_id')
    )
    op.create_table('venues',
    sa.Column('venue_id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), autoincrement=False, nullable=False),
    sa.Column('name', sa.TEXT(), nullable=False),
    sa.Column('longitude', postgresql.DOUBLE_PRECISION(), nullable=True),
    sa.Column('latitude', postgresql.DOUBLE_PRECISION(), nullable=True),
    sa.Column('addr1', sa.TEXT(), nullable=False),
    sa.Column('addr2', sa.TEXT(), nullable=True),
    sa.Column('addr3', sa.TEXT(), nullable=True),
    sa.Column('city', sa.TEXT(), nullable=False),
    sa.Column('state', sa.TEXT(), nullable=False),
    sa.Column('country', sa.TEXT(), nullable=False),
    sa.Column('postcode', sa.TEXT(), nullable=True),
    sa.Column('info', sa.TEXT(), nullable=True),
    sa.Column('provider_id', postgresql.UUID(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('venue_id')
    )
    op.create_table('activities',
    sa.Column('activity_id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), autoincrement=False, nullable=False),
    sa.Column('name', sa.TEXT(), nullable=False),
    sa.Column('info', sa.TEXT(), nullable=True),
    sa.Column('venue_id', postgresql.UUID(), nullable=False),
    sa.Column('provider_id', postgresql.UUID(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.venue_id'], ),
    sa.PrimaryKeyConstraint('activity_id')
    )
    op.create_table('babies',
    sa.Column('baby_id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), autoincrement=False, nullable=False),
    sa.Column('family_name', sa.TEXT(), nullable=True),
    sa.Column('given_name', sa.TEXT(), nullable=True),
    sa.Column('nick_name', sa.TEXT(), nullable=True),
    sa.Column('full_name', sa.TEXT(), nullable=True),
    sa.Column('gender', sa.TEXT(), nullable=True),
    sa.Column('dob', sa.DATE(), nullable=True),
    sa.Column('creator_id', postgresql.UUID(), nullable=False),
    sa.Column('info', sa.TEXT(), nullable=True),
    sa.Column('avatar_image_id', postgresql.UUID(), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['avatar_image_id'], ['images.image_id'], ),
    sa.ForeignKeyConstraint(['creator_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('baby_id')
    )
    op.create_table('venues_images',
    sa.Column('venue_id', postgresql.UUID(), nullable=False),
    sa.Column('image_id', postgresql.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.image_id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.venue_id'], )
    )
    op.create_table('timeslots',
    sa.Column('timeslot_id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), autoincrement=False, nullable=False),
    sa.Column('activity_id', postgresql.UUID(), nullable=False),
    sa.Column('start', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('end', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.activity_id'], ),
    sa.PrimaryKeyConstraint('timeslot_id')
    )
    op.create_table('vacancies',
    sa.Column('vacancy_id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), autoincrement=False, nullable=False),
    sa.Column('activity_id', postgresql.UUID(), nullable=False),
    sa.Column('timeslot_id', postgresql.UUID(), nullable=False),
    sa.Column('booked_by', postgresql.UUID(), nullable=True),
    sa.Column('booked_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.activity_id'], ),
    sa.ForeignKeyConstraint(['booked_by'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['timeslot_id'], ['timeslots.timeslot_id'], ),
    sa.PrimaryKeyConstraint('vacancy_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vacancies')
    op.drop_table('timeslots')
    op.drop_table('venues_images')
    op.drop_table('babies')
    op.drop_table('activities')
    op.drop_table('venues')
    op.drop_table('sessions')
    op.drop_table('providers')
    op.drop_table('images')
    op.drop_table('wechat_users')
    op.drop_table('users')
    # ### end Alembic commands ###
