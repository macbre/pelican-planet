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


from operator import attrgetter

import feedparser
from jinja2 import Template

from .utils import make_date, make_summary


class FeedError(Exception):
    pass


class Planet:
    def __init__(
            self, feeds, max_articles_per_feed=None, max_summary_length=None):
        self._feeds = feeds
        self._max_articles_per_feed = max_articles_per_feed
        self._max_summary_length = max_summary_length

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

    def _get_articles(self, feed, feed_name):
        def _get_articles():
            for article in feed['entries']:
                article['updated'] = make_date(article['updated'])
                article['summary'] = make_summary(
                    article['summary'], max_words=self._max_summary_length)
                article['feed_name'] = feed_name

                yield article

        articles = sorted(
            _get_articles(), key=attrgetter('updated'), reverse=True)
        articles = articles[:self._max_articles_per_feed]

        return articles

    def get_feeds(self):
        for name, url in self._feeds.items():
            try:
                feed = self._get_feed(name, url)

            except FeedError as e:
                print('ERROR: %s' % e)
                continue

            articles = self._get_articles(feed, name)
            self._articles.extend(articles)

    def write_page(self, template, destination, max_articles=None):
        articles = sorted(
            self._articles, key=attrgetter('updated'), reverse=True)
        articles = articles[:max_articles]

        template = Template(template.open().read())
        destination.open(mode='w').write(template.render(articles=articles))
