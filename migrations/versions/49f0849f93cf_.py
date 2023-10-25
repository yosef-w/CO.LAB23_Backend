"""empty message

Revision ID: 49f0849f93cf
Revises: 2bd33899694c
Create Date: 2023-10-23 22:38:56.504891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49f0849f93cf'
down_revision = '2bd33899694c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('links',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=250), nullable=False),
    sa.Column('link', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('meetings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=250), nullable=False),
    sa.Column('date', sa.String(length=100), nullable=True),
    sa.Column('notes', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])
        batch_op.create_foreign_key('fk_projects_user', 'user', ['admin_id'], ['id'], use_alter=True)

    with op.batch_alter_table('resources', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_user_projects', 'projects', ['current_project_id'], ['id'], use_alter=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('fk_user_projects', type_='foreignkey')

    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('resources', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.drop_constraint('fk_projects_user', type_='foreignkey')
        batch_op.drop_constraint(None, type_='unique')

    op.drop_table('meetings')
    op.drop_table('links')
    # ### end Alembic commands ###