"""add profile img field

Revision ID: cf450a59f9cf
Revises: 90935222af8f
Create Date: 2023-05-22 09:05:01.100535

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision = "cf450a59f9cf"
down_revision = "90935222af8f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user",
        sa.Column("profile_img", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "profile_img")
    # ### end Alembic commands ###
