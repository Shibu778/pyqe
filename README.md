# pyqe
Python library to help do calculations in quantum espresso.


## Help

The `pyqe` package provides command-line utilities and Python functions for pre- and post-processing Quantum ESPRESSO calculations.

To see available commands and options, run:

```sh
pyqe --help
```

For help on a specific command, use:

```sh
pyqe <command> --help
```

Example:

```sh
pyqe xml2json-cmd --help
```

You can also use the Python API by importing functions from the `pyqe` package in your scripts.

## Setting Up config.yaml

The `config.yaml` file stores paths and settings used by `pyqe`. It should be placed in the project root directory.

Example `config.yaml`:

```yaml
paths:
  pseudo_dir: "/path/to/your/pseudopotentials"
  output_dir: "./output/"
```

- `pseudo_dir`: Path to your Quantum ESPRESSO pseudopotential files.
- `output_dir`: Directory where output files will be saved.

Edit these paths to match your local environment before running calculations.