"""how could I forget food?

Revision ID: 6aaa818cedb3
Revises: None
Create Date: 2017-06-16 18:33:03.589475

"""

# revision identifiers, used by Alembic.
revision = '6aaa818cedb3'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game_data', sa.Column('food', sa.Integer(), nullable=False))
    op.create_index('EmailIndex', 'oauth_creds', ['email'], unique=True, mysql_length=255)
    op.drop_index('EmailIndex', table_name='oauth_creds')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('EmailIndex', 'oauth_creds', ['email'], unique=1)
    op.drop_index('EmailIndex', table_name='oauth_creds')
    op.drop_column('game_data', 'food')
    # ### end Alembic commands ###
