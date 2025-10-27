"""add parts and deliveries tables

Revision ID: c5432e87ab3f
Revises: b1324d93ee1d
Create Date: 2025-10-25 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'c5432e87ab3f'
down_revision = 'b1324d93ee1d'
branch_labels = None
depends_on = None


def upgrade():
    # Create part table
    op.create_table('part',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('stock', sa.Integer(), nullable=False),
        sa.Column('min_stock', sa.Integer(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )
    with op.batch_alter_table('part', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_part_code'), ['code'], unique=True)

    # Create part_delivery table
    op.create_table('part_delivery',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('part_id', sa.Integer(), nullable=False),
        sa.Column('mechanic_id', sa.Integer(), nullable=False),
        sa.Column('assignment_id', sa.Integer(), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('delivered_by', sa.Integer(), nullable=False),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['assignment_id'], ['assignment.id'], ),
        sa.ForeignKeyConstraint(['delivered_by'], ['user.id'], ),
        sa.ForeignKeyConstraint(['mechanic_id'], ['mechanic.id'], ),
        sa.ForeignKeyConstraint(['part_id'], ['part.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('part_delivery')
    with op.batch_alter_table('part', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_part_code'))
    op.drop_table('part')
