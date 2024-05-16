"""empty message

Revision ID: 69b7a782dcb7
Revises: 07d512a33ada
Create Date: 2024-05-16 09:26:28.374314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69b7a782dcb7'
down_revision = '07d512a33ada'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favoritosPersonaje',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('personajes_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['personajes_id'], ['personajes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favoritosPersonaje')
    # ### end Alembic commands ###
