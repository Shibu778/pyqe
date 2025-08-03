import click
from pyqe.utils import xml2json, xml2laststruct  # Replace with actual function names
from pyqe.defaults import ASE_FORMATS
from pyqe.utils import conv_structure
import os
from pyqe.input import qe_input
import yaml


@click.group()
def cli():
    """Command-line interface for utils.py functions."""
    pass


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("filename", type=str)
@click.option(
    "--pbc/--no-pbc", default=True, help="Periodic boundary conditions (default: True)"
)
@click.option(
    "--constrain/--no-constrain",
    default=False,
    help="Apply constraints (default: False)",
)
@click.option(
    "--format",
    type=click.Choice(ASE_FORMATS, case_sensitive=False),
    default="vasp",
    show_default=True,
    help="Output file format",
)
def xml2laststruct_cmd(input_file, filename, pbc, constrain, format):
    """
    Convert XML to last structure and save as POSCAR.

    INPUT_FILE: Input XML file generated from pw.x calculation (prefix.xml)
    FILENAME: Output Structure filename to store the last structure
    """
    xml2laststruct(input_file, filename, pbc=pbc, constrain=constrain, format=format)
    click.echo(
        f"Saved last structure from {input_file} to {filename} (pbc={pbc}, constrain={constrain})"
    )


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=str)
@click.option(
    "--save/--no-save",
    default=False,
    help="Save the JSON output to file (default: False)",
)
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


@cli.command("conv")  # Abbreviated command name
@click.argument("infile", type=click.Path(exists=True))  # Abbreviated argument
@click.argument("outfile", type=str)
@click.option(
    "-if",
    "--in-fmt",
    type=click.Choice(ASE_FORMATS, case_sensitive=False),
    required=True,
    help="Input file format",
)
@click.option(
    "-of",
    "--out-fmt",
    type=click.Choice(ASE_FORMATS, case_sensitive=False),
    required=True,
    help="Output file format",
)
@click.option(
    "-ow",
    "--overwrite/--no-overwrite",
    default=False,
    help="Overwrite output file if exists",
)
def conv_cmd(infile, outfile, in_fmt, out_fmt, overwrite):
    """
    Convert structure file between formats.

    INFILE: Input structure file
    OUTFILE: Output structure file
    """
    if os.path.exists(outfile) and not overwrite:
        click.echo(
            f"Error: {outfile} already exists. Use -ow/--overwrite to overwrite.",
            err=True,
        )
        return
    conv_structure(
        infile,
        outfile,
        inp_format=in_fmt,
        out_format=out_fmt,
        overwrite=overwrite,
    )
    click.echo(f"Converted {infile} ({in_fmt}) to {outfile} ({out_fmt})")


@cli.command("genpw")
@click.argument("structure", type=click.Path(exists=True))
@click.argument("input_yaml", type=click.Path(exists=True))
@click.argument("output", type=str, default="pw.in")
def genpw_cmd(structure, input_yaml, output):
    """
    Generate Quantum ESPRESSO input from VASP POSCAR and YAML input file.

    STRUCTURE: Path to Structure file
    INPUT_YAML: Path to YAML file with QE input parameters
    OUTPUT: Output QE input filename (default: pw.in)
    """
    from pyqe.input import qe_input

    with open(input_yaml, "r") as f:
        input_dict = yaml.safe_load(f)

    input_data = input_dict.get("input", input_dict)
    kpts = input_dict.get("kpts", None)
    inp = qe_input(structure, input_data, kpts=kpts)
    inp.write_input(output)
    click.echo(f"QE input written to {output} using {structure} and {input_yaml}")


if __name__ == "__main__":
    cli()
