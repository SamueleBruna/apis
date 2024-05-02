import typer
from typing_extensions import Annotated
from clients.model.table import Table
from clients.model.blob import Blob
from clients.bqfinder_v1 import BQFinder
from clients.gcsfinder_v1 import GCSFinder
from logger.logger import Logger

app = typer.Typer(name="gcpfinder", no_args_is_help=True, add_completion=False, pretty_exceptions_enable=False)
logger = Logger()

help_proj = "This Argument represents the name of the project in Bigquery"
help_dataset = "This Argument represents the name of the dataset in Bigquery"
help_table_name = "This Argument represents the name of the table in Bigquery"
help_bucket = "This Argument represents the name of the bucket in Google Cloud Storage"
help_path_to_blob = "This Argument represents the path to the blob inside a bucket in Google Cloud Storage"


# TODO: Composer client development
# TODO: Ask if raising an exception is better in main or in the Class implementation if found or not
# TODO: Create the complete Routine from BQ to GCS(finding the Composer Bucket + finding the source code) to Composer (Daginfos)

# add id needed callbacks for argument type https://typer.tiangolo.com/tutorial/options/callback-and-context/
@app.command()
def bqfinder(
        project: Annotated[str, typer.Option("--project", "-pr", help=help_proj)] = None,
        dataset: Annotated[str, typer.Option("--dataset", "-d", help=help_dataset)] = None,
        table_name: Annotated[str, typer.Option("--table", "-t", help=help_table_name)] = None
):
    """
    Prints if a Table exists inside a project in Bigquery
    """
    if all(v is not None for v in [project, dataset, table_name]):
        # Creating the Table object
        table: Table = Table(project=project, dataset=dataset, table_name=table_name)
        # Creating the Client using BQFinder and the target
        bq_find: BQFinder = BQFinder(target=table)
    else:
        # Creating the Client using BQFinder without a target (It will be asked in input later in the constructor)
        bq_find: BQFinder = BQFinder()

    table_exists: bool = bq_find.find()
    if table_exists:
        typer.echo(f"The table {bq_find.target.project}:{bq_find.target.dataset}.{bq_find.target.table_name} exists!")
    else:
        typer.echo(f"The table {bq_find.target.project}:{bq_find.target.dataset}.{bq_find.target.table_name} doesn't "
                   f"exists!")


@app.command()
def gcsfinder(
        project: Annotated[str, typer.Option("--project", "-pr", help=help_proj)] = None,
        bucket: Annotated[str, typer.Option("--bucket", "-b", help=help_bucket)] = None,
        path_to_blob: Annotated[str, typer.Option("--path", "-pt", help=help_path_to_blob)] = None
):
    """
    Prints if a Blob exists and if Logger level is set to INFO, even some additional information
    """
    if all(v is not None for v in [project, bucket, path_to_blob]):
        # Creating the Table object
        blob: Blob = Blob(project=project, bucket=bucket, path=path_to_blob)
        # Creating the Client using GCSFinder
        gcs_find: GCSFinder = GCSFinder(target=blob, logger=logger)
    else:
        # Creating the Client using GCSFinder without a target (It will be asked in input later in the constructor)
        gcs_find: GCSFinder = GCSFinder(logger=logger)

    blob_exists: bool = gcs_find.find()
    if blob_exists:
        typer.echo(f"The table {gcs_find.target.project}:{gcs_find.target.bucket}/{gcs_find.target.path} exists!")


if __name__ == "__main__":
    app()
