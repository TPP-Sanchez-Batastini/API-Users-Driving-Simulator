import pytest
from unittest import TestCase

class TestUserController(TestCase):

    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, mocker):
        self.mocker = mocker
        self.mocker.patch