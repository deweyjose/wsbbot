from service.user_role_service import UserRoleService
from test.controller.test_controller_base import TestControllerBase


class TestRoleController(TestControllerBase):

    def test(self):
        with self.app.test_client() as c:
            id1 = self.register("a@a.com", "d", c)['id']

            user_role_svc = UserRoleService()
            user_role_svc.create_user_role_by_name(user_id=id1, role_name='admin')

            self.login("a@a.com", "d", c)

            roles = c.get('/role')
            self.assert200(roles)
            # assumes admin and investor roles were created by test_controller_base
            self.assertEqual(2, len(roles.json))
