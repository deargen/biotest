# ruff: noqa: T201
import typer

app = typer.Typer(
    no_args_is_help=True, context_settings={"help_option_names": ["-h", "--help"]}
)


def version_callback(*, value: bool):
    if value:
        from .. import __version__

        print(__version__)
        raise typer.Exit


@app.callback()
def common(
    ctx: typer.Context,
    *,
    version: bool = typer.Option(
        None, "-v", "--version", callback=version_callback, help="Show version"
    ),
):
    pass


@app.command()
def health():
    from ..health import main as health_main
    from ..utils.log import setup_logging

    setup_logging(output_files=[], file_levels=[])
    health_main()


def main():
    app()


if __name__ == "__main__":
    main()
