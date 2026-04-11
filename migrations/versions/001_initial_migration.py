"""Initial migration

Revision ID: 001
Revises:
Create Date: 2026-03-29 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Users table with enhanced columns
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.Text(), nullable=False),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('display_name', sa.Text(), nullable=True),
        sa.Column('google_id', sa.Text(), nullable=True),
        sa.Column('role', sa.Text(), nullable=True, default='buyer'),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=True, default=False),
        sa.Column('last_login_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('NOW()')),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('version', sa.Integer(), nullable=True, default=1),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('google_id'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id'], )
    )

    # Refresh tokens table
    op.create_table(
        'refresh_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('token', sa.Text(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('revoked', sa.Boolean(), nullable=True, default=False),
        sa.Column('revoked_at', sa.DateTime(), nullable=True),
        sa.Column('revoked_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['revoked_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )

    # Wishlist table with enhanced columns
    op.create_table(
        'wishlist',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('display_title', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.Text(), nullable=True),
        sa.Column('subcategory', sa.Text(), nullable=True),
        sa.Column('filters_json', sa.JSON(), nullable=True),
        sa.Column('user_email', sa.Text(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('expiry_date', sa.DateTime(), nullable=True),
        sa.Column('status', sa.Text(), nullable=True, default='active'),
        sa.Column('priority', sa.Text(), nullable=True, default='medium'),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('NOW()')),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('version', sa.Integer(), nullable=True, default=1),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id'], )
    )

    # Clusters table with enhanced columns
    op.create_table(
        'clusters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('normalized_filters', sa.Text(), nullable=False),
        sa.Column('display_name', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('buyer_count', sa.Integer(), nullable=True, default=0),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=True, default=False),
        sa.Column('last_matched_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('NOW()')),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('version', sa.Integer(), nullable=True, default=1),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('normalized_filters'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id'], )
    )

    # Matches table with enhanced columns
    op.create_table(
        'matches',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cluster_id', sa.Integer(), nullable=True),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('source', sa.Text(), nullable=True),
        sa.Column('title', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('location', sa.Text(), nullable=True),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('status', sa.Text(), nullable=True, default='pending'),
        sa.Column('validation_attempts', sa.Integer(), nullable=True, default=0),
        sa.Column('last_validation_error', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('NOW()')),
        sa.Column('last_validated_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('version', sa.Integer(), nullable=True, default=1),
        sa.ForeignKeyConstraint(['cluster_id'], ['clusters.id'], ),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Clicks table with enhanced columns
    op.create_table(
        'clicks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('match_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('ip_address', sa.Text(), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True, server_default=sa.text('NOW()')),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Audit log table for tracking all changes
    op.create_table(
        'audit_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('table_name', sa.Text(), nullable=False),
        sa.Column('record_id', sa.Integer(), nullable=False),
        sa.Column('action', sa.Text(), nullable=False),  # INSERT, UPDATE, DELETE
        sa.Column('old_values', sa.JSON(), nullable=True),
        sa.Column('new_values', sa.JSON(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True, server_default=sa.text('NOW()')),
        sa.Column('ip_address', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Indexes for performance
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_google_id', 'users', ['google_id'])
    op.create_index('idx_wishlist_user_id', 'wishlist', ['user_id'])
    op.create_index('idx_clusters_normalized_filters', 'clusters', ['normalized_filters'])
    op.create_index('idx_matches_cluster_id', 'matches', ['cluster_id'])
    op.create_index('idx_matches_status', 'matches', ['status'])
    op.create_index('idx_clicks_match_id', 'clicks', ['match_id'])
    op.create_index('idx_clicks_user_id', 'clicks', ['user_id'])
    op.create_index('idx_audit_log_table_record', 'audit_log', ['table_name', 'record_id'])


def downgrade():
    op.drop_index('idx_audit_log_table_record')
    op.drop_index('idx_clicks_user_id')
    op.drop_index('idx_clicks_match_id')
    op.drop_index('idx_matches_status')
    op.drop_index('idx_matches_cluster_id')
    op.drop_index('idx_clusters_normalized_filters')
    op.drop_index('idx_wishlist_user_id')
    op.drop_index('idx_users_google_id')
    op.drop_index('idx_users_email')
    op.drop_table('audit_log')
    op.drop_table('clicks')
    op.drop_table('matches')
    op.drop_table('clusters')
    op.drop_table('wishlist')
    op.drop_table('refresh_tokens')
    op.drop_table('users')