"""empty message

Revision ID: b569af001a26
Revises: 5a5c60c8c157
Create Date: 2022-12-30 13:19:50.843944

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b569af001a26'
down_revision = '5a5c60c8c157'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('outbound_order',
    sa.Column('id', sa.String(length=36), nullable=False, comment='哈希自动生成id'),
    sa.Column('title', sa.String(length=150), nullable=False, comment='出库单标题，例如出库安仁经销商的货'),
    sa.Column('total_price', mysql.FLOAT(precision=10, scale=2), nullable=False, comment='本次出库金额总计（元）'),
    sa.Column('total_piece', sa.Integer(), nullable=False, comment='本次出库数量总计（件）'),
    sa.Column('remarks', sa.Text(), nullable=True, comment='备注'),
    sa.Column('is_delete', sa.Integer(), nullable=False, comment='逻辑删除，查询的时候按照 filter is_delete != 0 来过滤已经逻辑删除的数据'),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False, comment='创建时间，修改数据不会自动更改'),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False, comment='更新时间'),
    sa.Column('business_id', sa.String(length=36), nullable=False, comment='业务id（使用雪花算法生成唯一id）'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('business_id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('outbound_order_list',
    sa.Column('id', sa.String(length=36), nullable=False, comment='哈希自动生成id'),
    sa.Column('purchase_order_id', sa.String(length=150), nullable=False, comment='出库单表（outbound_order）的business id，与之关联'),
    sa.Column('product_name', sa.String(length=36), nullable=False, comment='产品名称'),
    sa.Column('specifications', sa.Integer(), nullable=False, comment='规格（ML）'),
    sa.Column('scent_type', sa.String(length=36), nullable=False, comment='香型'),
    sa.Column('quantity', sa.Integer(), nullable=False, comment='数量（件）'),
    sa.Column('specification_of_piece', sa.Integer(), nullable=False, comment='每件规格（瓶）'),
    sa.Column('unit_price', mysql.FLOAT(precision=10, scale=2), nullable=False, comment='单价（元/瓶）'),
    sa.Column('subtotal_price', mysql.FLOAT(precision=10, scale=2), nullable=False, comment='小计（元）'),
    sa.Column('is_delete', sa.Integer(), nullable=False, comment='逻辑删除，查询的时候按照 filter is_delete != 0 来过滤已经逻辑删除的数据'),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False, comment='创建时间，修改数据不会自动更改'),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False, comment='更新时间'),
    sa.Column('business_id', sa.String(length=36), nullable=False, comment='业务id（使用雪花算法生成唯一id）'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('business_id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('outbound_order_list')
    op.drop_table('outbound_order')
    # ### end Alembic commands ###