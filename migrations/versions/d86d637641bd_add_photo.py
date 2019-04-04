"""Add photo

Revision ID: d86d637641bd
Revises: a9ed14bd1e72
Create Date: 2019-04-04 14:06:23.110629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd86d637641bd'
down_revision = 'a9ed14bd1e72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('unbabelite', sa.Column('photo', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('unbabelite', 'photo')
    # ### end Alembic commands ###
