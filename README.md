# Blog aggregation, static-website style!

This is a plugin for the [Pelican](https://getpelican.com) static site
generator.

It allows generating a page aggregating blog articles from other web sites.

## Usage

Install this plugin:

    $ pip install git+https://framagit.org/bochecha/pelican-planet#egg=pelican_planet

Then, in your Pelican config file, enable the plugin:

    PLUGINS = [
        ...
        'pelican_planet',
        ...
        ]

Next, declare the feeds you want to aggregate in your Pelican config file:

    PLANET_FEEDS = {
        'Some amazing blog': 'https://example1.org/feeds/blog.atom.xml',
        'Another great blog': 'http://example2.org/feeds/blog.atom.xml',
        }

Write a [Jinja2](http://jinja.pocoo.org/) template for your aggregation page.
For example, if the rest of your website is generated from Markdown pages, then
create a `planet.md.tmpl` file with the following contents:


    Some blogs aggregated here.

    {% for article in articles %}
    # {{ article.title }}

    {% endfor %}

Finally, declare the template and destination page in your Pelican config file:

    PLANET_TEMPLATE = 'planet.md.tmpl'
    PLANET_PAGE = 'content/planet.md'

Then rebuild your website as usual using the `pelican` command line, and you
should have your blog aggregation page.

You'll probably want to rebuild your website periodically though, maybe with a
systemd timer or a cron job, to always fetch the latest articles in the feeds
you aggregate.

## Template design

The template for your aggregation page will be passed an `articles` variable,
containing the list of, well, articles aggregated.

Each item of this list will have the following attributes:

*   `title`: The title of the article;

*   `author`: The author of the article;

*   `link`: The URL to the article on its original website;

## Optional configuration

**TODO:** Document this.

## Legalities

pelican-planet is offered under the terms of the
[GNU Affero General Public License, either version 3 or any later version](http://www.gnu.org/licenses/agpl.html).

We will never ask you to sign a copyright assignment or any other kind of
silly and tedious legal document before accepting your contributions.

In case you're wondering, we do **not** consider that a website built with
pelican-planet would need to be licensed under the AGPL.
