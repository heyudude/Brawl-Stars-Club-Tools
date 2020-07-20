from configparser import SafeConfigParser
import copy
from datetime import datetime
import gettext
import json
import locale
import logging
import os
import requests
try:  # pragma: no coverage
    from packaging.version import parse
except ImportError:  # pragma: no coverage
    from pip._vendor.packaging.version import parse

from ._version import __version__
from bstools import gdoc
from bstools.models import Demerit, MemberVacation

logger = logging.getLogger(__name__)

PYPI_URL = 'https://pypi.org/pypi/bstools/json'
LOCALE_LIST = {
    'de': 'German',
    'en': 'English (default)',
    'fr': 'French',
    'cn': 'Chinese',
    'pt': 'Portuguese',
    'ru': 'Russian'
}

LOCALE_NOT_FOUND_ERROR_TEMPLATE = 'Locale "{}" not defined. Please use one of the following:\n'
for name, description in LOCALE_LIST.items():
    LOCALE_NOT_FOUND_ERROR_TEMPLATE += '  - {} : {}\n'.format(name, description)

# Create config dict with defaults
config_defaults = {
    'api' : {
        'api_key'                       : False,
        'club_id'                       : False,
        'proxy'                         : '',
        'proxy_headers'                 : ''
    },
    'paths' : {
        'out'                           : './bstools-out',
        'favicon'                       : False,
        'club_logo'                     : False,
        'description_html'              : False,
        'temp_dir_name'                 : 'bstools',
        'use_fankit'                    : False
    },
    'www' : {
        'canonical_url'                 : False
    },
    'activity': {
        'threshold_warn'                : 7,
        'threshold_kick'                : 21,
        'min_days_to_promote'           : 0
    },
    'score' : {
        'min_club_size' :               46,
        'threshold_promote' :           160,
        'threshold_demote' :            0,
        'threshold_kick' :              0,
        'threshold_warn' :              30,
        'new_member_grace_period_days': 3
    },
    'history': {
        'num_battles_to_track':            10
    },
    'members': {
        'blacklist'                     : [],
        'no_promote'                    : [],
        'kicked'                        : [],
        'warned'                        : [],
        'vacation'                      : [],
        'safe'                          : [],
        'custom'                        : {}
    },
    'member_table': {
        'show_rank'                     : True,
        'show_rank_previous'            : False,
        'show_name'                     : True,
        'show_xp_level'                 : False,
        'show_score'                    : True,
        'show_trophies'                 : True,
        'show_time_in_club'             : False,
        'show_last_seen'                : False,
        'show_days_inactive'            : True
    },
    'discord' : {
        'webhook_default'                   : '',
        'leaderboard_war'                   : False,
        'leaderboard_donations'             : False,
        'webhook_war_nag'                   : '',
        'warn_inactive'                     : False,
        'scold_missed_war_battle'           : False,
        'scold_missed_collection_battle'    : False
    },
    'google_docs' : {
        'api_key'                           : '',
        'sheet_id'                          : ''
    },
    'bstools' : {
        'debug'                         : False,
        'timestamp'                     : datetime.utcnow(),
        'locale'                        : 'en',
        'version'                       : __version__,
        'latest_version'                : __version__,
        'update_available'              : False
    }
}

