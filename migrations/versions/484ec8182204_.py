"""empty message

Revision ID: 484ec8182204
Revises: 053e4bb8fd81
Create Date: 2024-04-01 22:23:05.799634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '484ec8182204'
down_revision = '053e4bb8fd81'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dataset',
    sa.Column('id_d', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(length=250), nullable=False),
    sa.Column('file_hash', sa.String(length=250), nullable=False),
    sa.Column('created_at', sa.String(length=250), nullable=False),
    sa.Column('updated_at', sa.String(length=250), nullable=False),
    sa.Column('id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id_d')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dataset')
    # ### end Alembic commands ###