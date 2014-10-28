### route53 Manager ###
### sbrichards@mit.edu ###

import boto
import boto.route53
from boto.route53.record import ResourceRecordSets
import argparse

#Test Mocks
#class Tests(unittest.TestCase):
#    def setUp(self):
#        self.runtime = Main()
#        self.connection = self.runtime.get_connection()
#        self.records = self.runtime.get_records()
#    def test_get_instances(self):
#        self.assertEquals(,)
#    def tearDown(self):
#        self = None
    
class Route53():
    
    def enable_connection(self,region):
        self.connection = boto.route53.connect_to_region(region) 

    def disable_connection(self):
        self.connection = None
        
    def get_records(self,zone):
        return self.connection.get_records(zone)
    
    def get_zones(self):
        return self.connection.get_zones()
        
    def __init__(self):
        self
    
class Main():

    def main():
        r53 = Route53()
        r53.enable_connection('us-east-1')
        for zone in r53.get_zones():
            print zone.get_records()    
    
    if __name__ == '__main__':
        main()