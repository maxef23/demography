"""update CounterModel

Revision ID: 2171260c3159
Revises: 20d8540d3669
Create Date: 2018-12-04 14:10:37.042466

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2171260c3159'
down_revision = '20d8540d3669'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_code_year', 'Counter', ['code', 'year'], unique=True)
    op.drop_index('code', table_name='Counter')
    op.drop_index('name', table_name='Counter')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('name', 'Counter', ['name'], unique=True)
    op.create_index('code', 'Counter', ['code'], unique=True)
    op.drop_index('ix_code_year', table_name='Counter')
    # ### end Alembic commands ###