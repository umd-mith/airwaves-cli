import os
import ConfigParser

def get_config_file():
    return os.path.join(os.path.expanduser("~"), ".airwaves")

def get_config():
    config_file = get_config_file()
    config = ConfigParser.ConfigParser()

    if os.path.isfile(config_file):
        config.read(config_file)
        airtable_key = config.get('main', 'airtable-key')
        ia_access_key = config.get('main', 'ia-access-key')
        ia_secret_key = config.get('main', 'ia-secret-key')
        aapb_username = config.get('main', 'aapb-username')
        aapb_password = config.get('main', 'aapb-password')
        return {
            'airtable-key': airtable_key,
            'ia-access-key': ia_access_key,
            'ia-secret-key': ia_secret_key,
            'aapb-username': aapb_username,
            'aapb-password': aapb_password,
        }
    else:
        set_config()
        return get_config()

def set_config():
    config_file = get_config_file()
    config = ConfigParser.ConfigParser()
    airtable_key = raw_input('airtable-key: ')
    ia_access_key = raw_input('ia-access-key: ')
    ia_secret_key = raw_input('ia-secret-key: ')
    aapb_username = raw_input('aapb api username: ')
    aapb_password = raw_input('aapb api passpword: ')
    config.add_section('main')
    config.set('main', 'airtable-key', airtable_key)
    config.set('main', 'ia-access-key', ia_access_key)
    config.set('main', 'ia-secret-key', ia_secret_key)
    config.set('main', 'aapb-username', aapb_username)
    config.set('main', 'aapb-password', aapb_password)
    config_file = get_config_file()
    config.write(open(config_file, 'w'))

