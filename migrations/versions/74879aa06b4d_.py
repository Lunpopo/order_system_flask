"""empty message

Revision ID: 74879aa06b4d
Revises: 0dc51c8c0e6f
Create Date: 2023-03-01 15:19:34.538640

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '74879aa06b4d'
down_revision = '0dc51c8c0e6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('business_id', table_name='auth_group_api_relation')
    op.drop_index('id', table_name='auth_group_api_relation')
    op.drop_table('auth_group_api_relation')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth_group_api_relation',
    sa.Column('id', mysql.VARCHAR(length=36), nullable=False, comment='哈希自动生成id'),
    sa.Column('group_id', mysql.VARCHAR(length=32), nullable=False, comment='权限组的 business_id'),
    sa.Column('auth_api_id', mysql.VARCHAR(length=32), nullable=False, comment='api表的 business_id'),
    sa.Column('is_delete', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False, comment='逻辑删除，查询的时候按照 filter is_delete != 0 来过滤已经逻辑删除的数据'),
    sa.Column('create_time', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='创建时间，修改数据不会自动更改'),
    sa.Column('update_time', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False, comment='更新时间'),
    sa.Column('business_id', mysql.VARCHAR(length=36), nullable=False, comment='业务id（使用雪花算法生成唯一id）'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('id', 'auth_group_api_relation', ['id'], unique=False)
    op.create_index('business_id', 'auth_group_api_relation', ['business_id'], unique=False)
    # ### end Alembic commands ###