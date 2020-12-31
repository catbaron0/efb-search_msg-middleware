import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 6):
    raise Exception(
        "Python 3.6 or higher is required. Your version is %s." % sys.version)

__version__ = ""
exec(open('efb_search_msg_middleware/__version__.py').read())

long_description = open('README.md').read()

setup(
    name='efb-search_msg-middleware',
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version=__version__,
    description='WeChat Middleware for EH Forwarder Bot to search messages',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='catbaron',
    author_email='catbaron@live.cn',
    url='https://github.com/catbaron0/efb-search_msg-middleware',
    license='AGPLv3+',
    include_package_data=True,
    python_requires='>=3.6',
    keywords=['ehforwarderbot', 'EH Forwarder Bot',
              'EH Forwarder Bot Middleware', 'chatbot'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Communications :: Chat",
        "Topic :: Utilities"
    ],
    install_requires=[
        "ehforwarderbot>=2.0.0b15",
        "python-telegram-bot>=10.0.0<12.0.0",
        "python-magic",
        "peewee",
        "PyYaml",
        "python-dateutil",
    ],
    entry_points={
        'ehforwarderbot.middleware': 'catbaron.search_msg = efb_search_msg_middleware:SearchMessageMiddleware'
    }
)
