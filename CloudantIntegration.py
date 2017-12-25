from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

client = Cloudant("fbf0db35-7ef0-4ccb-8029-07c43932e4bb-bluemix", "52a8bfd2afeffbd91c379f8b8cc09c6335a4be79b5c3dc1989aa8aa0fad30ad1", url="https://fbf0db35-7ef0-4ccb-8029-07c43932e4bb-bluemix:52a8bfd2afeffbd91c379f8b8cc09c6335a4be79b5c3dc1989aa8aa0fad30ad1@fbf0db35-7ef0-4ccb-8029-07c43932e4bb-bluemix.cloudant.com")
client.connect()
# my_database = client['iotp_6hufwa_default_2017-12-06']
my_database = client['iotp_6hufwa_default_2017-12-08']
sum = 0
i = 0
for document in my_database:
    print(document)
    print("Reading from master ESP received from cloudant DB is : " + str(document['data']['d']['readingFromMaster']))
    print('\n')
    i = i+1
    sum = sum + int(document['data']['d']['readingFromMaster'])

avg = sum/i
print("The avg of all this data is : " + str(avg) + " for " + str(i) + " records")
