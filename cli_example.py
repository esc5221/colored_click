from colored_click import colored_subcommand_group, colored_echo

subcommand_sections = [
    {"name": "Package", "ends_with": "pkgs"},
    {"name": "Layer", "ends_with": "layer"},
    {"name": "Test", "ends_with": "test"},  
]

@colored_subcommand_group(subcommand_sections=subcommand_sections)
def cli():
    pass

@cli.command(help="Check packages")
def check_pkgs():
    colored_echo("Check packages...")
    colored_echo("  Done.")

@cli.command(help="Install packages")
def install_pkgs():
    colored_echo("Install packages...")
    colored_echo("  Done.")

@cli.command(help="Make layer")
def make_layer():
    colored_echo("Make layer...")
    colored_echo("  Done.")

@cli.command(help="Check Layer")
def check_layer():
    colored_echo("Check layer...")
    colored_echo("  Done.")

@cli.command()
def echo_test():
    colored_echo("Install packages...")
    colored_echo("  Done.")
    colored_echo("Install packages2...", color="green")
    colored_echo("  Error!", color="red")

if __name__ == "__main__":
    cli()
