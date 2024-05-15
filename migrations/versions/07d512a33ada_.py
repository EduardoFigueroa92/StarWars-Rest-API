"""empty message

Revision ID: 07d512a33ada
Revises: 10b3077dc5ed
Create Date: 2024-05-15 14:43:23.954773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07d512a33ada'
down_revision = '10b3077dc5ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favoritos', schema=None) as batch_op:
        batch_op.drop_constraint('favoritos_nave_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('favoritos_personaje_id_fkey', type_='foreignkey')
        batch_op.drop_column('nave_id')
        batch_op.drop_column('personaje_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favoritos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('personaje_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('nave_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('favoritos_personaje_id_fkey', 'personajes', ['personaje_id'], ['id'])
        batch_op.create_foreign_key('favoritos_nave_id_fkey', 'naves', ['nave_id'], ['id'])

    # ### end Alembic commands ###
