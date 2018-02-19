import config
import common.ies as ies
import common.custom as custom

import unittest
import uuid
import random
from nose.plugins.attrib import attr
from time import localtime, strftime


class IES_Smoke_Tests(unittest.TestCase):
    _multiprocess_shared_ = True

    def setUp(self):
        try:
            self.error = ''
            self.timestamp = strftime('%Y%m%d%H%M%S', localtime()) + '_' + str(uuid.uuid4())
            self.operations = custom.generate_random_operations(self)
            self.image_url = random.choice(config.sample_image_urls)
        except Exception as self.error:
            assert 1 == 2, custom.catch_exception(self)

    @attr(run=1)
    def test_diagnostics(self):
        try:
            response = ies.diagnostics()
            assert response.status_code == 200, "Expected: 200; Actual: " + str(response.status_code)
            for key in response.json().keys():
                assert key in ['environment', 'version'], "Expected: " + key + " in ['environment', 'version']"
                assert len(response.json()[key]) > 0, "Expected: : " + key + " to not be empty"
        except Exception as self.error:
            assert 1 == 2, custom.catch_exception(self)

    @attr(run=1)
    def test_edit_get_by_url(self):
        try:
            payload = {'url': self.image_url, 'operation': self.operations}
            self.response = ies.edit_get('by_url', payload)
            self.assertions()
        except Exception as self.error:
            assert 1 == 2, custom.catch_exception(self)

    @attr(run=1)
    def test_edit_get_by_url_encoded_operation(self):
        try:
            payload = {'url': self.image_url, 'operation': self.operations}
            self.response = ies.edit_get('by_url_encoded_operation', payload)
            self.assertions()
        except Exception as self.error:
            assert 1 == 2, custom.catch_exception(self)

    @attr(run=1)
    def test_edit_get_by_data(self):
        try:
            image_response = custom.create_test_image(
                image_name=self.timestamp+'.jpg', resolution=(10, 5), options='encode')
            payload = {'image': image_response['encoded_string'], 'operation': self.operations}
            self.response = ies.edit_get('by_data', payload)
            self.assertions()
        except Exception as self.error:
            assert 1 == 2, custom.catch_exception(self)

    @attr(run=1)
    def test_edit_get_by_data_encoded_operation(self):
        try:
            image_response = custom.create_test_image(
                image_name=self.timestamp+'.jpg', resolution=(10, 5), options='encode')
            payload = {'image': image_response['encoded_string'], 'operation': self.operations}
            self.response = ies.edit_get('by_data_encoded_operation', payload)
            self.assertions()
        except Exception as self.error:
            assert 1 == 2, custom.catch_exception(self)

    @attr(run=1)
    def test_edit_post_by_url(self):
        try:
            payload = {'url': self.image_url, 'operation': self.operations}
            self.response = ies.edit_post('by_url', payload)
            self.assertions()
        except Exception as self.error:
            assert 1 == 2, custom.catch_exception(self)

    @attr(run=1)
    def test_edit_post_by_url_encoded_operation(self):
        try:
            payload = {'url': self.image_url, 'operation': self.operations}
            self.response = ies.edit_post('by_url_encoded_operation', payload)
            self.assertions()
        except Exception as self.error:
            assert 1 == 2, custom.catch_exception(self)

    @attr(run=1)
    def test_edit_post_by_data(self):
        try:
            image_response = custom.create_test_image(image_name=self.timestamp+'.jpg', options='encode')
            payload = {'data': image_response['encoded_string'], 'operation': self.operations}
            self.response = ies.edit_post('by_data', payload)
            self.assertions()
        except Exception as self.error:
            assert 1 == 2, custom.catch_exception(self)

    @attr(run=1)
    def test_edit_post_by_data_encoded_operation(self):
        try:
            image_response = custom.create_test_image(image_name=self.timestamp+'.jpg', options='encode')
            payload = {'data': image_response['encoded_string'], 'operation': self.operations}
            self.response = ies.edit_post('by_data_encoded_operation', payload)
            self.assertions()
        except Exception as self.error:
            assert 1 == 2, custom.catch_exception(self)

    def assertions(self):
        assert self.response.status_code == 200, "Expected: 200; Actual: " + str(self.response.status_code)
        assert len(self.response.content) > 0, "Expected: Edited image in base64; Actual: " + self.response.text

    def tearDown(self):
        custom.tear_down(self)
