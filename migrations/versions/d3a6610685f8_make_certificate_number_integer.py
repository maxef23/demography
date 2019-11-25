"""make certificate.number integer

Revision ID: d3a6610685f8
Revises: db240d12433d
Create Date: 2018-11-20 14:50:00.614480

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd3a6610685f8'
down_revision = 'db240d12433d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('BirthCertificate', 'number',
               existing_type=mysql.VARCHAR(length=16),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('DeathCertificate', 'number',
               existing_type=mysql.VARCHAR(length=16),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('PerinatalDeathCertificate', 'number',
               existing_type=mysql.VARCHAR(length=16),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('PerinatalDeathCertificate', 'updateDatetime',
               existing_type=mysql.DATETIME(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
    op.alter_column('rbUserPreferences', 'width',
               existing_type=mysql.FLOAT(),
               type_=sa.Float(precision=10, asdecimal=2),
               existing_nullable=True)
    op.create_foreign_key(None, 'rbUserPreferences', 'User', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'rbUserPreferences', type_='foreignkey')
    op.alter_column('rbUserPreferences', 'width',
               existing_type=sa.Float(precision=10, asdecimal=2),
               type_=mysql.FLOAT(),
               existing_nullable=True)
    op.alter_column('PerinatalDeathCertificate', 'updateDatetime',
               existing_type=sa.DateTime(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('PerinatalDeathCertificate', 'number',
               existing_type=sa.Integer(),
               type_=mysql.VARCHAR(length=16),
               existing_nullable=True)
    op.alter_column('PerinatalDeathCertificate', 'createDatetime',
               existing_type=sa.DateTime(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('PerinatalDeathCertificate', 'closedDatetime',
               existing_type=sa.DateTime(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('Logger', 'datetime',
               existing_type=sa.DateTime(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('Logger', 'data',
               existing_type=sa.Text(length=5000),
               type_=mysql.TEXT(),
               existing_nullable=True)
    op.alter_column('DeathCertificate', 'updateDatetime',
               existing_type=sa.DateTime(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('DeathCertificate', 'number',
               existing_type=sa.Integer(),
               type_=mysql.VARCHAR(length=16),
               existing_nullable=True)
    op.alter_column('DeathCertificate', 'createDatetime',
               existing_type=sa.DateTime(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('DeathCertificate', 'closedDatetime',
               existing_type=sa.DateTime(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('Counter', 'updateDatetime',
               existing_type=sa.DateTime(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('BirthCertificate', 'updateDatetime',
               existing_type=sa.DateTime(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('BirthCertificate', 'number',
               existing_type=sa.Integer(),
               type_=mysql.VARCHAR(length=16),
               existing_nullable=True)
    op.alter_column('BirthCertificate', 'createDatetime',
               existing_type=sa.DateTime(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('BirthCertificate', 'closedDatetime',
               existing_type=sa.DateTime(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.create_table('User_Import',
    sa.Column('code', mysql.VARCHAR(length=16), server_default=sa.text("''"), nullable=True),
    sa.Column('SNILS', mysql.VARCHAR(length=16), server_default=sa.text("''"), nullable=True),
    sa.Column('fullName', mysql.VARCHAR(length=256), server_default=sa.text("''"), nullable=True),
    sa.Column('orgCode', mysql.VARCHAR(length=16), server_default=sa.text("''"), nullable=True),
    sa.Column('orgFullName', mysql.VARCHAR(length=256), server_default=sa.text("''"), nullable=True),
    sa.Column('orgShortName', mysql.VARCHAR(length=64), server_default=sa.text("''"), nullable=True),
    sa.Column('orgAddress', mysql.VARCHAR(length=128), server_default=sa.text("''"), nullable=True),
    sa.Column('orgOKPO', mysql.VARCHAR(length=16), server_default=sa.text("''"), nullable=True),
    sa.Column('postName', mysql.VARCHAR(length=256), server_default=sa.text("''"), nullable=True),
    sa.Column('postCode', mysql.VARCHAR(length=16), server_default=sa.text("''"), nullable=True),
    sa.Column('login', mysql.VARCHAR(length=32), server_default=sa.text("''"), nullable=True),
    sa.Column('password', mysql.VARCHAR(length=64), server_default=sa.text("''"), nullable=True),
    sa.Column('familyName', mysql.VARCHAR(length=128), server_default=sa.text("''"), nullable=True),
    sa.Column('firstName', mysql.VARCHAR(length=128), server_default=sa.text("''"), nullable=True),
    sa.Column('middleName', mysql.VARCHAR(length=128), server_default=sa.text("''"), nullable=True),
    sa.Column('postId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('orgId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    mysql_comment='?????? ??????',
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
