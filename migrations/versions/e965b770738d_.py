"""empty message

Revision ID: e965b770738d
Revises: 708b579f5577
Create Date: 2024-05-17 14:26:35.247627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e965b770738d'
down_revision = '708b579f5577'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('favoritosPlaneta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('planeta_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['planeta_id'], ['planetas.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('Users')
    op.drop_table('favoritos')
    with op.batch_alter_table('favoritosPersonaje', schema=None) as batch_op:
        batch_op.drop_constraint('favoritosPersonaje_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])

    with op.batch_alter_table('favoritosVehiculo', schema=None) as batch_op:
        batch_op.drop_constraint('favoritosVehiculo_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favoritosVehiculo', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('favoritosVehiculo_user_id_fkey', 'Users', ['user_id'], ['id'])

    with op.batch_alter_table('favoritosPersonaje', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('favoritosPersonaje_user_id_fkey', 'Users', ['user_id'], ['id'])

    op.create_table('favoritos',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('planeta_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['planeta_id'], ['planetas.id'], name='favoritos_planeta_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], name='favoritos_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='favoritos_pkey')
    )
    op.create_table('Users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Users_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='Users_pkey'),
    sa.UniqueConstraint('email', name='Users_email_key')
    )
    op.drop_table('favoritosPlaneta')
    op.drop_table('users')
    # ### end Alembic commands ###