def __localize_strings(locale_id):

    logger.debug('specified locale: "{}"'.format(locale_id))
    if locale_id not in LOCALE_LIST:
        print(LOCALE_NOT_FOUND_ERROR_TEMPLATE.format(locale_id))
        exit()

    try:
        locale.setlocale(locale.LC_TIME, (locale_id, 'UTF-8'))
    except locale.Error:
        print('Locale time setting not found in your os for "{}"'.format(locale_id))

    localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
    translate = gettext.translation('bstools', localedir, languages=[locale_id], fallback=True)
    _ = translate.gettext

    return {
        'mainHeader'                : _('{club_name} Club Dashboard'),

        'ctaLookingForClub'         : _('Looking for a Club?'),
        'buttonJoinUs'              : _('Join us!'),

        'sectionMemberTable'        : _('Member list and stats'),
        'sectionMemberTableMobile'  : _('Members'),
        'sectionSuggestions'        : _('Suggestions'),
        'sectionScoring'            : _('Score explanation'),
        'sectionClubLeaderboard'    : _('Leaderboard'),

        'labelClubStats'            : _('Club Stats'),
        'labelClubName'             : _('Club Name'),
        'labelClubScore'            : _('Club Score'),
        'labelCountry'              : _('Country'),
        'labelInternational'        : _('International'),
        'labelRequiredTrophies'     : _('Required Trophies'),
        'labelClubTag'              : _('Club Tag'),
        'labelClubRole'             : _('Club Role'),
        'labelLastUpdate'           : _('Last update'),
        'labelYes'                  : _('Yes'),
        'labelNo'                   : _('No'),
        'labelMember'               : _('Member'),
        'labelRankPrevious'         : _('Previous'),
        'labelMemberName'           : _('Member Name'),
        'labelMemberTag'            : _('Member Tag'),
        'labelMemberJoinDate'       : _('Join Date'),
        'labelMemberLastActivity'   : _('Last Active'),
        'labelBeforeHistory'        : _('Before recorded history'),
        'labelArena'                : _('Arena'),
        'labelXpLevel'              : _('XP Level'),
        'labelScore'                : _('Score'),
        'labelRank'                 : _('Rank'),
        'labelTrophies'             : _('Trophies'),
        'labelDaysInactive'         : _('Days Inactive'),
        'labelDays'                 : _('Days'),
        'labelMonths'               : _('Months'),
        'labelYears'                : _('Years'),
        'labelDay'                  : _('Day'),
        'labelMinutes'              : _('Minutes'),
        'labelHours'                : _('Hours'),
        'labelTimeInClub'           : _('Time in Club'),
        'labelLastSeen'             : _('Last Seen'),
        'labelNotInClub'            : _('Not in Club'),
        'labelNA'                   : _('N/A'),
        'labelViewOldMembers'       : _('View List of Old Members'),
        'labelOldMembers'           : _('Old Members'),

        'memberEventJoinedClub'     : _('Joined Club'),
        'memberEventRoleChange'     : _('Changed role to {}'),
        'memberEventExitClub'       : _('Departed Club'),

        'dialogTitleMemberDetails'  : _('Member Details'),
        'dialogLabelPlayerStats'    : _('Player Stats and Info'),
        'dialogMemberStatsRoyale'   : _('See on StatsRoyale'),
        'dialogMemberRoyaleApi'     : _('See on RoyaleAPI'),
        'dialogLabelPlayerHistory'  : _('Player History'),
        'dialogMemberBlacklist'     : _('Member is on the blacklist. Kick member immediately.'),
        'dialogMemberNoPromote'     : _('Member has been tagged on the "No Promote" list for abusing privileges in the past. Never promote to Vice-President or higher.'),
        'dialogTitleFormerMembers'  : _('Former Members'),
        'dialogTableHeaderNameTag'  : _('Name / tag'),
        'dialogTableHeaderEvents'   : _('Events'),
        'dialogTitleFormerLinks'    : _('Links'),
        'dialogButtonClose'         : _('Close'),

        'tooltipMemberNotInClub'    : _('<strong>{name}</strong> was not in the Club at the time of this war.'),

        'labelFilter'               : _('Filter'),
        'filterNone'                : _('None'),
        'filterLeadership'          : _('Leadership'),
        'filterRoleVP'              : _('Role: Vice-President'),
        'filterRoleMember'          : _('Role: Member'),
        'filterNewMembers'          : _('New Members'),
        'filterInactive'            : _('Inactive'),
        'filterDanger'              : _('In danger'),
        'filterWar'                 : _('War'),

        'suggestionKick'            : _('Members with a <strong class="bad">score below 0</strong> will be recommended for kicking or demotion.'),
        'suggestionInactive'        : _('Members inactive for <strong class="bad">{days_inactive} days</strong> will be kicked.'),
        'suggestionPromote'         : _('A member who achieves <strong class="good">{points} points</strong> is elegible for promotion to <strong>Vice-President</strong> at the discretion of leadership.'),
        'suggestionPromoteMinDays'  : _('Members must be in the Club for a at least <strong>{} days</strong> to be promoted.'),
        'suggestionRecruit'         : _('<strong>Recruit new members!</strong> The team needs some fresh blood.'),
        'suggestionNone'            : _('No suggestions at this time. The Club is in good order.'),
        'suggestionKickBlacklist'   : _('Kick <strong>{name}</strong>. Member is blacklisted.'),
        'suggestionKickInactivity'  : _('Kick <strong>{name}</strong> <strong class="bad">{days} days inactive</strong>'),
        'suggestionKickScore'       : _('Kick <strong>{name}</strong> <strong class="bad">{score}</strong>'),
        'suggestionDemoteScore'     : _('Demote <strong>{name}</strong> <strong class="bad">{score}</strong>'),
        'suggestionPromoteScore'    : _('Promote <strong>{name}</strong> to <strong>Vice-President</strong> <strong class="good">{score}</strong>'),

        'scoreBreakdown'            : _('Score is made of two components: <strong>donation score</strong> and <strong>war participation score</strong>.'),

        'scoreRuleHeader'           : _('For each of the last 10 wars, did member...'),
        'ruleParticipate'           : _('...participate in the war?'),

        'roleLeader'                : _('President'),
        'roleCoLeader'              : _('Vice-President'),
        'roleElder'                 : _('Vice-President'),
        'roleMember'                : _('Member'),
        'roleBlacklisted'           : _('Blacklisted. Kick!'),
        'roleVacation'              : _('On vacation'),
        'roleVacationUntil'         : _('Vacation until {}'),
        'roleInactive'              : _('Inactive {days} days'),
        'roleNoPromote'             : _('Never Promote'),

        'footerDisclaimer'          : _('This content is not affiliated with, endorsed, sponsored, or specifically approved by Supercell and Supercell is not responsible for it.'),
        'footerSeeContentPolicy'    : _("For more information see Supercell's Fan Content Policy.")
    }

