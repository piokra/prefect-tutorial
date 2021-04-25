import prefect
from prefect import task, Flow, Parameter
from prefect.storage import GitHub

@task
def say_hello(name):
    logger = prefect.context.get("logger")
    logger.info(f"Hello, {name}!")

with Flow("hello-flow") as flow:
    # An optional parameter "people", with a default list of names
    people = Parameter("people", default=["Arthur", "Ford", "Marvin", "Arti", "Wheezy"])
    # Map `say_hello` across the list of names
    say_hello.map(people)

# Register the flow under the "tutorial" project


flow.storage = GitHub(
    repo="piokra/prefect-tutorial",
    path="hello-flow.py"
)

