from sqlalchemy import (
    ForeignKey,
    Table,
    Column,
    MetaData,
    Integer,
    TIMESTAMP,
    text,
    BIGINT,
)


metadata_obj = MetaData()


users_table = Table(
    "users",
    metadata_obj,
    Column("user_id", BIGINT, primary_key=True),
    Column("created_at", TIMESTAMP, server_default=text("TIMEZONE('utc', now())")),
    Column("kreo", Integer),
)

purchases_table = Table(
    "purchases",
    metadata_obj,
    Column("id_user", BIGINT, ForeignKey("users.user_id")),
    Column("size", Integer),
    Column("purchased_at", TIMESTAMP, server_default=text("TIMEZONE('utc', now())")),
)
