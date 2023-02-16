"""empty message

Revision ID: ca4c2f22c9d6
Revises: 1a902b6b779a
Create Date: 2023-02-06 22:30:06.412957

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ca4c2f22c9d6'
down_revision = '1a902b6b779a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dealer_product_list', 'scent_type')
    op.drop_column('dealer_product_list', 'specification_of_piece')
    op.drop_column('dealer_product_list', 'specifications')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dealer_product_list', sa.Column('specifications', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False, comment='规格（ML）'))
    op.add_column('dealer_product_list', sa.Column('specification_of_piece', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False, comment='每件规格（瓶）'))
    op.add_column('dealer_product_list', sa.Column('scent_type', mysql.VARCHAR(length=36), nullable=False, comment='香型'))
    # ### end Alembic commands ###