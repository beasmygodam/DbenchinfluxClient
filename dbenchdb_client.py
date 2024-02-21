import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDBConnection:
    def __init__(self, url, token, org, bucket):
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket
        self.client = influxdb_client.InfluxDBClient(url=self.url, token=self.token, org=self.org)
    
    def write_data(self, measurement, fields, tags=None):
        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        p = influxdb_client.Point(measurement).tag(**tags).field(**fields)
        write_api.write(self.bucket, self.org, p)
    
    def read_data(self, query):
        query_api = self.client.query_api()
        result = query_api.query(org=self.org, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_field(), record.get_value()))
        return results


