"""empty message

Revision ID: 855169ec12d4
Revises: d663b30f7538
Create Date: 2023-01-04 21:05:30.753988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '855169ec12d4'
down_revision = 'd663b30f7538'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth_api',
    sa.Column('id', sa.String(length=36), nullable=False, comment='哈希自动生成id'),
    sa.Column('api_name', sa.String(length=150), nullable=False, comment='api的字段名，例如：/user/get_group_data'),
    sa.Column('is_delete', sa.Integer(), nullable=False, comment='逻辑删除，查询的时候按照 filter is_delete != 0 来过滤已经逻辑删除的数据'),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False, comment='创建时间，修改数据不会自动更改'),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False, comment='更新时间'),
    sa.Column('business_id', sa.String(length=36), nullable=False, comment='业务id（使用雪花算法生成唯一id）'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('business_id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_auth_api_api_name'), 'auth_api', ['api_name'], unique=True)
    op.create_table('auth_group',
    sa.Column('id', sa.String(length=36), nullable=False, comment='哈希自动生成id'),
    sa.Column('group_name', sa.Integer(), nullable=False, comment='组名，普通用户组（默认）：0；用户管理组：1；数据管理组：2；超级管理员组：99'),
    sa.Column('is_delete', sa.Integer(), nullable=False, comment='逻辑删除，查询的时候按照 filter is_delete != 0 来过滤已经逻辑删除的数据'),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False, comment='创建时间，修改数据不会自动更改'),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False, comment='更新时间'),
    sa.Column('business_id', sa.String(length=36), nullable=False, comment='业务id（使用雪花算法生成唯一id）'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('business_id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_auth_group_group_name'), 'auth_group', ['group_name'], unique=True)
    op.create_table('auth_group_api_relation',
    sa.Column('id', sa.String(length=36), nullable=False, comment='哈希自动生成id'),
    sa.Column('group_id', sa.String(length=32), nullable=False, comment='权限组的 business_id'),
    sa.Column('auth_api_id', sa.String(length=32), nullable=False, comment='api表的 business_id'),
    sa.Column('is_delete', sa.Integer(), nullable=False, comment='逻辑删除，查询的时候按照 filter is_delete != 0 来过滤已经逻辑删除的数据'),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False, comment='创建时间，修改数据不会自动更改'),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False, comment='更新时间'),
    sa.Column('business_id', sa.String(length=36), nullable=False, comment='业务id（使用雪花算法生成唯一id）'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('business_id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('auth_user',
    sa.Column('id', sa.String(length=36), nullable=False, comment='哈希自动生成id'),
    sa.Column('username', sa.String(length=150), nullable=False, comment='用户名'),
    sa.Column('password', sa.String(length=128), nullable=False, comment='密码'),
    sa.Column('register_ip', sa.String(length=32), nullable=True, comment='注册ip'),
    sa.Column('register_time', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False, comment='注册时间'),
    sa.Column('status', sa.Integer(), nullable=True, comment='状态，是否可用'),
    sa.Column('group_id', sa.String(length=32), nullable=False, comment='auth_group表的id，外键id'),
    sa.Column('is_delete', sa.Integer(), nullable=False, comment='逻辑删除，查询的时候按照 filter is_delete != 0 来过滤已经逻辑删除的数据'),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False, comment='创建时间，修改数据不会自动更改'),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False, comment='更新时间'),
    sa.Column('business_id', sa.String(length=36), nullable=False, comment='业务id（使用雪花算法生成唯一id）'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('business_id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_auth_user_username'), 'auth_user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_auth_user_username'), table_name='auth_user')
    op.drop_table('auth_user')
    op.drop_table('auth_group_api_relation')
    op.drop_index(op.f('ix_auth_group_group_name'), table_name='auth_group')
    op.drop_table('auth_group')
    op.drop_index(op.f('ix_auth_api_api_name'), table_name='auth_api')
    op.drop_table('auth_api')
    # ### end Alembic commands ###
