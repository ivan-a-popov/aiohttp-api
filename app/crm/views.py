import uuid
from app.crm.schemas import ListUsersResponseSchema, UserGetRequestSchema, UserGetResponseSchema, UserAddSchema
from app.web.app import View
from app.crm.models import User
from app.web.utils import json_response, check_basic_auth
from aiohttp.web_exceptions import HTTPNotFound, HTTPUnauthorized, HTTPForbidden
from aiohttp_apispec import docs, request_schema, response_schema, querystring_schema
from app.web.schemas import OkResponseSchema


class AddUserView(View):
    @docs(tags=["crm"], summary="Add user", description="Add new user to database")
    @request_schema(UserAddSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        data = await self.request.json()
        user = User(email=data["email"], id_=uuid.uuid4(), name=data["name"])
        await self.request.app.crm_accessor.add_user(user)
        return json_response(data=str(user.id_))


class ListUsersView(View):
    @docs(tags=["crm"], summary="List users", description="List users from database")
    @response_schema(ListUsersResponseSchema, 200)
    async def get(self):
        if not self.request.headers.get("Authorization"):
            raise HTTPUnauthorized
        if not check_basic_auth(self.request.headers["Authorization"],
                                username=self.request.app.config.username,
                                password=self.request.app.config.password):
            raise HTTPForbidden
        users = await self.request.app.crm_accessor.list_users()
        # raw_users = [UserSchema().dump(user) for user in users]
        return json_response(data={"users": users})


class GetUserView(View):
    @docs(tags=["crm"], summary="Get user", description="Get user from database")
    @querystring_schema(UserGetRequestSchema)
    @response_schema(UserGetResponseSchema, 200)
    async def get(self):
        if not self.request.headers.get("Authorization"):
            raise HTTPUnauthorized
        if not check_basic_auth(self.request.headers["Authorization"], username=self.request.app.config.username,
                                password=self.request.app.config.password):
            raise HTTPForbidden
        user_id = self.request.query["id"]
        user = await self.request.app.crm_accessor.get_user(user_id)
        if user:
            return json_response(data={"user": [u.to_dict() for u in user]})
        else:
            raise HTTPNotFound


class CheckQueryView(View):
    @response_schema(OkResponseSchema, 200)
    async def get(self):
        return json_response(data=await self.request.app.crm_accessor.check_query())
