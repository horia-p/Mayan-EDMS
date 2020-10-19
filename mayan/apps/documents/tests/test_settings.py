import importlib
import logging

from mayan.apps.documents import storages
from mayan.apps.smart_settings.tests.mixins import SmartSettingTestMixin
from mayan.apps.storage.classes import DefinedStorage
from mayan.apps.testing.tests.base import BaseTestCase

from ..literals import (
    STORAGE_NAME_DOCUMENT_VERSION_PAGE_IMAGE_CACHE, STORAGE_NAME_DOCUMENT_FILES
)
from ..settings import (
    setting_document_file_page_image_cache_maximum_size,
    setting_document_file_storage_backend_arguments,
    setting_documentfilepageimagecache_storage_arguments,
    setting_language_codes
)


class DocumentSettingsTestCase(SmartSettingTestMixin, BaseTestCase):
    def test_documents_language_codes_setting_double_quotes(self):
        self._set_environment_variable(
            name='MAYAN_{}'.format(setting_language_codes.global_name),
            value='["spa","fra"]'
        )

        self.assertEqual(
            setting_language_codes.value,
            ['spa', 'fra']
        )

    def test_documents_language_codes_setting_single_quotes(self):
        self._set_environment_variable(
            name='MAYAN_{}'.format(setting_language_codes.global_name),
            value="['spa','deu']"
        )

        self.assertEqual(
            setting_language_codes.value,
            ['spa', 'deu']
        )


class DocumentStorageSettingsTestCase(SmartSettingTestMixin, BaseTestCase):
    def tearDown(self):
        super().tearDown()
        importlib.reload(storages)

    def test_setting_document_file_image_cache_storage_arguments_invalid_value(self):
        self._set_environment_variable(
            name='MAYAN_{}'.format(
                setting_document_file_page_image_cache_maximum_size.global_name
            ), value='invalid_value'
        )
        self.test_case_silenced_logger_new_level = logging.FATAL + 10
        self._silence_logger(name='mayan.apps.storage.classes')

        with self.assertRaises(expected_exception=TypeError) as assertion:
            importlib.reload(storages)
            DefinedStorage.get(
                name=STORAGE_NAME_DOCUMENT_VERSION_PAGE_IMAGE_CACHE
            ).get_storage_instance()
        self.assertTrue('Unable to initialize' in str(assertion.exception))
        self.assertTrue('document image' in str(assertion.exception))

    def test_setting_document_file_storage_backend_arguments_invalid_value(self):
        self._set_environment_variable(
            name='MAYAN_{}'.format(
                setting_document_file_storage_backend_arguments.global_name
            ), value='invalid_value'
        )
        self.test_case_silenced_logger_new_level = logging.FATAL + 10
        self._silence_logger(name='mayan.apps.storage.classes')

        with self.assertRaises(expected_exception=TypeError) as assertion:
            importlib.reload(storages)
            DefinedStorage.get(
                name=STORAGE_NAME_DOCUMENT_FILES
            ).get_storage_instance()
        self.assertTrue('Unable to initialize' in str(assertion.exception))
        self.assertTrue('document file' in str(assertion.exception))

    def test_setting_document_file_page_image_cache_maximum_size(self):
        old_value = setting_document_file_page_image_cache_maximum_size.value
        new_value = old_value + 1
        setting_document_file_page_image_cache_maximum_size.value = '{}'.format(new_value)

        self.assertEqual(setting_document_file_page_image_cache_maximum_size.value, new_value)
