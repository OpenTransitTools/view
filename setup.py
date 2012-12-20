from setuptools import setup, find_packages
import sys

required_eggs = [
    'pyramid',
    'Babel',
    'lingua',
    'simplejson',
]

#
# eggs that you need if you're running a version of python lower than 2.7
#
if sys.version_info[:2] < (2, 7):
    required_eggs.extend(['argparse>=1.2.1', 'unittest2>=0.5.1'])

#
# eggs you need for development, but not production
#
dev_extras = (
    'coverage>=3.5.2',
    'fabric>=1.4.3',
    'zest.releaser>=3.37',
    'distribute',
)

# when you run: bin/py setup.py extract_messages
# the setup's 'message_extractors' will lookin in the following places for _('Translate me') strings
# this then creates a template (example.pot) of translation text ... which can then feed into a .po file for each language 
# @see: http://babel.edgewall.org/wiki/Documentation/setup.html#id7
# @see: http://blog.abourget.net/2011/1/13/pyramid-and-mako:-how-to-do-i18n-the-pylons-way/
find_translation_strings_in_these_files = {'.' : [
            ('ott/**.py', 'python', None),
            ('ott/**/templates/**.html', 'mako', None),
            ('ott/**/templates/**.mako', 'mako', None),
            ('ott/**/static/**', 'ignore', None)
        ]
}

setup(
    name='ott.view',
    version='0.1.0',
    description='Ott View (Python / Javascript)',
    author="Open Transit Tools",
    author_email="info@opentransittools.org",
    dependency_links=('http://opentransittools.com',),
    license="Mozilla-derived (http://opentransittools.com)",
    url='https://opentransittools.com',
    namespace_packages=('ott',),
    packages=find_packages(),
    install_requires=required_eggs,
    extras_require=dict(dev=dev_extras),
    include_package_data=True,  # include non .py / static stuff in egg, like mako templates
    zip_safe=False,             # be able unzip static stuff from egg
    message_extractors = find_translation_strings_in_these_files,
)
