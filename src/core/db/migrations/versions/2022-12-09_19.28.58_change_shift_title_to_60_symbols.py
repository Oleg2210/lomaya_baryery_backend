"""Change shift_title to 60 symbols

Revision ID: 691cdea87322
Revises: a418e2ead89b
Create Date: 2022-12-09 19:28:58.525398

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '691cdea87322'
down_revision = 'a418e2ead89b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("UPDATE shifts SET title = SUBSTRING ( title ,0 , 60 )  ")
    op.alter_column('shifts', 'title',
               existing_type=sa.String(length=100),
               type_=sa.String(length=60),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('shifts', 'title',
               existing_type=sa.String(length=60),
               type_=sa.String(length=100),
               existing_nullable=False)
    # ### end Alembic commands ###
