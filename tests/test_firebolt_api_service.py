from datetime import date

from firebolt_db.firebolt_api_service import FireboltApiService
from tests import constants
from requests.exceptions import HTTPError
from firebolt_db import exceptions
import pytest

access_token = FireboltApiService.get_access_token({'username': constants.username,
                                                    'password': constants.password})
engine_url = FireboltApiService.get_engine_url_by_db(constants.db_name, access_token["access_token"])


class TestFireboltApiService:

    def test_get_connection_success(self):
        response = FireboltApiService.get_connection(constants.username, constants.password,
                                                     constants.db_name, date.today())
        if type(response) == HTTPError:
            assert response.response.status_code == 503
        else:
            assert response != ""

    def test_get_connection_invalid_credentials(self):
        with pytest.raises(Exception) as e_info:
            response = FireboltApiService.get_connection('username', 'password', constants.db_name, date.today())[0]

    def test_get_connection_invalid_schema_name(self):
        with pytest.raises(Exception) as e_info:
            response = FireboltApiService.get_connection(constants.username, constants.password, 'db_name', date.today())[1]

    def test_get_access_token_success(self):
        assert access_token["access_token"] != ""

    def test_get_access_token_invalid_credentials(self):
        with pytest.raises(Exception) as e_info:
            response = FireboltApiService.get_access_token({'username': 'username', 'password': 'password'})

    def test_get_access_token_via_refresh_success(self):
        assert FireboltApiService.get_access_token_via_refresh(access_token["refresh_token"]) != ""

    def test_get_access_token_via_refresh_invalid_token(self):
        with pytest.raises(Exception) as e_info:
            response = FireboltApiService.get_access_token_via_refresh({'refresh_token': 'refresh_token'})

    def test_get_engine_url_by_db_success(self):
        assert engine_url != ""

    def test_get_engine_url_by_db_invalid_schema(self):
        with pytest.raises(Exception) as e_info:
            response = FireboltApiService.get_engine_url_by_db('db_name', access_token["access_token"])

    def test_get_engine_url_by_db_invalid_header(self):
        with pytest.raises(Exception) as e_info:
            response = FireboltApiService.get_engine_url_by_db(constants.db_name, 'header') != ""

    def test_run_query_success(self):
        try:
            response = FireboltApiService.run_query(access_token["access_token"],
                                                    engine_url, constants.db_name,
                                                    constants.query)
            assert response != ""
        except exceptions.InternalError as http_err:
            assert http_err != ""

    def test_run_query_invalid_url(self):
        with pytest.raises(Exception) as e_info:
            response = FireboltApiService.run_query(access_token["access_token"], "",
                                                    constants.db_name, constants.query) != {}

    def test_run_query_invalid_schema(self):
        with pytest.raises(Exception) as e_info:
            response = FireboltApiService.run_query(access_token["access_token"],
                                                    engine_url, 'db_name', constants.query)

    def test_run_query_invalid_header(self):
        try:
            response = FireboltApiService.run_query('header',
                                                    engine_url, constants.db_name,
                                                    constants.query)
            assert response != ""
        except exceptions.InternalError as e_info:
            assert e_info != ""

    def test_run_query_invalid_query(self):
        with pytest.raises(Exception) as e_info:
            response = FireboltApiService.run_query(access_token["access_token"],
                                                    engine_url, constants.db_name, 'query')
