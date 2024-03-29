"""add Counter

Revision ID: db240d12433d
Revises: c818531eabec
Create Date: 2018-11-14 16:28:51.303566

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'db240d12433d'
down_revision = 'c818531eabec'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    op.create_table('Counter',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('updateDatetime', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('updateUserId', sa.Integer(), nullable=True),
                    sa.Column('code', sa.String(length=16), nullable=False),
                    sa.Column('name', sa.String(length=64), nullable=False),
                    sa.Column('year', sa.Integer(), nullable=False),
                    sa.Column('number', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['updateUserId'], ['User.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('code'),
                    sa.UniqueConstraint('name'),
                    mysql_engine='InnoDB')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.get_bind().execute('DROP FUNCTION IF EXISTS `getCounterValue`;')
    op.drop_table('Counter')
    # ### end Alembic commands ###
