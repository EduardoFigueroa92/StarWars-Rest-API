"""empty message

Revision ID: 708b579f5577
Revises: 69b7a782dcb7
Create Date: 2024-05-16 13:08:08.909537

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '708b579f5577'
down_revision = '69b7a782dcb7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vehiculos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('model', sa.String(length=200), nullable=True),
    sa.Column('manufacturer', sa.String(length=200), nullable=True),
    sa.Column('cost_in_credits', sa.String(length=200), nullable=True),
    sa.Column('length', sa.Float(), nullable=True),
    sa.Column('crew', sa.Integer(), nullable=True),
    sa.Column('passengers', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favoritosVehiculo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('vehiculos_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.ForeignKeyConstraint(['vehiculos_id'], ['vehiculos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('naves')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('naves',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('model', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('manufacturer', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('cost_in_credits', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('length', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('crew', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('passengers', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='naves_pkey')
    )
    op.drop_table('favoritosVehiculo')
    op.drop_table('vehiculos')
    # ### end Alembic commands ###
