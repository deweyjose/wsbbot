from service.role_service import RoleService
from test.service.test_service_base import TestServiceBase


class TestRoleService(TestServiceBase):
    role_svc = RoleService()

    def test_create_role(self):
        role = self.role_svc.create_role('foo')
        self.assertEqual('foo', role.name)

    def test_get_roles(self):
        self.role_svc.create_role('foo')
        self.role_svc.create_role('bar')
        x = self.role_svc.get_roles()
        self.assertEqual(3, len(self.role_svc.get_roles()))