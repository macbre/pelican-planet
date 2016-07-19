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


from datetime import datetime, timezone

import pytest


@pytest.mark.parametrize(
    'date_string, expected',
    [
        ('2016-03-30T00:00:00Z', (2016, 3, 30, 0, 0, 0)),
        ('2016-07-06T10:15:00+02:00', (2016, 7, 6, 8, 15, 0)),
    ],
    ids=[
        'iso-utc',
        'iso-local',
    ])
def test_make_date(date_string, expected):
    from pelican_planet.utils import make_date

    dt = make_date(date_string)
    expected = datetime(*expected, tzinfo=timezone.utc)

    assert dt == expected


@pytest.mark.parametrize(
    'text, expected, max_words',
    [
        ('<p>A short text.</p>', '<p>A short text.</p>', None),
        ('<p>A short text.</p>', '<p>A short text.</p>', 10),
        ('<p>A short text.</p>', '<p>A short …</p>', 2),
    ],
    ids=[
        'no-limit',
        'big-limit',
        'small-limit',
    ])
def test_make_summary(text, expected, max_words):
    from pelican_planet.utils import make_summary

    summary = make_summary(text, max_words=max_words)

    assert summary == expected
