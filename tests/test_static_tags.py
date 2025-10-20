from django.test import SimpleTestCase, override_settings
from django.template import Template, Context

from wt_templatetags.templatetags.static_tags import make_min


class TestMakeMinFunction(SimpleTestCase):
    """Direct unit tests for make_min function"""

    def test_css_extension(self):
        result = make_min('main.css')
        self.assertEqual(result, 'main.min.css')

    def test_js_extension(self):
        result = make_min('app.js')
        self.assertEqual(result, 'app.min.js')

    @override_settings(
        WT_TEMPLATETAGS={'STATIC_MIN_SUFFIX': 'minified'}
    )
    def test_custom_suffix(self):
        result = make_min('main.css')
        self.assertEqual(result, 'main.minified.css')

    @override_settings(
        WT_TEMPLATETAGS={'STATIC_MIN_EXTENSIONS': ['.js']}
    )
    def test_no_matching_extension_silent(self):
        result = make_min('main.css')
        self.assertEqual(result, 'main.css')  # Unchanged

    @override_settings(
        WT_TEMPLATETAGS={
            'STATIC_MIN_EXTENSIONS': ['.js'],
            'STATIC_MIN_FAIL_SILENT': False
        }
    )
    def test_no_matching_extension_raises(self):
        with self.assertRaises(ValueError) as cm:
            make_min('main.css')
        self.assertIn("No matching extension", str(cm.exception))
        self.assertIn("main.css", str(cm.exception))


class TestStaticMinTemplateTag(SimpleTestCase):

    def test_basic_path(self):
        template = Template(
            "{% load static_tags %}{% static_min 'main.css' %}"
        )
        result = template.render(Context())
        self.assertEqual(result, 'main.min.css')
