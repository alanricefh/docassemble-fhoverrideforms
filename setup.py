import os
import sys
from setuptools import setup, find_packages
from fnmatch import fnmatchcase
from distutils.util import convert_path

standard_exclude = ('*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')

def find_package_data(where='.', package='', exclude=standard_exclude, exclude_directories=standard_exclude_directories):
    out = {}
    stack = [(convert_path(where), '', package)]
    while stack:
        where, prefix, package = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                        stack.append((fn, '', new_package))
                else:
                    stack.append((fn, prefix + name + '/', package))
            else:
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out

setup(name='docassemble.fhoverrideforms',
      version='1.0.0',
      description=('Automating Override Forms for Financial Horizons'),
      long_description="# Docassemble Override Forms\r\n\r\nAutomation script for creating override forms at Financial Horizons.\r\n\r\n## Setup instructions\r\n\r\n- Install docassemble (see [How to install docassemble](https://docassemble.org/docs/installation.html))\r\n- Log in to admin account\r\n- Set up the [Configuration](https://docassemble.org/docs/config.html)\r\n\r\n  > ⚠️ Make sure that any newly-added property in the YAML file is not already defined in the file.\r\n\r\n  - Email\r\n\r\n    Email config is required to send emails to carriers, see [E-mail configuration](https://docassemble.org/docs/config.html#mail)\r\n\r\n    SMTP is likely the best option to work with FH's Microsoft Exchange server.\r\n  - Translations\r\n\r\n    Make sure the `words` property (used to translate words in interviews) is set to the below code. See [words](https://docassemble.org/docs/config.html#words)\r\n\r\n    ```yaml\r\n    words:\r\n      - docassemble.base:data/sources/us-words.yml\r\n      # adds french translation for docassemble\r\n      - docassemble.base:data/sources/fr-words.yml\r\n      # adds french translations for override form interview\r\n      - docassemble.fhoverrideforms:data/sources/words.yml\r\n    ```\r\n- In 'Package Management', install this package using the Github URL (i.e. https://github.com/bensengupta/docassemble-fhoverrideforms)\r\n- The interview should now be accessible at https://YOUR_DOCASSEMBLE_URL/fhoverrideforms/interview?new_session=1\r\n  - For user-friendly URLS, see the [`dispatch` directive](https://docassemble.org/docs/config.html#dispatch) (the interview name is `docassemble.fhoverrideforms:data/questions/interview.yml`)\r\n- Note that emails will not send to carriers until the `DEBUG_EMAIL = True` line is set to `DEBUG_EMAIL = False` in `override_forms.py`. To do this, you can make changes via GitHub in your browser or set up the playground (see below instructions) and edit the file in the 'Modules' section\r\n\r\n## Development setup instructions\r\n\r\n- If possible, the docassemble docs recommends running a separate instance of docassemble for development since changes to interview files often require a full server restart and might inconvenience users.\r\n\r\n- Set up [GitHub integration](https://docassemble.org/docs/packages.html#github) (or another integration) to back up and track version history of interview files.\r\n\r\n  Note that if you wish to delete a file in the Playground, you must also manually delete it on GitHub.\r\n- Set up the playground\r\n  - Open the Playground, click on arrow on top left and click 'Manage Projects'\r\n  - Create a new project\r\n  - Folders > Packages > Pull\r\n  - Enter GitHub URL and click Pull\r\n  - The package is now ready to edit in the playground\r\n    \r\n    If you configured GitHub integration, you should see a GitHub button at the bottom of the packages screen to push changes to GitHub\r\n\r\n    Make sure you are running the main interview file `interview.yml`. Running the other files will not work.",
      long_description_content_type='text/markdown',
      author='Benjamin Sengupta',
      author_email='benjamin.sengupta@gmail.com',
      license='',
      url='https://docassemble.bensengupta.com',
      packages=find_packages(),
      namespace_packages=['docassemble'],
      install_requires=['Babel>=2.9.1'],
      zip_safe=False,
      package_data=find_package_data(where='docassemble/fhoverrideforms/', package='docassemble.fhoverrideforms'),
     )

