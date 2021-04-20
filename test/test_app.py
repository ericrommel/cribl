import json
import os
import pathlib
import subprocess
import time
import traceback

import docker

from .log import Log

AGENT = "agent"
EVENTS_LOG = "../events.log"
INPUT_FILE = "../agent/inputs/large_1M_events.log"
SPLITTER = "splitter"
TARGET = "target"
TARGET_1 = "target_1"
TARGET_2 = "target_2"

LOGGER = Log("cribl-app").get_logger(logger_name="app")


class TestApp:

    @classmethod
    def setup_class(cls):
        LOGGER.info(f"Starting class {cls.__name__} execution")

    @classmethod
    def teardown_class(cls):
        LOGGER.info(f"Ending class {cls.__name__} execution")

    def setup_method(self, method):
        LOGGER.info(f"Starting method {method.__name__} execution")
        self.client = self.get_client_docker()
        self.containers = self.create_app_containers(self.client)

    def teardown_method(self, method):
        LOGGER.info(f"Ending method {method.__name__} execution")

        self.delete_app_containers(self.client)
        self.delete_event_output()

    def test_event_log_output_has_been_created(self):
        LOGGER.info("Assert that events log file has been created")
        assert os.path.exists(EVENTS_LOG)

    def test_output_log_size_is_equal_to_input_log_size(self):
        LOGGER.info("Assert that the output log file size is equal to the input log file size")
        time.sleep(3)  # Wait a bit in order to process the output log completion
        assert self.get_number_of_lines(EVENTS_LOG) == self.get_number_of_lines(INPUT_FILE)

    def test_create_containers(self):
        LOGGER.info(f"Assert that test create containers")
        assert AGENT in self.containers
        assert SPLITTER in self.containers
        assert TARGET_1 in self.containers
        assert TARGET_2 in self.containers

    def test_delete_containers(self):
        LOGGER.info(self.delete_app_containers(self.client))
        LOGGER.info(f"Assert that test delete containers")
        assert self.client.containers.list() == []

    def test_splitter_config_files_is_a_valid_json(self):
        files = pathlib.Path().glob(f"../{SPLITTER}/*.json")
        for file in files:
            LOGGER.info(file)
            assert self.is_valid_json(open(file, "r").read())

    def test_splitter_ran_correctly(self):
        LOGGER.info(f"Assert that test splitter ran correctly")
        splitter_working = f"working as {SPLITTER}"
        assert splitter_working in self.get_logs(container=SPLITTER, client=self.client).lower()

    def test_target_config_files_is_a_valid_json(self):
        files = pathlib.Path().glob(f"../{TARGET}/*.json")
        for file in files:
            LOGGER.info(file)
            assert self.is_valid_json(open(file, "r").read())

    def test_targests_ran_correctly(self):
        LOGGER.info(f"Assert that test targets ran correctly")
        target_working = f"working as {TARGET}"
        assert target_working in self.get_logs(container=TARGET_1, client=self.client).lower()
        assert target_working in self.get_logs(container=TARGET_2, client=self.client).lower()

    def test_agent_config_files_is_a_valid_json(self):
        files = pathlib.Path().glob(f"../{AGENT}/*.json")
        for file in files:
            LOGGER.info(file)
            assert self.is_valid_json(open(file, "r").read())

    def test_agent_ran_correctly(self):
        LOGGER.info(f"Assert that test agent ran correctly")
        agent_working = f"working as {AGENT}"
        assert agent_working in self.get_logs(container=AGENT, client=self.client).lower()

    def log_traceback(self, ex: Exception) -> None:
        lines = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
        txt = "".join(lines)
        LOGGER.error(txt)

    def execute_command_line(self, cmd: str):
        LOGGER.info(f"Executing command: {cmd}")
        try:
            return subprocess.check_output(cmd, stderr=subprocess.PIPE, shell=True).decode()
        except subprocess.CalledProcessError as error:
            return f"CalledProcessError (code: {error.returncode}): {error.stderr.decode()}"
        except subprocess.TimeoutExpired as error:
            return f"TimeoutExpired: {error.stderr.decode()}"
        except Exception as error:
            self.log_traceback(error)

    def create_app_containers(self, client) -> list:
        LOGGER.info("Create containers")
        containers = []
        self.execute_command_line("docker-compose up -d")
        for c in client.containers.list():
            containers.append(c.name)
        return containers

    def get_logs(self, container: str, client) -> str:
        LOGGER.info(f"Get logs from {container}")
        for c in client.containers.list():
            if c.name.lower() == container.lower():
                return c.logs().decode("utf-8")
        return ""

    def get_containers_name(self, client: docker) -> list:
        LOGGER.info("Get container names")
        names = []
        for c in client.containers.list():
            names.append(c.name)

        return names

    def delete_app_containers(self, client: docker):
        LOGGER.info("Delete containers. First, stop them")
        for c in client.containers.list():
            LOGGER.info(f"Stopping {c.name} container")
            c.stop()
        LOGGER.info("Now, prune them")
        return client.containers.prune()

    def get_services(self):
        return self.client.services.list()

    def get_client_docker(self):
        return docker.from_env()

    def is_valid_json(self, a_json):
        try:
            LOGGER.info(f"Read a json:\n{json.loads(a_json)}")
        except ValueError as error:
            LOGGER.error(error)
            return False

        return True

    def delete_event_output(self):
        if os.path.exists(EVENTS_LOG):
            os.remove(EVENTS_LOG)
        else:
            LOGGER.info("The events.log file does not exist")

    def get_number_of_lines(self, file):
        file = open(file, "r")
        nonempty_lines = [line.strip("\n") for line in file if line != "\n"]
        file.close()
        return len(nonempty_lines)
