#!/usr/bin/python
"""Tools for creating a Club management dashboard for Brawl Stars."""

__license__   = 'LGPLv3'
__docformat__ = 'reStructuredText'

from datetime import datetime
import logging
import os
import shutil
import tempfile

import pybrawl
import json
import traceback

from ._version import __version__
from bstools.api_wrapper import ApiWrapper
from bstools import history
from bstools import fankit
from bstools import io
from bstools import discord
from bstools.memberfactory import MemberFactory
from bstools.models import FormerMember, ProcessedClub, ProcessedPlayer, GetBrawlers

MAX_CLAN_SIZE = 100

logger = logging.getLogger(__name__)

def get_suggestions(config, processed_members, required_trophies):
    """ Returns list of suggestions for the Club leadership to perform.
    Suggestions are to kick, demote, or promote. Suggestions are based on
    user score, and various thresholds in configuration. """

    # sort members by score, and preserve trophy order if relevant
    members_by_score = sorted(processed_members, key=lambda m: (m.score, m.trophies))

    logger.debug("min_club_size: {}".format(config['score']['min_club_size']))
    logger.debug("# members: {}".format(len(members_by_score)))

    suggestions = []
    for index, member in enumerate(members_by_score):
        member.score = 0 # TODO just temp
        if member.blacklist:
            suggestion = config['strings']['suggestionKickBlacklist'].format(name=member.name)
            logger.debug(suggestion)
            suggestions.append(suggestion)
            continue

        # if member on the 'safe' or 'vacation' list, don't make
        # recommendations to kick or demote
        # if not (member.safe or member.vacation) and member.current_war.status == 'na':
        if not (member.safe or member.vacation):
            # suggest kick if inactive for the set threshold
            if member.days_inactive >= config['activity']['threshold_kick']:
                suggestion = config['strings']['suggestionKickInactivity'].format(name=member.name, days=member.days_inactive)
                logger.debug(suggestion)
                suggestions.append(suggestion)
            # if members have a score below zero, we recommend to kick or
            # demote them.
            # if we're above the minimum Club size, recommend kicking
            # poorly participating member.
            elif member.score < config['score']['threshold_kick'] and index <= len(members_by_score) - config['score']['min_club_size']:
                suggestion = config['strings']['suggestionKickScore'].format(name=member.name, score=member.score)
                logger.debug(suggestion)
                suggestions.append(suggestion)
            # If we aren't recommending kicking someone, and their role is
            # > member, recoomend demotion
            elif member.role != 'member' and member.score < config['score']['threshold_demote']:
                suggestions.append(config['strings']['suggestionDemoteScore'].format(name=member.name, score=member.score))

        # if user is above the threshold, and has not been promoted to
        # Vice-President or higher, recommend promotion.
        if not member.no_promote and not member.blacklist and (member.score >= config['score']['threshold_promote']) and (member.role == 'member') and (member.trophies >= required_trophies) and (member.days_from_join > config['activity']['min_days_to_promote']):
            suggestions.append(config['strings']['suggestionPromoteScore'].format(name=member.name, score=member.score))

    # If there are no other suggestions, give some sort of message
    if len(suggestions) == 0:
        if len(members_by_score) < MAX_CLAN_SIZE:
            suggestions.append(config['strings']['suggestionRecruit'])
        else:
            suggestions.append(config['strings']['suggestionNone'])

    return suggestions

def get_scoring_rules(config):
    """ Get list of scoring rules to display on the site.
        TODO These rules are somewhat vague for Brawl Stars: no donations no wars
        Propose to leave this in for now and think of somewhat ingenius and brilliant ;) 
    """

    def get_score_rule_status(score):
        if score > 0:
            return 'good'
        elif score < 0:
             return 'bad'
        else:
            return 'normal'

    rules = [ # TODO no rules defined yet
    #    {'name': config['strings']['ruleParticipate'],        'yes': config['score']['war_participation'],        'no': config['score']['war_non_participation'] },
    #    {'name': config['strings']['ruleCollectionComplete'], 'yes': config['score']['collect_battle_played'],    'no': config['score']['collect_battle_incomplete']},
    #    {'name': config['strings']['ruleCollectionWin'],      'yes': config['score']['collect_battle_won'],       'no': config['score']['collect_battle_lost']},
    #    {'name': config['strings']['ruleWarDayComplete'],     'yes': config['score']['war_battle_played'],        'no': config['score']['war_battle_incomplete']},
    #    {'name': config['strings']['ruleWarDayWin'],          'yes': config['score']['war_battle_won'],           'no': config['score']['war_battle_lost']}
    ]

    for rule in rules:
        rule['yes_status'] = get_score_rule_status(rule['yes'])
        rule['no_status'] = get_score_rule_status(rule['no'])

    return rules

