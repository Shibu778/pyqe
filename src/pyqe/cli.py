import click
from pyqe.utils import xml2json, xml2laststruct  # Replace with actual function names
from pyqe.defaults import ASE_FORMATS

@click.group()
def cli():
    """Command-line interface for utils.py functions."""
    pass

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('filename', type=str)
@click.option('--pbc/--no-pbc', default=True, help="Periodic boundary conditions (default: True)")
@click.option('--constrain/--no-constrain', default=False, help="Apply constraints (default: False)")
@click.option('--format', type=click.Choice(ASE_FORMATS, case_sensitive=False), default="vasp", show_default=True, help="Output file format")
def xml2laststruct_cmd(input_file, filename, pbc, constrain, format):
    """
    Convert XML to last structure and save as POSCAR.

    INPUT_FILE: Input XML file generated from pw.x calculation (prefix.xml)
    FILENAME: Output Structure filename to store the last structure
    """
    xml2laststruct(input_file, filename, pbc=pbc, constrain=constrain)
    click.echo(f"Saved last structure from {input_file} to {filename} (pbc={pbc}, constrain={constrain})")

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=str)
@click.option('--save/--no-save', default=False, help="Save the JSON output to file (default: False)")
def xml2json_cmd(input_file, output_file, save):
    """
    Convert XML to JSON.

    INPUT_FILE: Path to the input XML file
    OUTPUT_FILE: Path to output JSON file (used if --save is set)
    """
    xml2json(input_file, output_file, save=save)
    if save:
        click.echo(f"Converted {input_file} to {output_file} (JSON saved)")
    else:
        click.echo(f"Converted {input_file} to JSON (not saved to file)")


if __name__ == "__main__":
    cli()
