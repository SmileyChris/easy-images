from unittest import TestCase

import mock

from . import base


class BaseLedgerTest(TestCase):

    def setUp(self):
        self.ledger = base.BaseLedger()
        self.ledger_kwargs = {
            'source_path': 'easy_images/fake.gif',
            'opts': {'fit': (128, 128)},
        }
        fake_filenameinfo = mock.Mock(self.ledger.filename_info_class)
        fake_filenameinfo.src_dir = 'adir/'
        fake_filenameinfo.hash = 'ahash'
        fake_filenameinfo.ext = '.ext'
        self.ledger.filename_info_class = mock.Mock(
            return_value=fake_filenameinfo)

    def test_meta(self):
        meta = self.ledger.meta(**self.ledger_kwargs)
        self.assertEqual(meta, {})

    def test_meta_list(self):
        self.ledger.meta = mock.Mock(return_value={})
        opts = {'fit': (128, 128)}
        meta_list = self.ledger.meta_list(
            [('a/1.jpg', opts), ('b/2.jpg', opts), ('c/3.jpg', opts)])
        self.assertEqual(meta_list, [{}, {}, {}])
        self.assertEqual(self.ledger.meta.call_count, 3)

    def test_get_filename_info(self):
        opts = {'fit': (128, 128)}
        expected = self.ledger.filename_info_class()
        output = self.ledger.get_filename_info('test.jpg', opts)
        self.assertEqual(output, expected)
        self.ledger.filename_info_class.assert_called_with(
            source_path='test.jpg', opts=opts, ledger=self.ledger)

    def test_get_filename_info_shortcircuit(self):
        info = object()
        opts = {'fit': (128, 128)}
        output = self.ledger.get_filename_info(
            'test.jpg', opts, filename_info=info)
        self.assertEqual(output, info)
        self.assertFalse(self.ledger.filename_info_class.called)

    def test_build_filename(self):
        filename = self.ledger.build_filename(**self.ledger_kwargs)
        self.assertEqual(filename, 'adir/ahash.ext')

    def test_build_filename_custom(self):
        filename = self.ledger.build_filename(
            source_path='easy_images/fake.jpg',
            opts={
                'fit': (128, 128),
                'FILENAME_FORMAT': '{info.hash}{info.ext}',
            })
        self.assertEqual(filename, 'ahash.ext')

    def test_output_extension(self):
        ext = self.ledger.output_extension(meta={})
        self.assertEqual(ext, '.jpg')

    def test_output_extension_transparent(self):
        ext = self.ledger.output_extension(meta={'transparent': True})
        self.assertEqual(ext, '.png')

    def test_output_extension_passed_meta(self):
        self.ledger.meta = mock.Mock(return_value={})
        self.ledger.output_extension(
            meta={}, source_ext='.png', **self.ledger_kwargs)
        self.assertFalse(self.ledger.meta.called)
