from django.conf import settings

# TODO: Implement validation system checks

# validate is sequence
# validate items are string
# validate char first position is dot
STATIC_MIN_EXTENSIONS = getattr(settings, 'WT_STATIC_MIN_EXTENSIONS', ['.css', '.js'])

# validation is string
STATIC_MIN_SUFFIX = getattr(settings, 'WT_STATIC_MIN_SUFFIX', 'min')

# validate is bool
STATIC_MIN_FAIL_SILENT = getattr(settings, 'WT_STATIC_MIN_FAIL_SILENT', True)
