import os
import sys
import setuptools
from setuptools import setup, find_packages
setuptools.dist.Distribution(dict(setup_requires='Babel')) # for message_extractors line below (else warnings / errors)

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'ott.utils',
    'ott.view_header_footer',
    'pillow',
    'simplejson',
    'qrcode'
]

#
# eggs that you need if you're running a version of python lower than 2.7
#
if sys.version_info[:2] < (2, 7):
    requires.extend(['argparse>=1.2.1', 'unittest2>=0.5.1'])

#
# eggs you need for development, but not production
#
dev_extras = (
    'zc.buildout',
)

# when you run: bin/py setup.py extract_messages
# the setup's 'message_extractors' will lookin in the following places for _('Translate me') strings
# this then creates a template (example.pot) of translation text ... which can then feed into a .po file for each language 
# @see: http://babel.edgewall.org/wiki/Documentation/setup.html#id7
# @see: http://blog.abourget.net/2011/1/13/pyramid-and-mako:-how-to-do-i18n-the-pylons-way/
find_translation_strings_in_these_files = {'.' : [
            ('ott/**.py', 'python', None),
            ('ott/**/locale/*.html',     'mako', None),
            ('ott/**/templates/**.html', 'mako', None),
            ('ott/**/templates/**.mako', 'mako', None),
            ('ott/**/static/**', 'ignore', None)
        ]
}

setup(
    name='ott.view',
    version='0.1.0',
    description='Open Transit Tools - View (Python / Javascript)',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="Open Transit Tools",
    author_email="info@opentransittools.org",
    dependency_links=[
        'git+https://github.com/OpenTransitTools/utils.git#egg=ott.utils-0.1.0',
        'git+https://github.com/OpenTransitTools/view_header_footer.git#egg=ott.view_header_footer-0.1.0',
    ],
    license="Mozilla-derived (http://opentransittools.com)",
    url='http://opentransittools.com',
    keywords='ott, otp, view, transit',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require=dict(dev=dev_extras),
    message_extractors = find_translation_strings_in_these_files,
    tests_require=requires,
    test_suite="ott.view",
    entry_points="""\
        [paste.app_factory]
        main = ott.view.pyramid.app:main
    """,
)
