from service.user_role_service import UserRoleService
from test.controller.test_controller_base import TestControllerBase


class TestUserService(TestControllerBase):

    def test_register(self):
        with self.app.test_client() as c:
            self.register("a@a.com", "a", c)
            self.register("a@a.com", "a", c, 403)

    def test_login(self):
        with self.app.test_client() as c:
            self.register("a@a.com", "b", c)
            self.login("a@a.com", "a", c, 401)
            self.login("a@a.com", "b", c, 200)

    def test_logout(self):
        with self.app.test_client() as c:
            self.register("a@a.com", "c", c)
            self.login("a@a.com", "c", c, 200)
            self.logout(c)
            self.logout(c, 401)

    def test_get_user(self):
        with self.app.test_client() as c:
            id1 = self.register("a@a.com", "d", c)['id']
            id2 = self.register("b@b.com", "e", c)['id']

            self.login("a@a.com", "d", c)

            self.assertStatus(c.get(f"/user/{id1}"), 200)
            self.assertStatus(c.get(f"/user/{id2}"), 401)

    def test_delete_user(self):
        with self.app.test_client() as c:
            id1 = self.register("a@a.com", "d", c)['id']
            id2 = self.register("b@b.com", "e", c)['id']

            self.login("a@a.com", "d", c)

            self.assertStatus(c.delete(f"/user/{id2}"), 401)
            self.assertStatus(c.delete(f"/user/{id1}"), 200)
            self.assertStatus(c.get(f"/user/{id1}"), 401)

    def test_get_user_as_admin(self):
        with self.app.test_client() as c:
            id1 = self.register("a@a.com", "d", c)['id']
            id2 = self.register("b@b.com", "e", c)['id']

            self.login("a@a.com", "d", c)

            self.assertStatus(c.get(f"/user/{id1}"), 200)
            self.assertStatus(c.get(f"/user/{id2}"), 401)

            user_role_svc = UserRoleService()
            user_role_svc.create_user_role_by_name(user_id=id1, role_name='admin')

            self.logout(c)

            self.login("a@a.com", "d", c)

            self.assertStatus(c.get(f"/user/{id1}"), 200)
            self.assertStatus(c.get(f"/user/{id2}"), 200)

    def test_delete_user_as_admin(self):
        with self.app.test_client() as c:
            id1 = self.register("a@a.com", "d", c)['id']
            id2 = self.register("b@b.com", "e", c)['id']

            self.login("a@a.com", "d", c)

            self.assertStatus(c.delete(f"/user/{id2}"), 401)

            user_role_svc = UserRoleService()
            user_role_svc.create_user_role_by_name(user_id=id1, role_name='admin')

            self.logout(c)

            self.login("a@a.com", "d", c)

            self.assertStatus(c.delete(f"/user/{id2}"), 200)

    def test_get_users(self):
        with self.app.test_client() as c:
            id1 = self.register("a@a.com", "d", c)['id']
            id2 = self.register("b@b.com", "e", c)['id']

            self.login("a@a.com", "d", c)

            self.assertStatus(c.get(f"/user"), 401)

            user_role_svc = UserRoleService()
            user_role_svc.create_user_role_by_name(user_id=id1, role_name='admin')

            self.logout(c)

            self.login("a@a.com", "d", c)

            response = c.get(f"/user")
            self.assert200(response)
            self.assertEquals(2, len(response.json))

    def test_grant_role_to_user(self):
        with self.app.test_client() as c:
            id1 = self.register("a@a.com", "d", c)['id']
            id2 = self.register("b@b.com", "e", c)['id']

            user_role_svc = UserRoleService()
            user_role_svc.create_user_role_by_name(user_id=id1, role_name='admin')

            self.login("b@b.com", "e", c)
            self.assert401(c.put(f"/user/{id2}/roles/{self.roles['admin'].id}"))
            self.logout(c)

            self.login("a@a.com", "d", c)
            self.assert200(c.put(f"/user/{id2}/roles/{self.roles['admin'].id}"))
            self.logout(c)

            self.login("b@b.com", "e", c)
            response = c.get(f"/user")
            self.assert200(response)
            self.assertEquals(2, len(response.json))

    def test_remove_role_from_user(self):
        with self.app.test_client() as c:
            id1 = self.register("a@a.com", "d", c)['id']
            id2 = self.register("b@b.com", "e", c)['id']

            user_role_svc = UserRoleService()
            user_role_svc.create_user_role_by_name(user_id=id1, role_name='admin')

            self.login("a@a.com", "d", c)
            self.assert200(c.put(f"/user/{id2}/roles/{self.roles['admin'].id}"))

            response = c.get(f"/user/{id2}")
            self.assertEquals(2, len(response.json['roles']))

            response = c.delete(f"/user/{id2}/roles/{self.roles['admin'].id}")
            self.assert200(response)

            response = c.get(f"/user/{id2}")
            self.assertEquals(1, len(response.json['roles']))
