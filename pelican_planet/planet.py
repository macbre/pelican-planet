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


import feedparser
from jinja2 import Template

from .utils import make_date


class FeedError(Exception):
    pass


class Planet:
    def __init__(self, feeds):
        self._feeds = feeds

        self._articles = []

    def _get_feed(self, name, url):
        parsed = feedparser.parse(url)
        status = parsed.get('status')

        if status is None and parsed['bozo']:
            raise FeedError(
                "Could not download %s's feed: %s"
                % (name, parsed['bozo_exception']))

        elif status == 404:
            raise FeedError(
                "Could not download %s's feed: not found" % name)

        elif status != 200:
            raise FeedError("Error with %s's feed: %s" % (name, parsed))

        return parsed

    def _get_articles(self, feed):
        def _get_articles():
            for article in feed['entries']:
                article['updated'] = make_date(article['updated'])

                yield article

        articles = list(_get_articles())

        return articles

    def get_feeds(self):
        for name, url in self._feeds.items():
            try:
                feed = self._get_feed(name, url)

            except FeedError as e:
                print('ERROR: %s' % e)
                continue

            articles = self._get_articles(feed)
            self._articles.extend(articles)

    def write_page(self, template, destination):
        articles = self._articles

        template = Template(template.open().read())
        destination.open(mode='w').write(template.render(articles=articles))
