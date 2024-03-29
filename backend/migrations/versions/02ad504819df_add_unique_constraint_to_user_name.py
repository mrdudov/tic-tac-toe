"""add unique constraint to user name

Revision ID: 02ad504819df
Revises: 813e3496ebf6
Create Date: 2023-03-17 09:58:58.418270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02ad504819df'
down_revision = '813e3496ebf6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_id', table_name='user')
    op.drop_index('ix_user_name', table_name='user')
    op.create_unique_constraint(None, 'user', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.create_index('ix_user_name', 'user', ['name'], unique=False)
    op.create_index('ix_user_id', 'user', ['id'], unique=False)
    # ### end Alembic commands ###
