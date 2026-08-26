"""Refactor summary to meeting-based

Revision ID: a1b2c3d4e5f6
Revises: 82025bb8a8e4
Create Date: 2026-08-26 14:12:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '82025bb8a8e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'meeting_summaries',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('meeting_id', sa.UUID(), nullable=False),
        sa.Column('summary_text', sa.Text(), nullable=False),
        sa.Column('summary_json', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['meeting_id'], ['meetings.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_meeting_summaries_meeting_id'), 'meeting_summaries', ['meeting_id'], unique=True)
    op.drop_index(op.f('ix_daily_summaries_date'), table_name='daily_summaries')
    op.drop_table('daily_summaries')


def downgrade() -> None:
    op.create_table(
        'daily_summaries',
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('summary_text', sa.Text(), nullable=False),
        sa.Column('summary_json', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('meeting_count', sa.Integer(), nullable=False),
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_daily_summaries_date'), 'daily_summaries', ['date'], unique=True)
    op.drop_index(op.f('ix_meeting_summaries_meeting_id'), table_name='meeting_summaries')
    op.drop_table('meeting_summaries')
