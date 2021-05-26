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


from collections import OrderedDict
from pathlib import Path
from ssl import CertificateError

import feedparser


def test_get_feeds(datadir):
    from pelican_planet.planet import Planet

    feeds = {
        "Le blog à Perceval": "file://%s/perceval.atom.xml" % datadir,
    }
    p = Planet(feeds)
    p.get_feeds()

    assert p._feeds == feeds
    assert len(p._articles) == 7

    titles = [a["title"] for a in p._articles]
    titles.reverse()
    assert titles == [
        "Sloubi 1 !",
        "Sloubi 2 !",
        "Sloubi 3 !",
        "Sloubi 4 !",
        "Sloubi 5 !",
        "Sloubi 324 !",
        "Sloubi 325 !",
    ]


def test_get_multiple_feeds(datadir):
    from pelican_planet.planet import Planet

    feeds = OrderedDict(
        [  # Need to guarantee ordering for this test
            ("Le blog à Perceval", "file://%s/perceval.atom.xml" % datadir),
            ("L'auberge à Karadoc", "file://%s/karadoc.atom.xml" % datadir),
        ]
    )
    p = Planet(feeds)
    p.get_feeds()

    assert p._feeds == feeds
    assert len(p._articles) == 10

    titles = [a["title"] for a in p._articles]
    titles.reverse()
    assert titles == [
        "Le gras, c'est la vie",
        "Unagi",
        "Sept cent quarante-quatre",
        "Sloubi 1 !",
        "Sloubi 2 !",
        "Sloubi 3 !",
        "Sloubi 4 !",
        "Sloubi 5 !",
        "Sloubi 324 !",
        "Sloubi 325 !",
    ]


def test_get_multiple_feeds_with_limit(datadir):
    from pelican_planet.planet import Planet

    feeds = OrderedDict(
        [  # Need to guarantee ordering for this test
            ("Le blog à Perceval", "file://%s/perceval.atom.xml" % datadir),
            ("L'auberge à Karadoc", "file://%s/karadoc.atom.xml" % datadir),
        ]
    )
    p = Planet(feeds, max_articles_per_feed=2)
    p.get_feeds()

    assert p._feeds == feeds
    assert len(p._articles) == 4

    titles = [a["title"] for a in p._articles]
    titles.reverse()
    assert titles == [
        "Unagi",
        "Sept cent quarante-quatre",
        "Sloubi 324 !",
        "Sloubi 325 !",
    ]


def test_get_no_feeds():
    from pelican_planet.planet import Planet

    p = Planet({})
    p.get_feeds()

    assert p._feeds == {}
    assert p._articles == []


def test_get_feeds_404(monkeypatch, datadir):
    from pelican_planet.planet import Planet

    def mock_parse(url):
        return {"status": 404}

    monkeypatch.setattr(feedparser, "parse", mock_parse)

    feeds = {
        "Le blog à Perceval": "file://%s/perceval.atom.xml" % datadir,
    }
    p = Planet(feeds)
    p.get_feeds()

    assert p._articles == []


def test_get_feeds_500(monkeypatch, datadir):
    from pelican_planet.planet import Planet

    def mock_parse(url):
        return {"status": 500}

    monkeypatch.setattr(feedparser, "parse", mock_parse)

    feeds = {
        "Le blog à Perceval": "file://%s/perceval.atom.xml" % datadir,
    }
    p = Planet(feeds)
    p.get_feeds()

    assert p._articles == []


def test_get_feeds_ssl_error(monkeypatch, datadir):
    from pelican_planet.planet import Planet

    def mock_parse(url):
        return {
            "bozo": 1,
            "bozo_exception": CertificateError(
                "hostname 'fedoraplanet.org' doesn't match either of "
                "'*.fedorapeople.org', 'fedorapeople.org'"
            ),
        }

    monkeypatch.setattr(feedparser, "parse", mock_parse)

    feeds = {
        "Le blog à Perceval": "file://%s/perceval.atom.xml" % datadir,
    }
    p = Planet(feeds)
    p.get_feeds()

    assert p._articles == []


def test_write_page(datadir, tmpdir):
    from pelican_planet.planet import Planet

    templatepath = Path(datadir.join("planet.md.tmpl").strpath)
    destinationpath = Path(tmpdir.join("planet.md").strpath)
    assert not destinationpath.exists()

    expected = "\n\n\n".join(
        [
            "Some blogs aggregated here.",
            "# Sloubi 325 !",
            "# Sloubi 324 !",
            "# Sloubi 5 !",
            "# Sloubi 4 !",
            "# Sloubi 3 !",
            "# Sloubi 2 !",
            "# Sloubi 1 !",
        ]
    )

    feeds = {
        "Le blog à Perceval": "file://%s/perceval.atom.xml" % datadir,
    }
    p = Planet(feeds)
    p.get_feeds()
    p.write_page(templatepath, destinationpath)

    assert destinationpath.open().read().strip() == expected


def test_write_page_from_multiple_feeds(datadir, tmpdir):
    from pelican_planet.planet import Planet

    templatepath = Path(datadir.join("planet.md.tmpl").strpath)
    destinationpath = Path(tmpdir.join("planet.md").strpath)
    assert not destinationpath.exists()

    expected = "\n\n\n".join(
        [
            "Some blogs aggregated here.",
            "# Sept cent quarante-quatre",
            "# Sloubi 325 !",
            "# Sloubi 324 !",
            "# Unagi",
            "# Sloubi 5 !",
            "# Sloubi 4 !",
            "# Sloubi 3 !",
            "# Sloubi 2 !",
            "# Sloubi 1 !",
            "# Le gras, c'est la vie",
        ]
    )

    feeds = {
        "Le blog à Perceval": "file://%s/perceval.atom.xml" % datadir,
        "L'auberge à Karadoc": "file://%s/karadoc.atom.xml" % datadir,
    }
    p = Planet(feeds)
    p.get_feeds()
    p.write_page(templatepath, destinationpath)

    assert destinationpath.open().read().strip() == expected


def test_write_page_from_multiple_feeds_with_total_limit(datadir, tmpdir):
    from pelican_planet.planet import Planet

    templatepath = Path(datadir.join("planet.md.tmpl").strpath)
    destinationpath = Path(tmpdir.join("planet.md").strpath)
    assert not destinationpath.exists()

    expected = "\n\n\n".join(
        [
            "Some blogs aggregated here.",
            "# Sept cent quarante-quatre",
            "# Sloubi 325 !",
            "# Sloubi 324 !",
            "# Unagi",
        ]
    )

    feeds = {
        "Le blog à Perceval": "file://%s/perceval.atom.xml" % datadir,
        "L'auberge à Karadoc": "file://%s/karadoc.atom.xml" % datadir,
    }
    p = Planet(feeds)
    p.get_feeds()
    p.write_page(templatepath, destinationpath, max_articles=4)

    assert destinationpath.open().read().strip() == expected
