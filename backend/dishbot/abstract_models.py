from django.db import models


class BaseModel(models.Model):
    created_at: models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OwnedByGroupMeUser(BaseModel):
    owned_by = models.ForeignKey("GroupMeUser", on_delete=models.CASCADE)

    class Meta:
        abstract = True