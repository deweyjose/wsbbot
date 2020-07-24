from controller.advice_controller import solid_advice
from test.controller.test_controller_base import TestControllerBase


class TestAdviceController(TestControllerBase):

    def test_get_advice(self):
        with self.app.test_client() as c:
            advice = c.get('/advice')
            self.assertIn(advice.get_data(as_text=True), solid_advice)
            self.assertStatus(advice, 200)
