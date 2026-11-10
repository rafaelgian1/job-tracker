"""remove pending from analysis_status

Revision ID: ae8600e13a71
Revises: b1f8e33e4fd0
Create Date: 2026-11-10 13:04:12.144138

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as postgresql

# revision identifiers, used by Alembic.
revision: str = "ae8600e13a71"
down_revision: Union[str, Sequence[str], None] = "b1f8e33e4fd0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    status_enum = postgresql.ENUM(
        "completed",
        "failed",
        name="analysis_status_updated",
    )
    status_enum.create(op.get_bind())
    op.alter_column(
        "job_analysis",
        "analysis_status",
        type_=status_enum,
        postgresql_using="analysis_status::text::analysis_status_updated",
    )
    op.execute("DROP TYPE analysis_status;")
    op.execute("ALTER TYPE analysis_status_updated RENAME TO analysis_status;")


def downgrade() -> None:
    status_enum = postgresql.ENUM(
        "pending",
        "completed",
        "failed",
        name="analysis_status_updated",
    )
    status_enum.create(op.get_bind())
    op.alter_column(
        "job_analysis",
        "analysis_status",
        type_=status_enum,
        postgresql_using="analysis_status::text::analysis_status_updated",
    )
    op.execute("DROP TYPE analysis_status;")
    op.execute("ALTER TYPE analysis_status_updated RENAME TO analysis_status;")
