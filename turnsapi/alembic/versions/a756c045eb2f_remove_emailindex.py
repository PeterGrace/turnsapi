"""remove emailindex

Revision ID: a756c045eb2f
Revises: 74e10ca62253
Create Date: 2017-06-16 18:42:39.867337

"""

# revision identifiers, used by Alembic.
revision = 'a756c045eb2f'
down_revision = '74e10ca62253'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('EmailIndex', table_name='oauth_creds')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('EmailIndex', 'oauth_creds', ['email'], unique=1)
    # ### end Alembic commands ###
