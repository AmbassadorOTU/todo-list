"""empty message

Revision ID: 00432253d9d9
Revises: 70fcbe250cf9
Create Date: 2022-06-02 22:11:28.226524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00432253d9d9'
down_revision = '70fcbe250cf9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todo')
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))

    op.execute('UPDATE todos SET completed = False WHERE completed IS NULL;')

    op.alter_column('todos', 'completed', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'completed')
    op.create_table('todo',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('completed', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='todo_pkey')
    )
    # ### end Alembic commands ###
