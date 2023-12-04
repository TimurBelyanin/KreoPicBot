from sqlalchemy import (
    ForeignKey,
    Table,
    Column,
    MetaData,
    Integer,
    TIMESTAMP,
    text,
    BIGINT,
    Numeric,
    String,
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
    Column("id_pack", String),
    Column("TB", String, default="Buy"),
    Column("kreo_type", String),
    Column("GEO", String),
    Column("language", String),
    Column("size", Integer),
    Column("offer", String),
    Column("price", Numeric, comment="$"),
    Column("purchased_at", TIMESTAMP, server_default=text("TIMEZONE('utc', now())")),
)
