class RunBackgroundTasks():
    is_running_as_server = False

    def runtask(self):
        """
        this method ingest the data in a async call
        """
        from app.tasks import run_mqtt_server
        run_mqtt_server.delay()
