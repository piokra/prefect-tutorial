from prefecthq/prefect:0.14.16

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT prefect agent local start -t $TOKEN -l github-flows
