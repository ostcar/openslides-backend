from typing import Any, Dict

from ....models.models import User
from ....shared.patterns import FullQualifiedId
from ...generics.update import UpdateAction
from ...util.default_schema import DefaultSchema
from ...util.register import register_action


@register_action("user.reset_password_to_default")
class UserResetPasswordToDefaultAction(UpdateAction):
    """
    Action to reset a password to default of a user.
    """

    model = User()
    schema = DefaultSchema(User()).get_update_schema()

    def update_instance(self, instance: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gets the default_password and reset password.
        """
        user = self.datastore.get(
            FullQualifiedId(self.model.collection, instance["id"]), ["default_password"]
        )
        default_password = self.auth.hash(str(user.get("default_password")))
        instance["password"] = default_password
        return instance
