import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDBConnection:
    def __init__(self, url, token, org, bucket):
        """
        Initializes the InfluxDBConnection object.

        Parameters:
        - url (str): The URL of the InfluxDB instance.
        - token (str): Authentication token for accessing the InfluxDB instance.
        - org (str): Organization name.
        - bucket (str): Bucket name to write and read data from.

        Returns:
        None
        """
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket
        self.client = influxdb_client.InfluxDBClient(url=self.url, token=self.token, org=self.org)
    
    def write_data(self, measurement, fields, tags=None):
        """
        Writes data points to the specified measurement in the InfluxDB.

        Parameters:
        - measurement (str): The measurement name.
        - fields (dict): Dictionary containing field names and values for the data point.
        - tags (dict, optional): Dictionary containing tag names and values for the data point. Default is None.

        Returns:
        None
        """
        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        p = influxdb_client.Point(measurement).tag(**tags).field(**fields)
        write_api.write(self.bucket, self.org, p)
    
    def read_data(self, query):
        """
        Reads data from the InfluxDB based on the specified query.

        Parameters:
        - query (str): InfluxDB query to execute.

        Returns:
        list: A list of tuples containing field names and their corresponding values.
        """
        query_api = self.client.query_api()
        result = query_api.query(org=self.org, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_field(), record.get_value()))
        return results


