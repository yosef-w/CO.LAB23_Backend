"""empty message

Revision ID: 252e53bafdc1
Revises: cbaa4fae7405
Create Date: 2023-10-24 20:29:45.177934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '252e53bafdc1'
down_revision = 'cbaa4fae7405'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inspiration', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inspiration', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
