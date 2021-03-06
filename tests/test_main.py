import bstools

__config_debug =  '''
[bstools]
debug=True
'''

def test_parse_args_config_file(tmpdir):
    """Send a custom config file to the parser and verify that it
    loads and parses properly"""
    config_file = tmpdir.mkdir('test_parse_args').join('config.ini')
    config_file.write(__config_debug)

    argv = [
        '--config', str(config_file.realpath())
    ]

    config = bstools.get_config_from_args(bstools.parse_args(argv), False)

    assert config['bstools']['debug'] == True

def test_parse_args_config_file_not_found():
    """Checks that missing file is properly handled when a config
    file is specified."""
    argv = [
        '--config', '~/fake/path/that/does/not/exist'
    ]

    try:
        config = bstools.get_config_from_args(bstools.parse_args(argv))
    except SystemExit as e:
        assert e.code != 0
        return

    # Fail if we didn't catch a SystemExit
    assert False

def test_parse_args_version(capsys):
    argv = [
        '--version'
    ]

    try:
        config = bstools.get_config_from_args(bstools.parse_args(argv))
    except SystemExit as e:
        #
        assert e.code == 0
        captured = capsys.readouterr()
        assert captured.out == "{}\n".format(bstools.__version__)
        return

    # Fail if we didn't catch a SystemExit
    assert False

def test_parse_args_all(tmpdir):
    """Test all of the other command line arguments, other than
    config file path which is a bit of a special case."""
    argv = [
        '--api_key',        'FakeAPIKey',
        '--Club',           '#FakeClubTag',
        '--out',            '/fake/output/path',
        '--favicon',        '/fake/favicon/path',
        '--club_logo',      '/fake/Club/logo/path',
        '--description',    '/fake/description/path',
        '--canonical_url',  'https://fake-canonical-url.fake-tld/fake/path',
        '--locale',         'fr',
        '--debug'
    ]
    config = bstools.get_config_from_args(bstools.parse_args(argv), False, '~/fake/path/that/does/not/exist')
    assert config['api']['api_key'] == argv[1]
    assert config['api']['club_id'] == argv[3]
    assert config['paths']['out'] == argv[5]
    assert config['paths']['favicon'] == argv[7]
    assert config['paths']['club_logo'] == argv[9]
    assert config['paths']['description_html'] == argv[11]
    assert config['www']['canonical_url'] == argv[13]
    assert config['bstools']['debug'] == True
    assert config['bstools']['locale'] == 'fr'

