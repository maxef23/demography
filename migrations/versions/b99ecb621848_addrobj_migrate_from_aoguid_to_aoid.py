"""ADDROBJ: migrate from AOGUID to AOID

Revision ID: b99ecb621848
Revises: e4b8375cc8ac
Create Date: 2019-01-15 18:33:01.448807

"""
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b99ecb621848'
down_revision = 'e4b8375cc8ac'
branch_labels = None
depends_on = None

ADDRESS_FIELDS = {
    'BirthCertificate': ['motherRegistryRegion',
                         'motherRegistryArea',
                         'motherRegistryCity',
                         'motherRegistryStreet',
                         'childBirthRegion',
                         'childBirthArea',
                         'childBirthCity'],
    'DeathCertificate': ['registryRegion',
                         'registryArea',
                         'registryCity',
                         'registryStreet',
                         'deathRegion',
                         'deathArea',
                         'deathCity',
                         'deathStreet',
                         'childRegion',
                         'childArea',
                         'childCity'],
    'PerinatalDeathCertificate': ['motherRegistryRegion',
                                  'motherRegistryArea',
                                  'motherRegistryCity',
                                  'motherRegistryStreet',
                                  'childBirthRegion',
                                  'childBirthArea',
                                  'childBirthCity']
}


def upgrade_field(connection, table, field):
    connection.execute(f"""UPDATE `{table}` t
    INNER JOIN `fias`.`ADDROBJ` ao ON ao.AOGUID = t.`{field}`
    SET t.`{field}` = ao.AOID 
    WHERE t.`{field}` IS NOT NULL AND (ao.CURRSTATUS = 0 OR ao.LIVESTATUS = 1) """)


def downgrade_field(connection, table, field):
    connection.execute(f"""UPDATE `{table}` t
    INNER JOIN `fias`.`ADDROBJ` ao ON ao.AOID = t.`{field}`
    SET t.`{field}` = ao.AOGUID 
    WHERE t.`{field}` IS NOT NULL""")


def upgrade():
    connection = op.get_bind()
    for table, fields in ADDRESS_FIELDS.items():
        for field in fields:
            upgrade_field(connection, table, field)


def downgrade():
    connection = op.get_bind()
    for table, fields in ADDRESS_FIELDS.items():
        for field in fields:
            downgrade_field(connection, table, field)
