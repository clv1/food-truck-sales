# Pipeline

This folder should contain all code and resources required for the pipeline.

You'll write a lot of code in this week, doing a lot of different-but-related tasks. By the end of the week, you should have created the following:

- An extract Python script which downloads relevant files from S3.
- A transform Python script which combines the downloaded files, producing a single transaction data file.
- A notebook which reads from the transaction data file, exploring and visualising the data.
- A database creation SQL script that connects to the cloud, creates all tables, and seeds the database with initial data.
- An ETL pipeline task that runs on the cloud, extracting transaction data from S3 uploading it to the database.
- A locally-running dashboard service that reads from the cloud database.
  Crucially, although some of these artefacts will depend on the outputs of others, each script/task/notebook should run independently; building each one as a distinct element makes them more testable, more flexible, and more maintainable.
