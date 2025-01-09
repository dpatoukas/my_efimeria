"""Initial migration

Revision ID: 662b54628603
Revises: 
Create Date: 2025-01-09 12:07:55.791434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '662b54628603'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### Replace problematic alter_column with table recreation ###
    # Create a new table with the desired schema
    op.create_table(
        'AdminUser_new',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(length=50), nullable=False, unique=True)
    )

    # Copy data from the old table to the new table
    op.execute('INSERT INTO AdminUser_new (id, username) SELECT id, username FROM AdminUser')

    # Drop the old table
    op.drop_table('AdminUser')

    # Rename the new table to the original name
    op.rename_table('AdminUser_new', 'AdminUser')

    # Add other table-specific commands if necessary

def downgrade():
    # Reverse the upgrade steps
    op.create_table(
        'AdminUser_old',
        sa.Column('id', sa.Integer(), nullable=True, primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(length=50), nullable=False, unique=True)
    )

    op.execute('INSERT INTO AdminUser_old (id, username) SELECT id, username FROM AdminUser')

    op.drop_table('AdminUser')
    op.rename_table('AdminUser_old', 'AdminUser')
