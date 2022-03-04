import typing
from typing import List, Optional
import uuid

from app.crm.models import User
# from app.store.crm.gino import db

from app.store.crm.models import db, ConnectInfo, UserInfo

if typing.TYPE_CHECKING:
    from app.web.app import Application


class CrmAccessor:
    def __init__(self):
        self.app: Optional["Application"] = None

    async def connect(self, app: "Application"):
        self.app = app
        await db.set_bind(f"postgresql://{app.config.db_host}/{app.config.db_name}")
        await db.gino.create_all()
        await self._on_connect()
        print("connect to database")

    async def _on_connect(self):
        await ConnectInfo.create()

    async def disconnect(self, _: "Application"):
        self.app = None
        await db.pop_bind().close()
        print("disconnect from database")

    async def add_user(self, user: User):
        await UserInfo.create(
            id=str(user.id_),
            email=user.email,
            name=user.name
        )

    async def list_users(self) -> List[User]:
        users = await UserInfo.query.gino.all()
        return [u.to_dict() for u in users]

    async def get_user(self, id_: uuid.UUID) -> Optional[User]:
        user = await UserInfo.query.where(UserInfo.id == id_).gino.all()
        return user

    async def check_query(self) -> typing.Union[dict, list]:
        user = await UserInfo.query.where(UserInfo.id == "822b55d4-e358-42cf-acee-0f7c5701d42").gino.all()
        print(user, type(user), len(user))
        return [u.to_dict() for u in user]
    #     return user
    #     res = await db.select([ConnectInfo]).gino.load(ConnectInfo.connect_time).all()
    #     return [e.isoformat() for e in res]
    #