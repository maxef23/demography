"""split cert date fields to YMD

Revision ID: 940d253b4b0f
Revises: d6a09464934f
Create Date: 2018-10-16 15:52:10.647944

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '940d253b4b0f'
down_revision = 'd6a09464934f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('BirthCertificate', sa.Column('childDATOB_D', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('BirthCertificate', sa.Column('childDATOB_M', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('BirthCertificate', sa.Column('childDATOB_Y', mysql.SMALLINT(unsigned=True), nullable=True))
    op.add_column('BirthCertificate', sa.Column('deliveryDate_D', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('BirthCertificate', sa.Column('deliveryDate_M', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('BirthCertificate', sa.Column('deliveryDate_Y', mysql.SMALLINT(unsigned=True), nullable=True))
    op.add_column('BirthCertificate', sa.Column('motherDOB_D', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('BirthCertificate', sa.Column('motherDOB_M', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('BirthCertificate', sa.Column('motherDOB_Y', mysql.SMALLINT(unsigned=True), nullable=True))
    op.drop_column('BirthCertificate', 'motherDOB')
    op.drop_column('BirthCertificate', 'deliveryDate')
    op.drop_column('BirthCertificate', 'childDATOB')
    op.add_column('DeathCertificate', sa.Column('birthDate_D', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('DeathCertificate', sa.Column('birthDate_M', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('DeathCertificate', sa.Column('birthDate_Y', mysql.SMALLINT(unsigned=True), nullable=True))
    op.add_column('DeathCertificate', sa.Column('deathDate_D', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('DeathCertificate', sa.Column('deathDate_M', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('DeathCertificate', sa.Column('deathDate_Y', mysql.SMALLINT(unsigned=True), nullable=True))
    op.add_column('DeathCertificate', sa.Column('deliveryDate_D', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('DeathCertificate', sa.Column('deliveryDate_M', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('DeathCertificate', sa.Column('deliveryDate_Y', mysql.SMALLINT(unsigned=True), nullable=True))
    op.add_column('DeathCertificate', sa.Column('motherDOB_D', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('DeathCertificate', sa.Column('motherDOB_M', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('DeathCertificate', sa.Column('motherDOB_Y', mysql.SMALLINT(unsigned=True), nullable=True))
    op.drop_column('DeathCertificate', 'motherDOB')
    op.drop_column('DeathCertificate', 'deathDate')
    op.drop_column('DeathCertificate', 'deliveryDate')
    op.drop_column('DeathCertificate', 'birthDate')
    op.add_column('PerinatalDeathCertificate', sa.Column('birthDatetime_D', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('PerinatalDeathCertificate', sa.Column('birthDatetime_M', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('PerinatalDeathCertificate', sa.Column('birthDatetime_Y', mysql.SMALLINT(unsigned=True), nullable=True))
    op.add_column('PerinatalDeathCertificate', sa.Column('deathDate_D', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('PerinatalDeathCertificate', sa.Column('deathDate_M', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('PerinatalDeathCertificate', sa.Column('deathDate_Y', mysql.SMALLINT(unsigned=True), nullable=True))
    op.add_column('PerinatalDeathCertificate', sa.Column('deliveryDate_D', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('PerinatalDeathCertificate', sa.Column('deliveryDate_M', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('PerinatalDeathCertificate', sa.Column('deliveryDate_Y', mysql.SMALLINT(unsigned=True), nullable=True))
    op.add_column('PerinatalDeathCertificate', sa.Column('perinatalDeathDate_D', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('PerinatalDeathCertificate', sa.Column('perinatalDeathDate_M', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('PerinatalDeathCertificate', sa.Column('perinatalDeathDate_Y', mysql.SMALLINT(unsigned=True), nullable=True))
    op.add_column('PerinatalDeathCertificate', sa.Column('previousCertificateDeliveryDate_D', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('PerinatalDeathCertificate', sa.Column('previousCertificateDeliveryDate_M', mysql.TINYINT(unsigned=True), nullable=True))
    op.add_column('PerinatalDeathCertificate', sa.Column('previousCertificateDeliveryDate_Y', mysql.SMALLINT(unsigned=True), nullable=True))
    op.drop_column('PerinatalDeathCertificate', 'deliveryDate')
    op.drop_column('PerinatalDeathCertificate', 'perinatalDeathDate')
    op.drop_column('PerinatalDeathCertificate', 'deathDate')
    op.drop_column('PerinatalDeathCertificate', 'previousCertificateDeliveryDate')
    op.drop_column('PerinatalDeathCertificate', 'birthDatetime')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('PerinatalDeathCertificate', sa.Column('birthDatetime', sa.DATE(), nullable=True))
    op.add_column('PerinatalDeathCertificate', sa.Column('previousCertificateDeliveryDate', sa.DATE(), nullable=True))
    op.add_column('PerinatalDeathCertificate', sa.Column('deathDate', sa.DATE(), nullable=True))
    op.add_column('PerinatalDeathCertificate', sa.Column('perinatalDeathDate', sa.DATE(), nullable=True))
    op.add_column('PerinatalDeathCertificate', sa.Column('deliveryDate', sa.DATE(), nullable=True))
    op.drop_column('PerinatalDeathCertificate', 'previousCertificateDeliveryDate_Y')
    op.drop_column('PerinatalDeathCertificate', 'previousCertificateDeliveryDate_M')
    op.drop_column('PerinatalDeathCertificate', 'previousCertificateDeliveryDate_D')
    op.drop_column('PerinatalDeathCertificate', 'perinatalDeathDate_Y')
    op.drop_column('PerinatalDeathCertificate', 'perinatalDeathDate_M')
    op.drop_column('PerinatalDeathCertificate', 'perinatalDeathDate_D')
    op.drop_column('PerinatalDeathCertificate', 'deliveryDate_Y')
    op.drop_column('PerinatalDeathCertificate', 'deliveryDate_M')
    op.drop_column('PerinatalDeathCertificate', 'deliveryDate_D')
    op.drop_column('PerinatalDeathCertificate', 'deathDate_Y')
    op.drop_column('PerinatalDeathCertificate', 'deathDate_M')
    op.drop_column('PerinatalDeathCertificate', 'deathDate_D')
    op.drop_column('PerinatalDeathCertificate', 'birthDatetime_Y')
    op.drop_column('PerinatalDeathCertificate', 'birthDatetime_M')
    op.drop_column('PerinatalDeathCertificate', 'birthDatetime_D')
    op.add_column('DeathCertificate', sa.Column('birthDate', sa.DATE(), nullable=True))
    op.add_column('DeathCertificate', sa.Column('deliveryDate', sa.DATE(), nullable=True))
    op.add_column('DeathCertificate', sa.Column('deathDate', sa.DATE(), nullable=True))
    op.add_column('DeathCertificate', sa.Column('motherDOB', sa.DATE(), nullable=True))
    op.drop_column('DeathCertificate', 'motherDOB_Y')
    op.drop_column('DeathCertificate', 'motherDOB_M')
    op.drop_column('DeathCertificate', 'motherDOB_D')
    op.drop_column('DeathCertificate', 'deliveryDate_Y')
    op.drop_column('DeathCertificate', 'deliveryDate_M')
    op.drop_column('DeathCertificate', 'deliveryDate_D')
    op.drop_column('DeathCertificate', 'deathDate_Y')
    op.drop_column('DeathCertificate', 'deathDate_M')
    op.drop_column('DeathCertificate', 'deathDate_D')
    op.drop_column('DeathCertificate', 'birthDate_Y')
    op.drop_column('DeathCertificate', 'birthDate_M')
    op.drop_column('DeathCertificate', 'birthDate_D')
    op.add_column('BirthCertificate', sa.Column('childDATOB', sa.DATE(), nullable=True))
    op.add_column('BirthCertificate', sa.Column('deliveryDate', sa.DATE(), nullable=True))
    op.add_column('BirthCertificate', sa.Column('motherDOB', sa.DATE(), nullable=True))
    op.drop_column('BirthCertificate', 'motherDOB_Y')
    op.drop_column('BirthCertificate', 'motherDOB_M')
    op.drop_column('BirthCertificate', 'motherDOB_D')
    op.drop_column('BirthCertificate', 'deliveryDate_Y')
    op.drop_column('BirthCertificate', 'deliveryDate_M')
    op.drop_column('BirthCertificate', 'deliveryDate_D')
    op.drop_column('BirthCertificate', 'childDATOB_Y')
    op.drop_column('BirthCertificate', 'childDATOB_M')
    op.drop_column('BirthCertificate', 'childDATOB_D')
    # ### end Alembic commands ###
