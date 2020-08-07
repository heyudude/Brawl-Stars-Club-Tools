==================================================
bstools - Brawl Stars Club Dashboard generator
==================================================

This is a tool for creating a dashboard for Club participation in Brawl Stars.
See https://developer.brawlstars.com to sign up for a developer account and
create an API key to use with this.

This tool is a static site generator -- it generates static HTML, JavaScript,
and CSS used to render the dashboard. If you wish to use this, you should set
it up to run once per hour on your web server.

==================================================
Installation
==================================================

This requires Python 3 and pip on your machine. To install, use

.. code::

  pip3 install bstools

If you have an older version installed, to upgrade to the latest version, run:

.. code::

  pip3 install -U bstools


==================================================
Syntax
==================================================

Usage:

.. code::

  bstools [-h] [--locale LOCALE] [--config CONFIG-FILE] [--api_key KEY]
          [--Club TAG] [--Player TAG] [--out PATH] [--favicon PATH] [--club_logo PATH]
          [--description PATH] [--canonical_url URL] [--debug]
          [--version]

optional arguments:
  -h, --help           show this help message and exit
  --locale LOCALE      Locale if language other than English is desired (see `Other languages/locales`_).
  --config FILE        configuration file for this app.
  --api_key KEY        API key for developer.brawlstars.com
  --club_id TAG        Club ID from Brawl Stars. If it starts with a '#', Club ID must be quoted.
  --player_id TAG      Optional player ID from Brawl Stars. If it starts with a '#', Player ID must be quoted.
  --out PATH           Output path for HTML.
  --favicon PATH       Source path for favicon.ico. If provided, we will copy to the output directory.
  --club_logo PATH     Source path for Club logo PNG. Recommended at least 64x64 pizels. If provided, we will copy to the output directory.
  --description PATH   Source path snippet of HTML to replace the Club description. Should not be a complete HTML document. 
  --canonical_url URL  Canonical URL for this site. Used for setting the rel=canonical link in the web site, as well as generating the robots.txt and sitemap.xml
  --debug              Turns on debug mode
  --version            List the version of bstools.

==================================================
Optional config file
==================================================

bstools looks for a config file in your home directory called .bstools

This is an INI file. As of current version, there's only one possible
parameter: api_key. The file should look like:

.. code:: ini

  [API]
  # API key provided for your account at https://developer.brawlstars.com
  # Note that the key is limited to a specific list of public IP addresses
  api_key=<YOUR-API-KEY>

  # Your Club tag
  club_id=#XXXXXX
  
  # Your Player tag (optional)
  player_id=#XXXXXX

  # Proxy URL -- URL for proxy server, if needed
  #proxy=https://my-proxy.com

  # Proxy headers -- custom headers for proxy if needed
  #proxy_headers=headers

  [Paths]
  # your output path. Where you want the static website to live.
  out=/var/www/html

  # Path to the logo artwork for Club. Must be PNG. Recommended at
  # least 64x64 pixels.
  club_logo=~/myclub/logo.png

  # Path to the favicon file you want to use for this
  favicon=~/myclub/favicon.ico

  # Path to a file that contains arbitrary HTML for the site.
  description_html=~/myclub/body.html

  [www]
  # Canonical URL for this site. Used for setting the rel=canonical
  # link in the web site, as well as generating the robots.txt
  # and sitemap.xml
  canonical_url=https://yourclub.com/

For more details, see `samples/bstools.ini <https://github.com/heyudude/Brawl-Stars-Club-Tools/blob/master/samples/bstools.ini>`_

===================================================================
--> TBD WIP Optional blacklist and vacation management using Google Sheets
===================================================================

You can optionally use a Google Sheets log to keep track of demerits
and vacations. If you want that info to be integrated with bstools, you
need to copy the
`bstools member log template <https://docs.google.com/spreadsheets/d/1_8YKfJf-2HVZOgtuosVaGM_50kB8q7YYR3H2d8p0Wzw>`_
to your Google Docs account and use that. Fill in with info about your
Club. Be sure not to re-name any of the tabs, or add/remove any columns.

