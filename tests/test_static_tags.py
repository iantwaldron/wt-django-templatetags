from django.test import SimpleTestCase, override_settings
from django.template import Template, Context

from wt_templatetags.templatetags.static_tags import static_min, static_version


class TestStaticMinFunction(SimpleTestCase):

    def test_css_extension(self):
        result = static_min('main.css')
        self.assertEqual(result, 'main.min.css')

    def test_js_extension(self):
        result = static_min('app.js')
        self.assertEqual(result, 'app.min.js')

    @override_settings(
        WT_TEMPLATETAGS={'STATIC_MIN_SUFFIX': 'minified'}
    )
    def test_custom_suffix(self):
        result = static_min('main.css')
        self.assertEqual(result, 'main.minified.css')

    @override_settings(
        WT_TEMPLATETAGS={'STATIC_MIN_EXTENSIONS': ['.js']}
    )
    def test_no_matching_extension_silent(self):
        result = static_min('main.css')
        self.assertEqual(result, 'main.css')  # Unchanged

    @override_settings(
        WT_TEMPLATETAGS={
            'STATIC_MIN_EXTENSIONS': ['.js'],
            'STATIC_MIN_FAIL_SILENT': False
        }
    )
    def test_no_matching_extension_raises(self):
        with self.assertRaises(ValueError) as cm:
            static_min('main.css')
        self.assertIn("No matching extension", str(cm.exception))
        self.assertIn("main.css", str(cm.exception))


class TestStaticMinTemplateTag(SimpleTestCase):

    def test_basic_path(self):
        template = Template(
            "{% load static_tags %}{% static_min 'main.css' %}"
        )
        result = template.render(Context())
        self.assertEqual(result, 'main.min.css')


class TestStaticVersionFunction(SimpleTestCase):

    @override_settings(
        WT_TEMPLATETAGS={'STATIC_VERSION': '1.2.3'}
    )
    def test_appends_version_query_string(self):
        result = static_version('css/main.css')
        self.assertEqual(result, 'css/main.css?v=1.2.3')

    @override_settings(
        WT_TEMPLATETAGS={'STATIC_VERSION': '2.0.0 beta'}
    )
    def test_version_with_special_characters(self):
        # check space is properly encoded
        result = static_version('js/app.js')
        # parse.urlencode uses '+' instead of '%20'
        self.assertEqual(result, 'js/app.js?v=2.0.0+beta')

    @override_settings(
        WT_TEMPLATETAGS={'STATIC_VERSION': None}
    )
    def test_no_version_with_fail_silent(self):
        result = static_version('css/main.css')
        self.assertEqual(result, 'css/main.css')

    @override_settings(
        WT_TEMPLATETAGS={
            'STATIC_VERSION': None,
            'STATIC_VERSION_FAIL_SILENT': False
        }
    )
    def test_no_version_without_fail_silent_raises(self):
        with self.assertRaises(AttributeError) as cm:
            static_version('css/main.css')
        self.assertIn("STATIC_VERSION", str(cm.exception))

    def test_bad_path_type(self):
        with self.assertRaises(ValueError) as cm:
            # noinspection PyTypeChecker
            static_version(100)
        self.assertIn('Expected string.', str(cm.exception))

class TestStaticVersionTemplateTag(SimpleTestCase):

    @override_settings(
        WT_TEMPLATETAGS={'STATIC_VERSION': '1.2.3'}
    )
    def test_basic_version(self):
        template = Template(
            "{% load static_tags %}{% static_version 'main.css' %}"
        )
        result = template.render(Context())
        self.assertEqual(result, 'main.css?v=1.2.3')


class TestSmartStaticNode(SimpleTestCase):

    @override_settings(
        WT_TEMPLATETAGS={
            'SMART_STATIC_ACTIVE': True,
            'STATIC_VERSION': '1.0.0',
        }
    )
    def test_active_applies_both_transforms(self):
        from wt_templatetags.settings import app_settings
        app_settings.reload()

        template = Template(
            "{% load static_tags %}{% smart_static 'css/main.css' %}"
        )
        result = template.render(Context())
        # Should have both min and version
        self.assertIn('main.min.css', result)
        self.assertIn('?v=1.0.0', result)

    @override_settings(
        WT_TEMPLATETAGS={'SMART_STATIC_ACTIVE': False}
    )
    def test_inactive_returns_plain_path(self):
        from wt_templatetags.settings import app_settings
        app_settings.reload()

        template = Template(
            "{% load static_tags %}{% smart_static 'css/main.css' %}"
        )
        result = template.render(Context())
        self.assertEqual(result, 'css/main.css')

    @override_settings(
        WT_TEMPLATETAGS={
            'SMART_STATIC_ACTIVE': True,
            'STATIC_VERSION': '1.0.0',
        }
    )
    def test_as_variable_syntax(self):
        from wt_templatetags.settings import app_settings
        app_settings.reload()

        template = Template(
            "{% load static_tags %}"
            "{% smart_static 'css/main.css' as my_css %}"
            "{{ my_css }}"
        )
        result = template.render(Context())
        self.assertIn('main.min.css', result)
        self.assertIn('?v=1.0.0', result)
