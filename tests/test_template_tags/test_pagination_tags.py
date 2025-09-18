from django.test import SimpleTestCase
from django.template import Context, Template


class TestRelativeURLTemplateTag(SimpleTestCase):

    def test_basic_page_url(self):
        template = Template(
            "{% load pagination_tags %}{% relative_url 1 'page' %}"
        )
        result = template.render(Context())
        self.assertEqual(result, "?page=1")

    def test_last_page_url(self):
        template = Template(
            "{% load pagination_tags %}{% relative_url 'last' 'page' %}"
        )
        result = template.render(Context())
        self.assertEqual(result, "?page=last")

    def test_custom_fied_name(self):
        template = Template(
            "{% load pagination_tags %}{% relative_url 1 'offset' %}"
        )
        result = template.render(Context())
        self.assertEqual(result, "?offset=1")

    def test_with_urlencode(self):
        template = Template(
            "{% load pagination_tags %}"
            "{% relative_url 1 'page' 'search=django' %}"
        )
        result = template.render(Context())
        self.assertEqual(result, "?page=1&search=django")

    def test_with_existing_page(self):
        template = Template(
            "{% load pagination_tags %}"
            "{% relative_url 2 'page' 'page=1' %}"
        )
        result = template.render(Context())
        self.assertEqual(result, "?page=2")

    def test_with_existing_page_and_urlencode(self):
        template = Template(
            "{% load pagination_tags %}"
            "{% relative_url 2 'page' 'page=1&search=django' %}"
        )
        result = template.render(Context())
        self.assertEqual(result, "?page=2&search=django")
