"""create_functional

Revision ID: e2ff751d30f1
Revises: 0558824649fe
Create Date: 2023-06-06 23:15:50.628110

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2ff751d30f1'
down_revision = '0558824649fe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TYPE record_status AS ENUM ('pending', 'approved', 'rejected');
    """)

    op.execute("""
        CREATE TYPE status AS ENUM ('На проверке', 'Одобренно', 'Отклоненно');
    """)

    op.execute("""
        CREATE TYPE post_new AS ENUM ('moderator', 'administrator', 'member');
    """)

    op.execute("""
        CREATE TYPE client_status AS ENUM ('work', 'blocked');
    """)

    op.execute("""
        CREATE TYPE estimation AS ENUM ('1', '2', '3', '4', '5');
    """)

    op.execute("")
    op.execute("")
    op.execute("")
    op.execute("")
    op.execute("")
    op.execute("")
    op.execute("")
    op.execute("")
    op.execute("")
    op.execute("")
    op.execute("")
    op.execute("")





def downgrade() -> None:
    op.execute("DROP TRIGGER update_admins_work_trigger ON report")
    op.execute("DROP TRIGGER update_violation_trigger ON report")
    op.execute("DROP TRIGGER update_moderators_work_trigger ON post_processing")
    op.execute("DROP TRIGGER account_insert_trigger ON account")
    op.execute("DROP TRIGGER postinfo_trigger ON postinfo")
    op.execute("DROP TRIGGER user_info_post_count_trigger ON user_info")
    op.execute("DROP TYPE record_status")
    op.execute("DROP TYPE status")
    op.execute("DROP TYPE post_new")
    op.execute("DROP TYPE client_status")
    op.execute("DROP TYPE estimation")
    op.execute("DROP FUNCTION update_user_info")
    op.execute("DROP FUNCTION update_user_achievement")
    op.execute("DROP FUNCTION update_moderators_work")
    op.execute("DROP FUNCTION update_admins_work")
    op.execute("DROP FUNCTION update_violation")
    op.execute("DROP FUNCTION create_general_information")
