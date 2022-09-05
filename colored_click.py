import os
import subprocess
import json
from datetime import datetime
import click

import typing as t
import click
from click.decorators import command
from click.core import Command, Context, Group, Option, Parameter, ParameterSource, HelpFormatter
from gettext import gettext as _

F = t.TypeVar("F", bound=t.Callable[..., t.Any])

def colored_echo(text, color=None, bold=False):
    if color is None and not text.startswith("  ") and not text.startswith(" "):
        color = "cyan"
        bold = True
    return click.echo(click.style(text, fg=color, bold=bold))

class ColoredSubcommandGroup(Group):
    subcommand_sections = [
        {
            "name": "package",
            "ends_with": "pkgs"
        },
        {
            "name": "layer",
            "ends_with": "layer"
        },
        {
            "name": "allinone",
            "ends_with": "allinone"
        }
    ]
    
    def __init__(self, *args, **kwargs):
        self.subcommand_sections = kwargs.pop("subcommand_sections", self.subcommand_sections)
        super().__init__(*args, **kwargs)

    def format_options(self, ctx: Context, formatter: HelpFormatter) -> None:
        """Writes all the options into the formatter if they exist."""
        opts = []
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if rv is not None:
                opts.append(rv)

        if opts:
            with formatter.section(_(click.style("Options", bold=True))):
                formatter.write_dl(opts)

        self.format_commands(ctx, formatter)

    def format_commands(self, ctx: Context, formatter: HelpFormatter) -> None:
        """Extra format methods for multi methods that adds all the commands
        after the options.
        """
        commands = []
        # reverse self.list_commands(ctx) to show the commands in the order of method definition
        reversed_commands = reversed(self.list_commands(ctx))
        for subcommand in reversed_commands:
            cmd = self.get_command(ctx, subcommand)
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:
                continue
            if cmd.hidden:
                continue

            commands.append((subcommand, cmd))

        # allow for 3 times the default spacing
        if len(commands):
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

            rows = []
            for subcommand_section in self.subcommand_sections:
                name = subcommand_section["name"]
                rows.append(("", ""))
                rows.append((click.style(f"[{name}]", bold=True, fg="red"), ""))
            for subcommand, cmd in commands:
                help = cmd.get_short_help_str(limit)
                for subcommand_section in self.subcommand_sections:
                    if subcommand.endswith(subcommand_section["ends_with"]):
                        # insert next to the section
                        rows.insert(
                            rows.index((click.style(f"[{subcommand_section['name']}]", bold=True, fg="red"), "")) + 1,
                            (click.style("   "+subcommand,bold=True), click.style(help,fg="bright_black"))
                        )
                        break

            if rows:
                with formatter.section(_(click.style("Available subcommands", bold=True))):
                    formatter.write_dl(rows)

def colored_subcommand_group(name: t.Optional[str] = None, **attrs: t.Any) -> t.Callable[[F], ColoredSubcommandGroup]:
    """Creates a new :class:`Group` with a function as callback.  This
    works otherwise the same as :func:`command` just that the `cls`
    parameter is set to :class:`Group`.
    """
    attrs.setdefault("cls", ColoredSubcommandGroup)
    return t.cast(ColoredSubcommandGroup, command(name, **attrs))
