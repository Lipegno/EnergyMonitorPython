import grequests, time
import json, threading
from PublishSubscriber.Subscriber import Subscriber

class DataSender(Subscriber):
    def __init__(self, collectionEventURL, collectionDataURL):
        self.EventCollectionUrl = collectionEventURL
        self.DataCollectionUrl = collectionDataURL
        self.buffer = []
        self.dataSendSemaphore = threading.Semaphore(value=0)

    def sendDataEvent(self,payload):
        """
        Function made to send events data when they are detected.
        :param payload:
        :return:
        """
        print("Going to send event data")
        headers = {'content-type': 'application/json'}
        req = grequests.post(self.EventCollectionUrl,data=json.dumps(payload),headers=headers)
        responses = grequests.map([req], exception_handler=self.requestException)

    def sendDataValues(self,payload):
        """
        Function made to send measured current and power values.
        :param payload:
        :return:
        """
        headers = {'content-type': 'application/json'}
        req = grequests.post(self.DataCollectionUrl,data=json.dumps(payload),headers=headers)
        responses = grequests.map([req], exception_handler=self.requestException)

    def requestException(self,request, exception):
        print("Unable to send data: " + str(exception))

    def update(self,data):
        print("Going to send power data")
        self.buffer.append(data)
        self.dataSendSemaphore.release()

"""
if __name__ == "__main__":
    url1 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.77:3000/api/json/plugs_events"
    url2 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.77:3000/api/json/continuous_measuring"
    object = dataSender(url1, url2)

    while True:
        print("Sending Data Events")
        object.sendDataEvent({'type': "on", 'timestamp': str(time.time())})
        #object.sendDataValues({'power':'1024', 'current':'10', 'timestamp': str(time.time())})
"""