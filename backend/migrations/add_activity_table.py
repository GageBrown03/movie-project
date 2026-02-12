# backend/migrations/add_activity_table.py
"""
Migration: Add activities table
Run with: flask db upgrade
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers
revision = 'add_activity_table'
down_revision = None  # Update this to your latest migration ID
branch_labels = None
depends_on = None


def upgrade():
    """Create activities table"""
    op.create_table(
        'activities',
        sa.Column('activity_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('activity_type', sa.String(length=50), nullable=False),
        sa.Column('media_id', sa.Integer(), nullable=True),
        sa.Column('friend_user_id', sa.Integer(), nullable=True),
        sa.Column('data', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['media_id'], ['media.media_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['friend_user_id'], ['users.user_id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('activity_id')
    )
    
    # Create indexes for common queries
    op.create_index('idx_activities_user_id', 'activities', ['user_id'])
    op.create_index('idx_activities_created_at', 'activities', ['created_at'])
    op.create_index('idx_activities_type', 'activities', ['activity_type'])


def downgrade():
    """Drop activities table"""
    op.drop_index('idx_activities_type', table_name='activities')
    op.drop_index('idx_activities_created_at', table_name='activities')
    op.drop_index('idx_activities_user_id', table_name='activities')
    op.drop_table('activities')