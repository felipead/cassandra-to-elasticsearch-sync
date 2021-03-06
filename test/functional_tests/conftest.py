from multiprocessing import Process
from uuid import uuid4

import pytest

from app.application import Application
from app.elasticsearch_domain.store.abstract_elasticsearch_store import MATCH_ALL_QUERY


def wipe_databases(cassandra_log_entry_store, elasticsearch_client):
    cassandra_log_entry_store.delete_all()
    elasticsearch_client.delete_by_query(index="_all", body=MATCH_ALL_QUERY)


@pytest.fixture(scope="session")
def application_instance(settings):
    return Application(settings)


@pytest.fixture(scope="function")
def state_filename(tmpdir):
    random_filename = str(uuid4()) + ".yaml"
    return str(tmpdir.join(random_filename))


@pytest.fixture(scope="session")
def sync_interval_time(settings):
    return settings.interval_between_runs * 5


# noinspection PyShadowingNames
@pytest.fixture(scope="function", autouse=True)
def setup_test(request, application_instance, state_filename, cassandra_log_entry_store, elasticsearch_client):
    wipe_databases(cassandra_log_entry_store, elasticsearch_client)

    def run_application():
        application_instance.run(state_filename)
    process = Process(target=run_application)
    process.start()

    def on_teardown():
        if process.is_alive():
            process.terminate()
    request.addfinalizer(on_teardown)
