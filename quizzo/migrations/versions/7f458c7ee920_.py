"""empty message

Revision ID: 7f458c7ee920
Revises: 
Create Date: 2021-04-16 13:39:05.291599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f458c7ee920'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('qid', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(), nullable=False),
    sa.Column('option1', sa.String(), nullable=True),
    sa.Column('option2', sa.String(), nullable=True),
    sa.Column('option3', sa.String(), nullable=True),
    sa.Column('option4', sa.String(), nullable=True),
    sa.Column('answer', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('qid')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('roll', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_roll'), 'user', ['roll'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_roll'), table_name='user')
    op.drop_table('user')
    op.drop_table('question')
    # ### end Alembic commands ###