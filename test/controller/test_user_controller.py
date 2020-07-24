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

            self.assertStatus(c.get('/logout'), 200)
            self.assertStatus(c.get('/logout'), 401)

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
