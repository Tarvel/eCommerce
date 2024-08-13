"""first migration

Revision ID: a556eddea46a
Revises: 
Create Date: 2024-08-13 21:10:41.798190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a556eddea46a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('user_img', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('user_description', sa.String(), nullable=True),
    sa.Column('user_address', sa.String(), nullable=True),
    sa.Column('user_state', sa.String(), nullable=True),
    sa.Column('user_country', sa.String(), nullable=True),
    sa.Column('user_gender', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('password'),
    sa.UniqueConstraint('username')
    )
    op.create_table('cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cart', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('notification', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(), nullable=False),
    sa.Column('product_description', sa.String(), nullable=False),
    sa.Column('product_img1', sa.String(), nullable=False),
    sa.Column('product_img2', sa.String(), nullable=True),
    sa.Column('product_img3', sa.String(), nullable=True),
    sa.Column('product_img4', sa.String(), nullable=True),
    sa.Column('product_img5', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wishlist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('wishlist', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wishlist')
    op.drop_table('products')
    op.drop_table('notification')
    op.drop_table('cart')
    op.drop_table('user')
    # ### end Alembic commands ###