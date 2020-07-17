"""empty message

Revision ID: 1e7b3fa51758
Revises: 
Create Date: 2020-06-24 10:04:31.513845

"""
import sqlalchemy as sa
from alembic import op
from werkzeug.security import generate_password_hash

# revision identifiers, used by Alembic.
revision = '1e7b3fa51758'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('user_role',
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )

    op.execute('INSERT INTO "role" ("name") VALUES (\'admin\')')
    op.execute('INSERT INTO "role" ("name") VALUES (\'investor\')')

    pwdhash = generate_password_hash('Greed1sG000d')
    op.execute('INSERT INTO "user" ("id", "password", "email") VALUES(\'gordon-root\',\'' + pwdhash + '\',\'ggekko@gekkoco.com\')')
    op.execute('INSERT INTO "user_role" ("user_id", "role_id") VALUES(\'gordon-root\',1)')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_role')
    op.drop_table('user')
    op.drop_table('role')
    # ### end Alembic commands ###
