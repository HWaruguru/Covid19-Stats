"""add post-comment relationship

Revision ID: 83622e4ccb05
Revises: 366a00361a76
Create Date: 2021-09-29 22:35:31.243837

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83622e4ccb05'
down_revision = '366a00361a76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('post', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'comments', 'covid', ['post'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_column('comments', 'post')
    # ### end Alembic commands ###