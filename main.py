### route53 Manager ###
### sbrichards@mit.edu ###

import boto
import boto.route53
import re
from boto.route53.record import ResourceRecordSets
import argparse
import unittest

#Test Mocks
class Tests(unittest.TestCase):
    def setUp(self):
        
        #self.runtime_delete = NaturalLanguage('delete web1.voice.us-east-1.steven.sh')
        #self.runtime_change = NaturalLanguage('point 45.43.32.1 to steven.sh')

        #self.runtime_get.get_action()
        #self.runtime_get.get_objects()
        #self.runtime_create.get_action()
        #self.runtime_delete.get_objects()
        #self.runtime_change.get_action()
        #self.runtime_change.get_objects()

        #self.get_result = self.runtime_get.get_operation()
        #self.create_result = self.runtime_create.get_operation()
        #self.delete_result = self.runtime_delete.get_operation()
        #self.change_result = self.runtime_change.get_operation()
        self
    def test_get(self):
        self.runtime = NaturalLanguage('get me more info about google.com')
        self.runtime.get_action()
        self.runtime.get_objects()
        self.result = self.runtime.get_operation()
        self.assertEquals(self.result['parameters']['source'],'google.com')    
    def test_create(self):
        self.runtime = NaturalLanguage('create a record that points google.com to ec2-54-423-34-32-compute.amazonaws.com')
        self.runtime.get_action()
        self.runtime.get_objects()
        self.result = self.runtime.get_operation()
        self.assertEquals(self.result['parameters']['dest'],'ec2-54-423-34-32-compute.amazonaws.com')
        self.assertEquals(self.result['parameters']['source'],'google.com')
    def test_delete(self):
        self.runtime = NaturalLanguage('delete web1.voice.us-east-1.steven.sh')
        self.runtime.get_action()
        self.runtime.get_objects()
        self.result = self.runtime.get_operation()
        self.assertEquals(self.result['parameters']['source'],'web1.voice.us-east-1.steven.sh')
    def test_change(self):
        self.runtime = NaturalLanguage('point 45.43.32.1 to steven.sh')
        self.runtime.get_action()
        self.runtime.get_objects()
        self.result = self.runtime.get_operation()
        self.assertEquals(self.result['parameters']['dest'],'45.43.32.1')
        self.assertEquals(self.result['parameters']['source'],'steven.sh')
    def tearDown(self):
        self = None
    
class Route53():
    
    def enable_connection(self):
        self.connection = boto.route53.connect_to_region(self.region) 
        
    def get_records(self,zone):
        return self.connection.get_records(zone)
    
    def get_zones(self):
        return self.connection.get_zones()

    def get_zone_by_name(self,name):
        return self.connection.get_zone(name)

    def cleanup(self):
        self = None
        
    def __init__(self, region):
        self
        self.region = region
    
class NaturalLanguage():
    
    def get_operation(self):
        return self.operation

    def get_action(self):
        for word in self.raw:
            if word in self.action_defs['change']:
                self.action = 'UPSERT'
            elif word in self.action_defs['delete']:
                self.action = 'DELETE'
            elif word in self.action_defs['create']:
                self.action = 'CREATE'
            elif word in self.action_defs['get']:
                self.action = 'get'
        self.operation = dict({ 'action':self.action,
                                'parameters':{}
                                })

    def get_objects(self):
        try:
            for word in self.raw:
                if re.match(self.ip_regex, word):
                    self.ip = word
                    self.raw.remove(word)
                    self.operation['parameters']['dest'] = word
                    self.operation['parameters']['type'] = 'A'
                elif re.match(self.aws_regex, word):
                    self.aws = word
                    self.raw.remove(word)
                    self.operation['parameters']['dest'] = word
                    self.operation['parameters']['type'] = 'CNAME'
                elif re.match(self.web_regex, word):
                    self.web = word
                    self.raw.remove(word)
                    self.operation['parameters']['source'] = word
            return True
        except KeyError:
            return False

    def derive_meaning(self):
        if self.action == 'UPSERT':
            self.query="You want to change: " + self.web + " to point to " + self.ip + self.aws + "? (y/n)"
        if self.action == 'DELETE':
            self.query="You want to delete: " + self.web + "? (y/n)"
        if self.action =='CREATE':
            self.query="You want to point: " + self.web + " to " + self.ip + self.aws +"? (y/n)"
        if self.action =='get':
            self.query="You want to get more info about: " + self.web + self.aws + "? (y/n)"
        self.response = raw_input(self.query)
        if self.response.lower() in ['yes', 'y', 'yay', 'ya', 'yea']:
            print "Affirmative " 
            print self.operation
            return False
        else:
            print "quitting"
            return True

    def __init__(self, input):
        self

        self.action_defs = dict({
            'get':['get', 'retrieve', 'pull'],
            'change':['point', 'change', 'modify', 'upsert', 'update'],
            'delete':['delete', 'destroy', 'remove'],
            'create':['create', 'add', 'define']})

        self.ip_regex = '[0-9]+(?:\.[0-9]+){3}'
        self.web_regex = '^([a-z0-9][a-z0-9\-]*\.)+[a-z0-9][a-z0-9\-]*$'
        self.aws_regex = 'ec2.+[0-9].+.amazonaws.com'

        self.raw = str(input).split(" ")
        self.ip=self.aws=self.web=self.action=self.query=self.operations= ''

class Main():

    def main():
        quit = False
        r53 = Route53('us-east-1')
        r53.enable_connection()
        while quit == False:
            user_input = raw_input('sup? ')
            nl = NaturalLanguage(user_input)
            nl.get_action()
            nl.get_objects()
            quit = nl.derive_meaning()
            if quit == True:
                exit()
            zone = r53.get_zone_by_name(nl.operation['parameters']['source'])
            if zone == None:
                zones = r53.connection.get_all_hosted_zones()
                for z in zones['ListHostedZonesResponse']['HostedZones']:
                    if str(z['Name']) in nl.operation['parameters']['source']+'.':
                        zone = z
            
            if nl.operation['action'] == 'CREATE':
                zone.add_record(nl.operation['parameters']['type'], nl.operation['parameters']['source'], nl.operation['parameters']['dest'])
            if nl.operation['action'] == 'UPSERT':
                zone.update_record(nl.operation['parameters']['type'], nl.operation['parameters']['source'], nl.operation['parameters']['dest'])
            print zone

    if __name__ == '__main__':
        unittest.main(exit=False,verbosity=2)
        main()
