"""add cert.organisation_id column

Revision ID: 54866119e2ef
Revises: 501b23affc81
Create Date: 2018-11-02 17:34:48.332303

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '54866119e2ef'
down_revision = '501b23affc81'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('BirthCertificate', sa.Column('organisation_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'BirthCertificate', 'Organisation', ['organisation_id'], ['id'])
    op.add_column('DeathCertificate', sa.Column('organisation_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'DeathCertificate', 'Organisation', ['organisation_id'], ['id'])
    op.add_column('PerinatalDeathCertificate', sa.Column('organisation_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'PerinatalDeathCertificate', 'Organisation', ['organisation_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'PerinatalDeathCertificate', type_='foreignkey')
    op.drop_column('PerinatalDeathCertificate', 'organisation_id')
    op.drop_constraint(None, 'DeathCertificate', type_='foreignkey')
    op.drop_column('DeathCertificate', 'organisation_id')
    op.drop_constraint(None, 'BirthCertificate', type_='foreignkey')
    op.drop_column('BirthCertificate', 'organisation_id')
    # ### end Alembic commands ###