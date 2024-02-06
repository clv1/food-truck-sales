FROM python:latest

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir latest_batch_data

COPY extract.py .
COPY transform.py .
COPY load.py .
COPY pipeline.py .

RUN echo "Building the pipeline image."  # This will execute during `docker build`
CMD python3 pipeline.py