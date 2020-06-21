import logging
import pybrawl

from bstools import leagueinfo

logger = logging.getLogger(__name__)

class ApiWrapper:
    def __init__(self, config):
        self.config = config

        logger.debug("Creating API instance")
        api_config = pybrawl.Configuration()
        api_config.api_key['authorization'] = config['api']['api_key']
        if config['api']['proxy']:
            api_config.proxy = config['api']['proxy']
        if config['api']['proxy_headers']:
            api_config.proxy_headers = config['api']['proxy_headers']

        self.clubs = pybrawl.ClubsApi(pybrawl.ApiClient(api_config))
        self.players = pybrawl.PlayersApi(pybrawl.ApiClient(api_config))

    def get_data_from_api(self): # pragma: no coverage
        try:
            # Get Club data from API.
            Club = self.clubs.getclub(self.config['api']['club_id'])

            logger.info('- Club: {} ({})'.format(Club.name, Club.tag))

            return (Club)
        except pybrawl.ApiException as e:
            if e.body:
                body = json.loads(e.body)
                if body['reason'] == 'accessDenied':
                    logger.error('developer.brawlstars.com claims that your API key is invalid. Please make sure you are setting up bstools with a valid key.')
                elif body['reason'] == 'accessDenied.invalidIp':
                    logger.error('developer.brawlstars.com says: {}'.format(body['message']))
                else:
                    logger.error('error: {}'.format(body))
            else:
                logger.error('error: {}'.format(e))
        except pybrawl.OpenApiException as e:
            logger.error('error: {}'.format(e))

        # If we've gotten here, something has gone wrong. We need to abort the application.
        exit(0)
