"""add soil_pot1, soil_temp1, soil_ph1

Revision ID: 053e4bb8fd81
Revises: cddc507dbd2b
Create Date: 2024-03-16 15:10:39.605895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '053e4bb8fd81'
down_revision = 'cddc507dbd2b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('manualdata', schema=None) as batch_op:
        batch_op.add_column(sa.Column('soil_temp1', sa.Float(), nullable=False))
        batch_op.add_column(sa.Column('soil_ph1', sa.Float(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('manualdata', schema=None) as batch_op:
        batch_op.drop_column('soil_ph1')
        batch_op.drop_column('soil_temp1')

    # ### end Alembic commands ###