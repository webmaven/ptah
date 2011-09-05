""" ptah settings """
import colander
from memphis import config


PTAH = config.registerSettings(
    'ptah',

    config.SchemaNode(
        config.Sequence(), colander.SchemaNode(colander.Str()),
        name = 'managers',
        title = 'Managers',
        description = 'List of user logins with access rights to '\
            'ptah management ui.',
        default = ()),

    config.SchemaNode(
        colander.Str(),
        name = 'login',
        title = 'Login url',
        default = ''),

    title = 'Ptah settings',
    )
