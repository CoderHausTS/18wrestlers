from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post = Table('post', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=8192)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
    Column('status', String(length=25)),
    Column('visibility', String(length=25)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['post'].columns['status'].create()
    post_meta.tables['post'].columns['visibility'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['post'].columns['status'].drop()
    post_meta.tables['post'].columns['visibility'].drop()