def __validate_bstools_settings(config):
    if config['bstools']['debug'] == True:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    return config

def __validate_paths(config):
    logger = logging.getLogger(__name__)

    # If logo_path is provided, use logo from path given, and put it where
    # it needs to go. Otherwise, use the default from the template folder
    logo_src_path = os.path.join(os.path.dirname(__file__), 'templates', 'bstools-logo.png')
    if config['paths']['club_logo']:
        logo_src_path_test = os.path.expanduser(config['paths']['club_logo'])
        if os.path.isfile(logo_src_path_test):
            logo_src_path = logo_src_path_test
        else:
            logger.warn('custom logo file "{}" not found. Using default instead.'.format(logo_src_path_test))
    config['paths']['club_logo'] = logo_src_path

    # If favicon_path is provided, use favicon from path given, and put it
    # where it needs to go. Otherwise, use the default from the template folder
    favicon_src_path = os.path.join(os.path.dirname(__file__), 'templates', 'bstools-favicon.ico')
    if config['paths']['favicon']:
        favicon_src_path_test = os.path.expanduser(config['paths']['favicon'])
        if os.path.isfile(favicon_src_path_test):
            favicon_src_path = favicon_src_path_test
        else:
            logger.warn('custom favicon file "{}" not found. Using default instead.'.format(favicon_src_path_test))
    config['paths']['favicon'] = favicon_src_path

    # if external Club description file is specified, read that file and
    # use it for the Club description section. If not, use the Club
    # description returned by the API
    config['paths']['description_html_src'] = None
    if config['paths']['description_html']:
        description_path = os.path.expanduser(config['paths']['description_html'])
        if os.path.isfile(description_path):
            with open(description_path, 'r') as myfile:
                config['paths']['description_html_src'] = myfile.read()
        else:
            logger.warn('custom description file "{}" not found. Using default instead.'.format(description_path))

    return config

def __parse_value(new_value, template_value):
    value = new_value
    if isinstance(template_value, list):
        value = value.split(',');
        value = [x.strip() for x in value]
    else:
        # if the value represents an integer, convert from string to int
        try:
            value = int(value)
        except ValueError:
            pass

        # if set to "true" or "false" or similar, convert to boolean
        if isinstance(value, str):
            if value.lower() in ['true', 'yes', 'on']:
                value = True
            elif value.lower() in ['false', 'no', 'off']:
                value = False
    return value

def __get_version_info(config):
    logger.debug('Grabbing current version from PyPI')

    try:
        req = requests.get(PYPI_URL)
        latest_version = current_version = parse(config['bstools']['version'])
        if req.status_code == requests.codes.ok:
            j = json.loads(req.text)
            releases = j.get('releases', [])
            for release in releases:
                ver = parse(release)
                latest_version = max(latest_version, ver)

        print('bstools v{}'.format(current_version))
        if latest_version > current_version:
            config['bstools']['latest_version'] = '{}'.format(latest_version)
            config['bstools']['update_available'] = True
            print('*** update available: bstools v{} ***'.format(latest_version))
    except:
        logger.debug('Could not contact PyPI. Continuing as normal.')

    return config

def __process_special_status(config):
    for demerit_type in ['blacklist', 'no_promote']:
        demerits = {}
        for tag in config['members'][demerit_type]:
            demerits[tag] = Demerit(tag=tag, status=demerit_type)
        config['members'][demerit_type] = demerits

    vacations = {}
    for tag in config['members']['vacation']:
        vacations[tag] = MemberVacation(tag=tag)
    config['members']['vacation'] = vacations

    return config

def load_config_file(config_file_name=None, check_for_update=False, locale=None):
    """ Look for config file. If config file exists, load it, and try to
    extract config from config file"""

    config = copy.deepcopy(config_defaults)

    if config_file_name and os.path.isfile(config_file_name):
        parser = SafeConfigParser()
        parser.read(config_file_name)

        # Map the contents of the ini file with the structure for the config object found above.
        for section in parser.sections():
            section_key = section.lower()
            if section_key in config:
                for (key, value) in parser.items(section):
                    if key in config[section_key]:
                        config[section_key][key] = __parse_value(value, config[section_key][key])

    config = __validate_paths(config)
    config = __validate_bstools_settings(config)
    config = __process_special_status(config)

    # Augment from Google Sheet
    config = gdoc.get_member_data_from_sheets(config)

    if check_for_update:
        config = __get_version_info(config)

    if locale:
        config['bstools']['locale'] = locale

    config['strings'] = __localize_strings(config['bstools']['locale'])

    return config
