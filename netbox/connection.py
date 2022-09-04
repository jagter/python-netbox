import requests
import json
import urllib.parse
from netbox import exceptions


class NetboxConnection(object):

    def __init__(self, ssl_verify=False, use_ssl=True, host=None, auth_token=None, auth=None,
                 port=None, api_prefix=None, extra_headers=None):
        self.use_ssl = use_ssl
        self.host = host
        self.auth_token = auth_token
        self.port = port
        self.auth = auth
        self.api_prefix = api_prefix

        self.base_url = 'http{s}://{host}{p}{prefix}'.format(s='s' if use_ssl else '', p=':{}'.format(self.port) if self.port else '', host=self.host, prefix='/api' if api_prefix is None else api_prefix)

        self.session = requests.Session()
        self.session.verify = ssl_verify

        if auth:
            self.session.auth = auth

        if auth_token:
            token = 'Token {}'.format(self.auth_token)
            self.session.headers.update({'Authorization': token})
            self.session.headers.update({'Accept': 'application/json'})
            self.session.headers.update({'Content-Type': 'application/json'})

        if auth and auth_token:
            raise exceptions.AuthException('Only one authentication method is possible. Please use auth or auth_token')

        if extra_headers:
            self.session.headers.update(extra_headers)

    def __request(self, method, params=None, key=None, body=None, url=None):

        if method != 'GET':
            if not self.auth_token:
                raise exceptions.AuthException('Authentication credentials were not provided')

            if self.auth:
                raise exceptions.AuthException('With basic authentication the API is not writable.')

        if url is None:
            if key is not None:
                url = self.base_url + str(params) + str('{}/'.format(key))
            else:
                url = self.base_url + str(params)

        request = requests.Request(method=method, url=url, json=body)
        prepared_request = self.session.prepare_request(request)

        try:
            response = self.session.send(prepared_request)
        except requests.exceptions.ConnectionError:
            err_msg = 'Unable to connect to Netbox host: {}'.format(self.host)
            raise ConnectionError(err_msg) from None
        except requests.exceptions.Timeout:
            raise TimeoutError('Connection to Netbox host timed out') from None
        except Exception as e:
            raise Exception(e)
        finally:
            self.close()

        if not 200 <= response.status_code < 300:
            self.__raise_error(response.status_code, response.content)

        if response.status_code == 204:
            return response.content

        try:
            response_data = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerException(response.content) from None

        return response_data

    def get(self, param, key=None, limit=0, **kwargs):

        if kwargs:
            url = '{}{}?{}&limit={}'.format(self.base_url, param,
                                            '&'.join('{}={}'.format(key, urllib.parse.quote(str(val))) for key, val in kwargs.items()), limit)
        elif key:
            if '_choices' in param:
                url = '{}{}{}/?limit={}'.format(self.base_url, param, key, limit)
            else:
                url = '{}{}/?q={}&limit={}'.format(self.base_url, param, key, limit)
        else:
            url = '{}{}?limit={}'.format(self.base_url, param, limit)

        resp_data = self.__request('GET', params=param, key=key, url=url)

        return resp_data['results']

    def put(self, params):

        return self.__request('PUT', params)

    def patch(self, params, key, **kwargs):

        body_data = {key: value for (key, value) in kwargs.items()}
        resp_data = self.__request('PATCH', params=params, key=key, body=body_data)

        return resp_data

    def post(self, params, required_fields, **kwargs):

        body_data = {key: value for (key, value) in required_fields.items()}

        if kwargs:
            body_data.update({key: value for (key, value) in kwargs.items()})
        resp_data = self.__request('POST', params=params, body=body_data)

        return resp_data

    def delete(self, params, del_id):

        del_str = '{}{}'.format(params, del_id)
        self.__request('DELETE', del_str)

        return True

    def close(self):

        self.session.close()

    def __raise_error(self, http_status_code, http_response):
        """Raise error with detailed information from http request."""
        try:
            error_msg = json.loads(http_response)
        except json.JSONDecodeError:
            error_msg = http_response

        if http_status_code == 404:
            raise exceptions.NotFoundException(error_msg)
        elif http_status_code == 403:
            raise exceptions.AuthorizationException(error_msg)
        elif http_status_code == 400:
            raise exceptions.ClientException(error_msg)
        elif http_status_code == 503:
            raise exceptions.ServerException(error_msg)
