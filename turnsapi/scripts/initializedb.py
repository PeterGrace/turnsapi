import os
import sys
import transaction

from sqlalchemy import engine_from_config

from alembic import command
from alembic.config import Config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from turnsapi.models.basic import (
    DBSession,
    Base,
    )
from turnsapi.models.OAuthModel import (
    OAuthModel
    )
from turnsapi.models.game_models import (
    Player,
    Game
)    


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    alembic_cfg = Config(config_uri)
    command.stamp(alembic_cfg, "head")
