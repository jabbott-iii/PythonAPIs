from _collections_abc import AsyncGenerator
import datetime
import uuid
from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship

DATABASE_URL = "sqlite_+aiosqlite:///./test.db"                                                              # database connection string

utc_now = datetime.datetime.now(datetime.timezone.utc)                                                       # utc variable necessary for timestamping

class Base(DeclarativeBase):                                                                                 # necessary base class for models to avoid warnings
    pass

class Post(Base):                                                                                            # define table structure
    __tablename__ = "posts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)                                    # primary key column with UUID
    caption = Column(Text)                                                                                   # optional caption for post
    url = Column(String, nullable=False)                                                                     # url of the post
    file_type = Column(String, nullable=False)                                                               # type of the file (image, video, etc.)
    file_name = Column(String, nullable=False)                                                               # name of the file
    created_at = Column(DateTime, default=utc_now)                                                           # timestamp of post creation

engine = create_async_engine(DATABASE_URL, echo=True)                                                          # create engine for database connection

async_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)                                        # create sessionmaker for sessions

async def create_db_and_tables():                                                                              # create tables / database
    async with engine.begin() as conn:                                                                         # begin connection
        await conn.run_sync(Base.metadata.create_all)                                                          # create tables after connecting

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:                                           # dependency to get session
    async with async_sessionmaker() as session:                                                                # create session
        yield session                                                                                          # yield session for use