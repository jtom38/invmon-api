"""01-init

Revision ID: 814c9cfe9e0e
Revises: 
Create Date: 2021-11-06 17:44:12.463208

"""

from alembic.op import create_table, drop_column, add_column, drop_table
from sqlalchemy import Column, String, Integer, Boolean


# revision identifiers, used by Alembic.
revision = '814c9cfe9e0e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
