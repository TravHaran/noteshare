"""empty message

Revision ID: c863c32a7f63
Revises: 6f51ba30e015
Create Date: 2022-08-21 10:32:28.971195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c863c32a7f63'
down_revision = '6f51ba30e015'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('library_id', sa.Integer(), nullable=False),
    sa.Column('file', sa.String(), nullable=False),
    sa.Column('thumbnail', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['library_id'], ['libraries.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, 'book_tag_map', 'books', ['book_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'book_votes', 'books', ['book_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'comments', 'books', ['book_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_constraint(None, 'book_votes', type_='foreignkey')
    op.drop_constraint(None, 'book_tag_map', type_='foreignkey')
    op.drop_table('books')
    # ### end Alembic commands ###