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


from dateutil import parser as dtparser

from pelican.utils import truncate_html_words


def make_date(date_string):
    return dtparser.parse(date_string)


def make_summary(text, max_words=None):
    if max_words is None:
        return text

    return truncate_html_words(text, max_words, end_text='…')
