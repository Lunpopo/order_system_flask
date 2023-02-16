"""empty message

Revision ID: 3202e6febaa1
Revises: c2dfedd94fd7
Create Date: 2023-02-05 16:59:55.567852

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3202e6febaa1'
down_revision = 'c2dfedd94fd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_list', sa.Column('scanning_price', mysql.FLOAT(precision=11, scale=2), nullable=False, comment='扫码价（元/瓶）'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product_list', 'scanning_price')
    # ### end Alembic commands ###