def process_members(config, club, player, member_history):
    """ Process member list, adding calculated meta-data for rendering of
    status in the Club member table. """

    # process members with results from the API
    api_config = pybrawl.Configuration()
    api_config.api_key['authorization'] = config['api']['api_key']
    api_config.access_token = config['api']['api_key']
    logger.debug("players instance")
    players = pybrawl.PlayersApi(pybrawl.ApiClient(api_config))
    factory = MemberFactory(
        config=config,
        club=club,
        player=player,
        member_history=member_history)
    members_processed = []
    rank = 0
    for member_src in club.members:
        playertag = member_src.tag
        player = players.get_player(playertag)
        explevel = player.exp_level
        rank = rank + 1
        members_processed.append(factory.get_processed_member(member_src, rank, explevel))
        
    return members_processed
 
def process_absent_members(config, historical_members):
    absent_members = []

    for tag, member in historical_members.items():
        if member['status'] == 'absent':
            absent_members.append(FormerMember(
                config=config,
                historical_member=member,
                player_tag=tag,
                processed_events=history.process_member_events(config, member['events'])
            ))

    return sorted(absent_members, key=lambda k: k.timestamp, reverse=True)

# NOTE: we're not testing this function because this is where we're
# isolating all of the I/O for the application here. The real "work"
# here is done in all of the calls to functions in this file, or in the
# ClashRoyaleAPI class, both of which are fully covered. (or soon will
# be)
#
# Similarly, we've tagged this function, and this function alone, to
# be ignored by static analysis. I don't want to spread out all of
# the I/O and there's no way to make the exception handling anything
# other than a mess that will trigger teh cognitive complexity
# warnings.
def build_dashboard(config): # pragma: no coverage
    """Compile and render Club dashboard, get club via player."""
    print('- info: requesting info for Club id: {}'.format(config['api']['club_id']))
   
    api = ApiWrapper(config)
    club, player = api.get_data_from_api()

    # Create temporary directory. All file writes, until the very end,
    # will happen in this directory, so that no matter what we do, it
    # won't hose existing stuff.
    tempdir = tempfile.mkdtemp(config['paths']['temp_dir_name'])
    # Putting everything in a `try`...`finally` to ensure `tempdir` is removed
    # when we're done. We don't want to pollute the user's disk.
    try:
        output_path = os.path.expanduser(config['paths']['out'])

        # process data from API
        club_processed = ProcessedClub(club, config)
        player_processed = ProcessedPlayer(player, config)
        brawler_processed = GetBrawlers(player)
        member_history = history.get_member_history(club.members, config['bstools']['timestamp'], io.get_previous_history(output_path))
        members_processed = process_members(config, club, player, member_history)
        former_members = process_absent_members(config, member_history['members'])

        io.parse_templates(
            config,
            member_history,
            tempdir,
            club_processed,
            members_processed,
            player_processed,
            brawler_processed,
            former_members,
            get_suggestions(config, members_processed, club_processed.required_trophies),
            get_scoring_rules(config)
        )

        if(config['bstools']['debug'] == True):
            # archive outputs of API for debugging
            io.dump_debug_logs(
                tempdir,
                {
                    'club'                  : club.to_dict(),
                    'club-processed'        : club_processed,
                    'player-processed'      : player_processed,
                    'members-processed'     : members_processed,
                    'brawler-processed'     : brawler_processed,
                }
            )

        # if fankit is previously downloaded, it will copy fankit. Otherwise,
        # if fankit is enabled, it will download it.
        fankit.get_fankit(tempdir, output_path, config['paths']['use_fankit'])

        io.copy_static_assets(tempdir, config['paths']['club_logo'], config['paths']['favicon'])

        io.move_temp_to_output_dir(tempdir, output_path)

        # TODO discord.trigger_webhooks(config, members_processed)
        #specialization_object = Specialization.objects.get(name="My Test Specialization")


    # except Exception as e:
    #     logger.error('Error bstools: {}'.format(e))
    except Exception as e:
        print(traceback.format_exc())

    finally:
        # Ensure that temporary directory gets deleted no matter what
        shutil.rmtree(tempdir)
