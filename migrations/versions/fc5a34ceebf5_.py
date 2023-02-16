"""empty message

Revision ID: fc5a34ceebf5
Revises: e29ab9faaaef
Create Date: 2022-12-30 13:46:16.987180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc5a34ceebf5'
down_revision = 'e29ab9faaaef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('outbound_order_list', sa.Column('img_url', sa.String(length=300), nullable=True, comment='图片路径'))
    op.add_column('outbound_order_list', sa.Column('thumb_img_url', sa.String(length=300), nullable=True, comment='缩略图路径'))
    op.add_column('purchase_order_list', sa.Column('img_url', sa.String(length=300), nullable=True, comment='图片路径'))
    op.add_column('purchase_order_list', sa.Column('thumb_img_url', sa.String(length=300), nullable=True, comment='缩略图路径'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('purchase_order_list', 'thumb_img_url')
    op.drop_column('purchase_order_list', 'img_url')
    op.drop_column('outbound_order_list', 'thumb_img_url')
    op.drop_column('outbound_order_list', 'img_url')
    # ### end Alembic commands ###
