"""empty message

Revision ID: 56bd475e5d65
Revises: a87c3dae09e6
Create Date: 2022-04-24 18:28:07.830718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56bd475e5d65'
down_revision = 'a87c3dae09e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('weekly_report', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avg_nop', sa.Float(), nullable=True))
        batch_op.drop_column('total')
        batch_op.drop_column('average')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('weekly_report', schema=None) as batch_op:
        batch_op.add_column(sa.Column('average', sa.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('total', sa.INTEGER(), nullable=True))
        batch_op.drop_column('avg_nop')

    # ### end Alembic commands ###
