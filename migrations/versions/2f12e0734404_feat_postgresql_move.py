"""feat:postgresql-move

Revision ID: 2f12e0734404
Revises: 
Create Date: 2024-07-05 14:06:20.533234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f12e0734404'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_file', sa.String(length=20), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=250), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('phone_number', sa.String(length=20), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_admin_username'), ['username'], unique=True)

    op.create_table('dataset',
    sa.Column('id_d', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(length=250), nullable=False),
    sa.Column('file_hash', sa.String(length=250), nullable=False),
    sa.Column('prediction', sa.String(length=250), nullable=False),
    sa.Column('created_at', sa.String(length=250), nullable=False),
    sa.Column('updated_at', sa.String(length=250), nullable=False),
    sa.Column('id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id_d')
    )
    op.create_table('manualdata',
    sa.Column('id_m', sa.Integer(), nullable=False),
    sa.Column('area', sa.String(length=250), nullable=True),
    sa.Column('hum', sa.Float(), nullable=False),
    sa.Column('soil_nitro1', sa.Float(), nullable=False),
    sa.Column('soil_phos1', sa.Float(), nullable=False),
    sa.Column('soil_pot1', sa.Float(), nullable=False),
    sa.Column('soil_temp1', sa.Float(), nullable=False),
    sa.Column('soil_ph1', sa.Float(), nullable=False),
    sa.Column('temp', sa.Float(), nullable=False),
    sa.Column('prediction', sa.String(length=250), nullable=True),
    sa.Column('created_at', sa.String(length=250), nullable=False),
    sa.Column('updated_at', sa.String(length=250), nullable=False),
    sa.Column('id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id_m')
    )
    op.create_table('area',
    sa.Column('id_area', sa.Integer(), nullable=False),
    sa.Column('area_name', sa.String(length=250), nullable=False),
    sa.Column('area_longitude', sa.Float(), nullable=True),
    sa.Column('area_latitude', sa.Float(), nullable=True),
    sa.Column('created_at', sa.String(length=250), nullable=False),
    sa.Column('updated_at', sa.String(length=250), nullable=False),
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('id_d', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['manualdata.id_m'], ),
    sa.ForeignKeyConstraint(['id'], ['manualdata.id_m'], name='fk_area_manualdata'),
    sa.ForeignKeyConstraint(['id_d'], ['dataset.id_d'], ),
    sa.ForeignKeyConstraint(['id_d'], ['dataset.id_d'], name='fk_area_dataset'),
    sa.PrimaryKeyConstraint('id_area')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('area')
    op.drop_table('manualdata')
    op.drop_table('dataset')
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_admin_username'))

    op.drop_table('admin')
    # ### end Alembic commands ###
