FROM python:latest

WORKDIR /dashboard

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY database.py .
COPY dashboard.py .

RUN echo "Building the dashboard image."
CMD streamlit run dashboard.py