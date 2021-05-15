FROM prefecthq/prefect:0.14.16


COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT prefect agent local start -t $TOKEN -l github-flows
