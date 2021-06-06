import requests


class AirflowEndPoints:
    TRIGGER_DAG = '{base_url}/api/experimental/dags/{dag_id}/dag_runs'


class AirflowRestClient:

    def __init__(
        self,
        base_url: str
    ):
        self.base_url = base_url

    def trigger_dag(self, dag_id: str, params: dict):
        url = AirflowEndPoints.TRIGGER_DAG.format(
            base_url=self.base_url,
            dag_id=dag_id
        )
        print('triggering dag: ', url)



        response = requests.post(
            url=url,
            headers={
                'Cache-Control': 'no-cache',
                'Content-Type': 'application/json'
            },
            json={'conf': params}
        )
        print(response.status_code)
        # print(response.status_code, response.json())
