"""Initial migration - create all tables

Revision ID: 001
Revises:
Create Date: 2026-02-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # chairs
    op.create_table(
        "chairs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("canonical_name", sa.Text(), nullable=False),
        sa.Column("maker", sa.Text()),
        sa.Column("model_number", sa.Text()),
        sa.Column("price_range", sa.Text()),
        sa.Column("features", postgresql.JSONB(), server_default="[]"),
        sa.Column("target_users", postgresql.JSONB(), server_default="[]"),
        sa.Column("pros", postgresql.JSONB(), server_default="[]"),
        sa.Column("cons", postgresql.JSONB(), server_default="[]"),
        sa.Column("comparison_notes", sa.Text()),
        sa.Column("is_recommendable", sa.Boolean(), server_default="false"),
        sa.Column("source_video_ids", postgresql.JSONB(), server_default="[]"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # videos
    op.create_table(
        "videos",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("youtube_video_id", sa.Text(), unique=True, nullable=False),
        sa.Column("title", sa.Text()),
        sa.Column("published_at", sa.DateTime()),
        sa.Column("url", sa.Text()),
        sa.Column("status", sa.Text(), server_default="pending"),
        sa.Column("transcript", sa.Text()),
        sa.Column("transcript_source", sa.Text()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # chair_aliases
    op.create_table(
        "chair_aliases",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("chair_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("chairs.id"), nullable=False),
        sa.Column("alias", sa.Text(), nullable=False),
        sa.Column("source_video_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("videos.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # extraction_logs
    op.create_table(
        "extraction_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("video_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("videos.id"), nullable=False),
        sa.Column("chair_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("chairs.id"), nullable=True),
        sa.Column("raw_mention", sa.Text()),
        sa.Column("context", sa.Text()),
        sa.Column("timestamp_hint", sa.Text()),
        sa.Column("confidence", sa.Text()),
        sa.Column("status", sa.Text(), server_default="unresolved"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # prompts
    op.create_table(
        "prompts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("key", sa.Text(), unique=True, nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("version", sa.Integer(), server_default="1"),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # prompt_versions
    op.create_table(
        "prompt_versions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("prompt_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("prompts.id"), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # recommendation_logs
    op.create_table(
        "recommendation_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("form_input", sa.Text()),
        sa.Column("parsed_conditions", postgresql.JSONB()),
        sa.Column("recommended_chair_ids", postgresql.JSONB()),
        sa.Column("response_text", sa.Text()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # maker_products
    op.create_table(
        "maker_products",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("maker", sa.Text(), nullable=False),
        sa.Column("product_name", sa.Text(), nullable=False),
        sa.Column("model_number", sa.Text()),
        sa.Column("source_url", sa.Text()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # maker_scrape_configs
    op.create_table(
        "maker_scrape_configs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("maker", sa.Text(), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("scrape_method", sa.Text()),
        sa.Column("last_scraped_at", sa.DateTime()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("maker_scrape_configs")
    op.drop_table("maker_products")
    op.drop_table("recommendation_logs")
    op.drop_table("prompt_versions")
    op.drop_table("prompts")
    op.drop_table("extraction_logs")
    op.drop_table("chair_aliases")
    op.drop_table("videos")
    op.drop_table("chairs")
