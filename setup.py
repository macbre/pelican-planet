# Copyright (c) 2016 - Mathieu Bridon <bochecha@daitauha.fr>
#
# This file is part of pelican-planet
#
# pelican-planet is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pelican-planet is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pelican-planet.  If not, see <http://www.gnu.org/licenses/>.


from pathlib import Path

from setuptools import setup, find_packages


def get_requirements(path):
    lines = Path(path).open('r')
    lines = map(lambda l: l.strip(), lines)
    lines = filter(lambda l: bool(l), lines)
    lines = filter(lambda l: not l.startswith('#'), lines)

    return list(lines)


README = Path('README.md').open().read()
CHANGES = Path('CHANGES.md').open().read()
REQUIREMENTS = get_requirements('requirements.txt')


setup(
    name='pelican-planet',
    description='Blog aggregator plugin for Pelican',
    long_description='%s\n\n%s' % (README, CHANGES),
    version='0.9',
    classifiers=[
        'Development Status :: 4 - Beta',
        ('License :: OSI Approved :: GNU Affero General Public License v3 or '
         'later (AGPLv3+)'),
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        ],
    author='Mathieu Bridon',
    author_email='bochecha@daitauha.fr',
    url='https://framagit.org/bochecha/pelican-planet',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    )
