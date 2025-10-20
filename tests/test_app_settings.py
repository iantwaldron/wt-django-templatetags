from django.test import SimpleTestCase, override_settings
from wt_templatetags.settings import AppSettings


class TestAppSettings(SimpleTestCase):

    def setUp(self):
        self.settings = AppSettings()

    def test_defaults_used_when_no_user_settings(self):
        self.assertEqual(
            self.settings.STATIC_MIN_EXTENSIONS,
            ['.css', '.js']
        )

    @override_settings(
        WT_TEMPLATETAGS={'STATIC_MIN_EXTENSIONS': ['.scss']}
    )
    def test_user_settings_override_defaults(self):
        settings = AppSettings()
        self.assertEqual(settings.STATIC_MIN_EXTENSIONS, ['.scss'])

    def test_invalid_setting_raises_attribute_error(self):
        with self.assertRaises(AttributeError) as cm:
            _ = self.settings.NONEXISTENT_SETTING
        self.assertIn("Invalid setting", str(cm.exception))

    def test_caching_works(self):        # First access
        val1 = self.settings.STATIC_MIN_SUFFIX
        # Should be in cache now
        self.assertIn('STATIC_MIN_SUFFIX', self.settings._cached_attrs)
        # Second access should return same object
        val2 = self.settings.STATIC_MIN_SUFFIX
        self.assertEqual(val1, val2)

    def test_reload_clears_cache(self):
        # Access a setting to cache it
        _ = self.settings.STATIC_MIN_SUFFIX
        self.assertIn('STATIC_MIN_SUFFIX', self.settings._cached_attrs)

        # Reload
        self.settings.reload()

        # Cache should be cleared
        self.assertEqual(len(self.settings._cached_attrs), 0)
        self.assertFalse('STATIC_MIN_SUFFIX' in self.settings.__dict__)
