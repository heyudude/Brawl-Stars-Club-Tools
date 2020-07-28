from argparse import ArgumentParser, RawDescriptionHelpFormatter
import gettext
import logging
import os
import sys

from ._version import __version__
from .bstools import build_dashboard
from .config import load_config_file
from .memberfactory import MemberFactory
from .scorecalc import ScoreCalculator

logger = logging.getLogger(__name__)

def parse_args(argv):
    # parse command line arguments
    parser = ArgumentParser(prog='bstools',
                            description='''A tool for creating a dashboard for Club participation in
                                             ClashRoyale. See https://developer.brawlstars.com to sign up
                                             for a developer account and create an API key to use with this.''')
    parser.add_argument('--locale',
                        metavar='LOCALE',
                        help='Locale if language other than English is desired'
                        )
    parser.add_argument('--config',
                        metavar='CONFIG-FILE',
                        help='configuration file for this app.')
    parser.add_argument('--api_key',
                        metavar='KEY',
                        help='API key for developer.brawlstars.com')
    parser.add_argument('--club',
                        metavar='TAG',
                        help='Club ID from Brawl Stars. If it starts with a "#", Club ID must be quoted.')
    parser.add_argument('--player',
                        metavar='TAG',
                        help='Player ID from Brawl Stars. If it starts with a "#", Player ID must be quoted. Note Brawlstars API needs a player tag to get the Club info')
    parser.add_argument('--out',
                        metavar='PATH',
                        help='Output path for HTML.')
    parser.add_argument('--favicon',
                        metavar='PATH',
                        help='Source path for favicon.ico. If provided, we will copy to the output directory.')
    parser.add_argument('--club_logo',
                        metavar='PATH',
                        help='Source path for Club logo PNG. Recommended at least 64x64 pizels. If provided, we will copy to the output directory.')
    parser.add_argument('--description',
                        metavar='PATH',
                        help='Source path snippet of HTML to replace the Club description. Should not be a complete HTML document. Sample here: https://github.com/AaronTraas/bstools-agrassar-assets/blob/master/description.html\n\nIf provided, we will copy to the output directory.')
    parser.add_argument('--canonical_url',
                        metavar='URL',
                        help='Canonical URL for this site. Used for setting the rel=\'canonical\' link in the web site, as well as generating the robots.txt and sitemap.xml')
    parser.add_argument('--debug',
                        action='store_true',
                        help='Turns on debug mode')
    parser.add_argument('--version',
                        action='store_true',
                        help='List the version of bstools.')

    return parser.parse_args(argv)

def get_config_from_args(args, check_config_file=True, config_default='~/.bstools'):
    if args.version:
        print(__version__)
        exit(0)

    if args.config:
        config_file_name = args.config
        os.path.expanduser(config_file_name)
        if os.path.isfile(config_file_name) == False:
            logger.error(
                'Config file specified {} not found'.format(config_file_name))
            exit(1)
    else:
        config_file_name = os.path.expanduser(config_default)

    locale = None
    if args.locale:
        locale = args.locale

    config = load_config_file(config_file_name, check_config_file, locale)

    # grab API key and Plaer / Club ID from arguments if applicable
    if args.api_key:
        config['api']['api_key'] = args.api_key
    if args.club:
        config['api']['club_id'] = args.club
    if args.player:
        config['api']['player_id'] = args.player
    if args.out:
        config['paths']['out'] = args.out
    if args.favicon:
        config['paths']['favicon'] = args.favicon
    if args.club_logo:
        config['paths']['club_logo'] = args.club_logo
    if args.description:
        config['paths']['description_html'] = args.description
    if args.canonical_url:
        config['www']['canonical_url'] = args.canonical_url
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        config['bstools']['debug'] = True

    return config

def main():  # pragma: no cover
    args = parse_args(sys.argv[1:])

    config = get_config_from_args(args)

    # Build the dashboard
    build_dashboard(config)