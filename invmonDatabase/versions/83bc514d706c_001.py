"""0.0.1 migration

Revision ID: 83bc514d706c
Revises: 814c9cfe9e0e
Create Date: 2021-11-11 05:50:49.152695

"""
from alembic.op import create_table, drop_column, add_column, drop_table
from sqlalchemy import Column, String, Integer, Boolean


# revision identifiers, used by Alembic.
revision = '83bc514d706c'
down_revision = '814c9cfe9e0e'
branch_labels = None
depends_on = None


def upgrade():
    # Defines who will be alerted
    create_table(
        'smtpContacts'
        ,Column('id', String, primary_key=True)
        ,Column('address', String) 
    )

    # Defines who wants to be alerted for what item
    create_table(
        'emailalerts'
        ,Column('id', String, primary_key=True)
        ,Column('smtpContactsId', String)
        ,Column('inventoryId', String)
    )

    # Defines alerts that need to be sent out
    create_table(
        'activealerts'
        ,Column('id', String, primary_key=True)
        ,Column('smtpContactId', String)
        ,Column('inventoryId', String)
    )

    # Defines items that will be monitored
    create_table(
        'inventory'
        ,Column("id", String, primary_key=True)
        ,Column("enabled", Boolean)
        ,Column('itemName', String)
        ,Column('lastStatus', String)
        ,Column('url', String)
    )


def downgrade():
    drop_table('smtpContacts')
    drop_table('emailalerts')
    drop_table('activealerts')
    drop_table('inventory')
    pass
