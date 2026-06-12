"""Création des tables initiales (users et audit_logs)

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-06-12 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Créer la table users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(128), unique=True, nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('role', sa.String(32), nullable=False, server_default='SUPERVISOR'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('failed_attempts', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email'),
    )
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_users_username', 'users', ['username'])

    # Créer la table import_jobs
    op.create_table(
        'import_jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('source', sa.String(128), nullable=True),
        sa.Column('status', sa.String(64), nullable=False, server_default='PENDING'),
        sa.Column('imported_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('imported_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('rows_count', sa.Integer(), nullable=True),
        sa.Column('errors', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_import_jobs_imported_by', 'import_jobs', ['imported_by'])

    # Créer la table raw_market_data
    op.create_table(
        'raw_market_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('isin', sa.String(32), nullable=False),
        sa.Column('libelle', sa.String(255), nullable=True),
        sa.Column('compartiment', sa.String(8), nullable=True),
        sa.Column('date_seance', sa.Date(), nullable=False),
        sa.Column('cours_ouverture', sa.Float(), nullable=True),
        sa.Column('cours_cloture', sa.Float(), nullable=True),
        sa.Column('volume', sa.Float(), nullable=True),
        sa.Column('capitalisation', sa.Float(), nullable=True),
        sa.Column('import_job_id', sa.Integer(), sa.ForeignKey('import_jobs.id'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_raw_market_data_isin', 'raw_market_data', ['isin'])
    op.create_index('ix_raw_market_data_import_job_id', 'raw_market_data', ['import_job_id'])

    # Créer la table processed_data
    op.create_table(
        'processed_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('raw_data_id', sa.Integer(), sa.ForeignKey('raw_market_data.id'), nullable=False),
        sa.Column('rendement', sa.Float(), nullable=True),
        sa.Column('volatilite_5j', sa.Float(), nullable=True),
        sa.Column('volume_relatif', sa.Float(), nullable=True),
        sa.Column('anomaly_score', sa.Float(), nullable=True),
        sa.Column('is_anomaly', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('computed_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_processed_data_raw_data_id', 'processed_data', ['raw_data_id'])

    # Créer la table alerts
    op.create_table(
        'alerts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('processed_data_id', sa.Integer(), sa.ForeignKey('processed_data.id'), nullable=True),
        sa.Column('isin', sa.String(32), nullable=True),
        sa.Column('compartiment', sa.String(8), nullable=True),
        sa.Column('alert_type', sa.String(128), nullable=True),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('status', sa.String(64), nullable=False, server_default='NOUVELLE'),
        sa.Column('assigned_to', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('closed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_alerts_processed_data_id', 'alerts', ['processed_data_id'])
    op.create_index('ix_alerts_assigned_to', 'alerts', ['assigned_to'])


def downgrade() -> None:
    op.drop_index('ix_alerts_assigned_to', table_name='alerts')
    op.drop_index('ix_alerts_processed_data_id', table_name='alerts')
    op.drop_table('alerts')
    op.drop_index('ix_processed_data_raw_data_id', table_name='processed_data')
    op.drop_table('processed_data')
    op.drop_index('ix_raw_market_data_import_job_id', table_name='raw_market_data')
    op.drop_index('ix_raw_market_data_isin', table_name='raw_market_data')
    op.drop_table('raw_market_data')
    op.drop_index('ix_import_jobs_imported_by', table_name='import_jobs')
    op.drop_table('import_jobs')
    op.drop_index('ix_audit_logs_user_id', table_name='audit_logs')
    op.drop_table('audit_logs')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
