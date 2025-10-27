"""add part request table

Revision ID: d8765f43bc2a
Revises: c5432e87ab3f
Create Date: 2025-10-25 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8765f43bc2a'
down_revision = 'c5432e87ab3f'
branch_labels = None
depends_on = None


def upgrade():
    # Create part_request table
    op.create_table('part_request',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('part_id', sa.Integer(), nullable=False),
        sa.Column('mechanic_id', sa.Integer(), nullable=False),
        sa.Column('assignment_id', sa.Integer(), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('requested_by', sa.Integer(), nullable=False),
        sa.Column('requested_at', sa.DateTime(), nullable=True),
        sa.Column('processed_by', sa.Integer(), nullable=True),
        sa.Column('processed_at', sa.DateTime(), nullable=True),
        sa.Column('response_note', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['assignment_id'], ['assignment.id'], ),
        sa.ForeignKeyConstraint(['mechanic_id'], ['mechanic.id'], ),
        sa.ForeignKeyConstraint(['part_id'], ['part.id'], ),
        sa.ForeignKeyConstraint(['processed_by'], ['user.id'], ),
        sa.ForeignKeyConstraint(['requested_by'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('part_request')