You will also need to sign up for a `Google Cloud API key <https://developers.google.com/sheets/api/guides/authorizing#APIKey>`_.

Then you will have to go to the `Google Developer API library page <https://console.developers.google.com/apis/library/sheets.googleapis.com>`_, and enable the Google Sheets library for your account.

You will then need to go the the `Google credential management page <https://console.developers.google.com/apis/credentials>`_, edit the API key you created, giving it access to the Sheets API.

Once you have created a key that you can use for this purpose, find the sheet ID from your spreadsheet URL, add
the following to your config file:

.. code:: ini

  [google_docs]
  api_key=<YOUR-API-KEY>
  sheet_id=<YOUR-SHEET-ID>
  
==================================================  
Using the Brawl Stars Official Fan Kit
==================================================

The design of this site is optionally enhanced by the fan kit provided by Supercell here. To enable automated downloading of the fan kit, add:

use_fankit=True

To the [Paths] section of your config file.

NOTE: This requires about 5GB free in your temp forlder on the machine that crtools runs on. It will take 10-15 minutes to download and extract, but only the first time you run with the fankit enabled.

If you have problems, you can manually install the fan kit. See Fan Kit Manual Install Instructions (TBD)
See https://github.com/heyudude/BrawlStarsOfficial-FanKit

==================================================
Other languages/locales
==================================================

bstools currently supports the following languages:

======= =================
locale  language
======= =================
de      German
en      English (default)
fr      French
cn      Chinese
pt      Portugese
ru      Russian
======= =================

If you'd like to use a language other than English, add the following switch
on the command line:

.. code::

  --locale=fr

The above example is French. Use the locale code listed above

If you wish for bstools to be available in another languages, reach out to
me. I'm unable to do the translation myself (I speak only English), but I can
help you provide a translation for this.

==================================================
Suggested usage on a Linux web server
==================================================

This tool is a static site generator -- it generates static HTML, JavaScript,
and CSS used to render the dashboard. If you wish to use this, you should set
it up to run once per hour on your web server using :code:`cron` or similar.
Below is an example setup on Linux.

Assuming root is going to be running the script:

1. Install this application via pip
2. Install nginx or apache
3. Find your document root (e.g., :code:`/var/www/html`)
4. Create :code:`/root/.bstools` file as specified above, and add your
   API key (from https://developer.brawlstars.com), output path (the
   document root), and Club tag
5. Create the following entry in your crontab:

.. code::

  0 * * * * bstools

==================================================
Support
==================================================


Keep in mind, this is a command-line utility that expects a working Python 3
environment. It also assumes you will know how to configure a web server to
serve up HTML, as well as cron or similar on your given platform. There is no
install wizard, GUI of any kind, etc.

==================================================
Contributors
==================================================

All of the non-code contributors are listed in
`CONTRIBUTORS.rst <https://github.com/heyudude/Brawl-Stars-Club-Tools/blob/master/CONTRIBUTORS.rst>`_

==================================================
Image rights
==================================================

All images except the flags included in this repository were created by the
team, and are included in the GPL license. The SVGs were all created in
Inkscape.

The flags included are from http://www.famfamfam.com/lab/icons/flags/, which
as of 5/27/2019 stated it required no attribution or license. We are
interpreting this to mean these are available in the public domain.

It was important to us to make sure the entirety of this application is
open source, and not subject to takedown request. We will not ever
extract assets from the game or from any other web properties.

Optionally, bstools can download the official Brawl Stars fan kit and use
some of the content contained. This is not the default behavior, and no
works copywritten by Supercell are contained within this code.

This content is not affiliated with, endorsed, sponsored, or specifically
approved by Supercell and Supercell is not responsible for it. For more
information see Supercell's Fan Content Policy: https://supercell.com/en/fan-content-policy/
