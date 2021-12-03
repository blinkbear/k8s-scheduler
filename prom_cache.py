# collect prometheus information and cache it
import pandas as pd
from prometheus_api_client import PrometheusConnect

class Cache(object):
    def __init__(self):
        self.cacheData = pd.DataFrame(
            columns=['timestamp', 'instance', 'pod_name',
                     'container_name', 'type', 'window', 'value']
        )

    def addNewItem(self, item):
        self.cacheData = self.cacheData.append(item, ignore_index=True)

    def queryItemByTimestampAndTypeAndWindow(self, item, timestamp, type, window):
        data = self.cacheData[(self.cacheData['timestamp'] == timestamp) & (
            self.cacheData['type'] == type) & (self.cacheData['window'] == window)]
        data.sort_values(by=['timestamp'], inplace=True)
        return data

    def queryItemByTimestampRangeAndTypeAndWindow(self, timestamp_start, timestamp_end, type, window):
        data = self.cacheData[(self.cacheData['timestamp'] >= timestamp_start) & (
            self.cacheData['timestamp'] <= timestamp_end) & (self.cacheData['type'] == type) & (self.cacheData['window'] == window)]
        data.sort_values(by=['timestamp'], inplace=True)
        return data

    def queryItemByPodNameAndTypeAndWindow(self, pod_name, type, window):
        data = self.cacheData[(self.cacheData['pod_name'] == pod_name) & (
            self.cacheData['type'] == type) & (self.cacheData['window'] == window)]
        data.groupby('pod_name').apply(
            lambda t: t[t.value == t.value.max()]).reset_index(drop=True)
        data.sort_values(by=['timestamp'], inplace=True)
        return data

    def queryItemByPodNameAndQueryRangeAndTypeAndWindow(self, pod_name, timestamp_start, timestamp_end, type, window):
        data = self.cacheData[(self.cacheData['pod_name'] == pod_name) & (self.cacheData['timestamp'] >= timestamp_start) & (
            self.cacheData['timestamp'] <= timestamp_end) & (self.cacheData['type'] == type) & (self.cacheData['window'] == window)]
        data.groupby('pod_name').apply(
            lambda t: t[t.value == t.value.max()]).reset_index(drop=True)
        data.sort_values(by=['timestamp'], inplace=True)
        return data

    def queryItemByContainerNameAndQueryRangeAndTypeAndWindow(self, container_name, timestamp_start, timestamp_end, type, window):
        data = self.cacheData[(self.cacheData['container_name'] == container_name) & (self.cacheData['timestamp'] >= timestamp_start) & (
            self.cacheData['timestamp'] <= timestamp_end) & (self.cacheData['type'] == type) & (self.cacheData['window'] == window)]
        data.sort_values(by=['timestamp'], inplace=True)
        return data


class PromQuery(object):

    def __init__(self, prom_url, prom_port):
        self.prom_url = prom_url
        self.prom_port = prom_port
        self.prom = PrometheusConnect(prom_url, prom_port)

    def query():
        pass

        

