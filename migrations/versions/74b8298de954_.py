"""empty message

Revision ID: 74b8298de954
Revises: dd2fa4d4c470
Create Date: 2023-10-18 20:32:12.368413

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74b8298de954'
down_revision = 'dd2fa4d4c470'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.Column('description', sa.String(length=250), nullable=False),
    sa.Column('notes', sa.String(length=500), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('todos_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('todo_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['todo_id'], ['todo.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.drop_table('to_do')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('to_do',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('completed', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('notes', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('project_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], name='to_do_project_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='to_do_pkey'),
    sa.UniqueConstraint('id', name='to_do_id_key')
    )
    op.drop_table('todos_users')
    op.drop_table('todo')
    # ### end Alembic commands ###
