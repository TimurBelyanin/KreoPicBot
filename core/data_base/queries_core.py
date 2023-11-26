from core.data_base.models import metadata_obj, users_table, purchases_table
from core.data_base.database import async_engine
from sqlalchemy import Integer, and_, func, insert, select, text, update
from sqlalchemy.sql import over


class AsyncCore:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(metadata_obj.drop_all)
            await conn.run_sync(metadata_obj.create_all)

    @staticmethod
    async def insert_user(user_id: int, kreo: int):
        """Function adds a recording about user(/start)"""
        """Function insert user in database"""
        async with async_engine.connect() as conn:
            # stmt = """INSERT INTO workers (username) VALUES
            #     ('Jack'),
            #     ('Michael');"""
            data = [{"user_id": user_id, "kreo": kreo}]
            stmt = insert(users_table).values(data)
            await conn.execute(stmt)
            await conn.commit()

    @staticmethod
    async def insert_purchase(id_user: int, size: int):
        """Function inserts purchase in database"""
        async with async_engine.connect() as conn:
            # stmt = """INSERT INTO workers (username) VALUES
            #     ('Jack'),
            #     ('Michael');"""
            data = [{"id_user": id_user, "size": size}]
            stmt = insert(purchases_table).values(data)
            await conn.execute(stmt)
            await conn.commit()

    @staticmethod
    async def select_workers():
        """Function gives users for the rating"""
        async with async_engine.connect() as conn:
            query = (
                select(users_table).order_by(users_table.c.kreo.desc()).limit(10)
            )  # SELECT * FROM workers
            result = await conn.execute(query)
            workers = result.all()
            ##################
            return workers

    @staticmethod
    async def does_user_exist(user_id: int):
        """Function gives True if user in the database else False"""
        async with async_engine.connect() as conn:
            query = select(users_table).where(
                users_table.c.user_id == user_id
            )  # SELECT * FROM workers WHERE id = {id}
            result = await conn.execute(query)
            workers = result.fetchone()
        return bool(workers)

    @staticmethod
    async def update_kreo(user_id: int, new_kreo: int):
        async with async_engine.connect() as conn:
            # stmt = text("UPDATE workers SET username=:username WHERE id=:id")
            # stmt = stmt.bindparams(username=new_username, id=worker_id)
            stmt = (
                update(users_table)
                .values(kreo=users_table.c.kreo + new_kreo)
                .where(users_table.c.user_id == user_id)
            )
            await conn.execute(stmt)
            await conn.commit()

    @staticmethod
    async def get_personal_position(user_id: int):
        """Function gives users for the rating"""
        async with async_engine.connect() as conn:
            query = text(
                "SELECT * FROM (SELECT user_id, kreo, row_number() OVER (ORDER BY kreo DESC)  AS rating FROM users) news WHERE user_id=:var",
            )

            result = await conn.execute(query, {"var": user_id})
            user = result.all()
            ##################
        return user

    # @staticmethod
    # async def insert_resumes():
    #     async with async_engine.connect() as conn:
    #         resumes = [
    #             {
    #                 "title": "Python Junior Developer",
    #                 "compensation": 50000,
    #                 "workload": Workload.fulltime,
    #                 "worker_id": 1,
    #             },
    #             {
    #                 "title": "Python Разработчик",
    #                 "compensation": 150000,
    #                 "workload": Workload.fulltime,
    #                 "worker_id": 1,
    #             },
    #             {
    #                 "title": "Python Data Engineer",
    #                 "compensation": 250000,
    #                 "workload": Workload.parttime,
    #                 "worker_id": 2,
    #             },
    #             {
    #                 "title": "Data Scientist",
    #                 "compensation": 300000,
    #                 "workload": Workload.fulltime,
    #                 "worker_id": 2,
    #             },
    #         ]
    #         stmt = insert(resumes_table).values(resumes)
    #         await conn.execute(stmt)
    #         await conn.commit()
    #
    # @staticmethod
    # async def select_resumes_avg_compensation(like_language: str = "Python"):
    #     """
    #     select workload, avg(compensation)::int as avg_compensation
    #     from resumes
    #     where title like '%Python%' and compensation > 40000
    #     group by workload
    #     having avg(compensation) > 70000
    #     """
    #     async with async_engine.connect() as conn:
    #         query = (
    #             select(
    #                 resumes_table.c.workload,
    #                 # 1 вариант использования cast
    #                 # cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation"),
    #                 # 2 вариант использования cast (предпочтительный способ)
    #                 func.avg(resumes_table.c.compensation)
    #                 .cast(Integer)
    #                 .label("avg_compensation"),
    #             )
    #             .select_from(resumes_table)
    #             .filter(
    #                 and_(
    #                     resumes_table.c.title.contains(like_language),
    #                     resumes_table.c.compensation > 40000,
    #                 )
    #             )
    #             .group_by(resumes_table.c.workload)
    #             .having(func.avg(resumes_table.c.compensation) > 70000)
    #         )
    #         print(query.compile(compile_kwargs={"literal_binds": True}))
    #         res = await conn.execute(query)
    #         result = res.all()
    #         print(result[0].avg_compensation)
    #
    # @staticmethod
    # async def insert_additional_resumes():
    #     async with async_engine.connect() as conn:
    #         workers = [
    #             {"username": "Artem"},  # id 3
    #             {"username": "Roman"},  # id 4
    #             {"username": "Petr"},  # id 5
    #         ]
    #         resumes = [
    #             {
    #                 "title": "Python программист",
    #                 "compensation": 60000,
    #                 "workload": "fulltime",
    #                 "worker_id": 3,
    #             },
    #             {
    #                 "title": "Machine Learning Engineer",
    #                 "compensation": 70000,
    #                 "workload": "parttime",
    #                 "worker_id": 3,
    #             },
    #             {
    #                 "title": "Python Data Scientist",
    #                 "compensation": 80000,
    #                 "workload": "parttime",
    #                 "worker_id": 4,
    #             },
    #             {
    #                 "title": "Python Analyst",
    #                 "compensation": 90000,
    #                 "workload": "fulltime",
    #                 "worker_id": 4,
    #             },
    #             {
    #                 "title": "Python Junior Developer",
    #                 "compensation": 100000,
    #                 "workload": "fulltime",
    #                 "worker_id": 5,
    #             },
    #         ]
    #         insert_workers = insert(workers_table).values(workers)
    #         insert_resumes = insert(resumes_table).values(resumes)
    #         await conn.execute(insert_workers)
    #         await conn.execute(insert_resumes)
    #         await conn.commit()
    #
    # @staticmethod
    # async def join_cte_subquery_window_func():
    #     """
    #     WITH helper2 AS (
    #         SELECT *, compensation-avg_workload_compensation AS compensation_diff
    #         FROM
    #         (SELECT
    #             w.id,
    #             w.username,
    #             r.compensation,
    #             r.workload,
    #             avg(r.compensation) OVER (PARTITION BY workload)::int AS avg_workload_compensation
    #         FROM resumes r
    #         JOIN workers w ON r.worker_id = w.id) helper1
    #     )
    #     SELECT * FROM helper2
    #     ORDER BY compensation_diff DESC;
    #     """
    #     async with async_engine.connect() as conn:
    #         r = aliased(resumes_table)
    #         w = aliased(workers_table)
    #         subq = (
    #             select(
    #                 r,
    #                 w,
    #                 func.avg(r.c.compensation)
    #                 .over(partition_by=r.c.workload)
    #                 .cast(Integer)
    #                 .label("avg_workload_compensation"),
    #             )
    #             # .select_from(r)
    #             .join(r, r.c.worker_id == w.c.id).subquery("helper1")
    #         )
    #         cte = select(
    #             subq.c.worker_id,
    #             subq.c.username,
    #             subq.c.compensation,
    #             subq.c.workload,
    #             subq.c.avg_workload_compensation,
    #             (subq.c.compensation - subq.c.avg_workload_compensation).label(
    #                 "compensation_diff"
    #             ),
    #         ).cte("helper2")
    #         query = select(cte).order_by(cte.c.compensation_diff.desc())
    #
    #         res = await conn.execute(query)
    #         result = res.all()
    #         print(f"{len(result)=}. {result=}")
    #
    # # Relationships отсутствуют при использовании Table
