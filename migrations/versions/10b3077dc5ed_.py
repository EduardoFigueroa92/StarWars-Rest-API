"""empty message

Revision ID: 10b3077dc5ed
Revises: 
Create Date: 2024-05-15 14:16:23.937359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10b3077dc5ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('naves',
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
    op.create_table('personajes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('mass', sa.Integer(), nullable=True),
    sa.Column('hair_color', sa.String(length=200), nullable=True),
    sa.Column('skin_color', sa.String(length=200), nullable=True),
    sa.Column('eye_color', sa.String(length=200), nullable=True),
    sa.Column('birth_year', sa.String(length=200), nullable=True),
    sa.Column('gender', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planetas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('diameter', sa.Integer(), nullable=True),
    sa.Column('rotation_period', sa.Integer(), nullable=True),
    sa.Column('population', sa.String(length=200), nullable=True),
    sa.Column('climate', sa.String(length=200), nullable=True),
    sa.Column('terrain', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favoritos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('planeta_id', sa.Integer(), nullable=True),
    sa.Column('personaje_id', sa.Integer(), nullable=True),
    sa.Column('nave_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['nave_id'], ['naves.id'], ),
    sa.ForeignKeyConstraint(['personaje_id'], ['personajes.id'], ),
    sa.ForeignKeyConstraint(['planeta_id'], ['planetas.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favoritos')
    op.drop_table('planetas')
    op.drop_table('personajes')
    op.drop_table('naves')
    op.drop_table('Users')
    # ### end Alembic commands ###