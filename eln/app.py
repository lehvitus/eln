import click
import os
from dotenv import load_dotenv
from eln.helpers.logger import log_error

load_dotenv()


__author__ = 'Leo Neto'


COMMANDS_FOLDER = os.path.join(os.path.dirname(__file__), 'commands')


class CLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []

        commands = {
            c.rsplit('/', 1)[-1]: c
            for c, _, files in os.walk(COMMANDS_FOLDER) if 'main.py' in files
        }

        for func, path in commands.items():
            # Only include top-level commands
            command = path.split('commands/')[-1].split('/')[0]
            if command not in rv:
                rv.append(func)

        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(COMMANDS_FOLDER, name, 'main.py')

        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)

        try:
            return ns[name]
        except KeyError:
            log_error(f"Failed to load {name} commands")
            raise click.Abort()


@click.command(cls=CLI)
@click.pass_context
def cli(ctx):
    """
        eln: by Leo Neto (Lehvitus ÖU)

        A command-line tool for miscellaneous tasks.
    """

    # Note for contributors:
    #
    # Commands are auto-discovered if they are placed under the commands directory.
    # But please be sure to do the following for this to work:
    #   1. Name your package and click command the same.
    #   2. Place your command definition within your package's `main.py`
    #   3. Any sub-commands of your command should be added directly to your main command.
    #
    #   Access your command like so:
    #   `eln my-command my-sub-command`


if __name__ == '__main__':
    cli()