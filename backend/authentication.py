from rest_framework import authentication, exceptions
from dishbot.models import GroupMeUser
from utils import request_current_user


class GroupMeAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token_string = request.META.get("HTTP_AUTHORIZATION")
        if not token_string:
            return None
        try:
            user = GroupMeUser.users.get(token=token_string)
        except GroupMeUser.DoesNotExist:
            data = request_current_user(token_string)
            if data["meta"]["code"] != 200:
                raise exceptions.AuthenticationFailed("Invalid Token")
            print(data["response"])
            current_user_data = data["response"]
            user = GroupMeUser.users.create(
                token=token_string,
                name=current_user_data["name"],
                group_me_id=current_user_data["id"],
            )
        if getattr(request.data, "owned_by", None):
            raise exceptions.AuthenticationFailed("Cannot change owner")
        request.data["owned_by"] = user.id
        return (user, token_string)
