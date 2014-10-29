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
        self.runtime_get = NaturalLanguage('get me more info about google.com')
        self.runtime_create = NaturalLanguage('create a record that points google.com to ec2-54-423-34-32-compute.amazonaws.com')
        self.runtime_delete = NaturalLanguage('delete web1.voice.us-east-1.steven.sh')
        self.runtime_change = NaturalLanguage('point 45.43.32.1 to steven.sh')

        self.runtime_get.get_action()
        self.runtime_get.get_objects()
        self.runtime_create.get_action()
        self.runtime_delete.get_objects()
        self.runtime_change.get_action()
        self.runtime_change.get_objects()

        self.get_result = self.runtime_get.get_operation()
        self.create_result = self.runtime_create.get_operation()
        self.delete_result = self.runtime_delete.get_operation()
        self.change_result = self.runtime_change.get_operation()
        
    def test_get(self):
        self.assertEquals(result['get'],'source:google.com')
    def tearDown(self):
        self = None
    
class Route53():
    
    def enable_connection(self,region):
        self.connection = boto.route53.connect_to_region(region) 
        
    def get_records(self,zone):
        return self.connection.get_records(zone)
    
    def get_zones(self):
        return self.connection.get_zones()

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
                self.action = 'change'
            elif word in self.action_defs['delete']:
                self.action = 'delete'
            elif word in self.action_defs['create']:
                self.action = 'create'
            elif word in self.action_defs['get']:
                self.action = 'get'
        self.operation = dict({self.action:[]})

    def get_objects(self):
        try:
            for word in self.raw:
                if re.match(self.ip_regex, word):
                    self.ip = word
                    per_word.remove(word)
                    self.operation[self.action].append('source:'+word)
                elif re.match(self.aws_regex, word):
                    self.aws = word
                    per_word.remove(word)
                    self.operation[self.action].append('source:'+word)
                elif re.match(self.web_regex, word):
                    self.web = word
                    per_word.remove(word)
                    self.operation[self.action].append('dest:'+word)
            return True
        except KeyError:
            return False

    def derive_meaning(self):
        if self.action == 'change':
            self.query="You want to change: " + self.web + " to point to " + self.ip + self.aws + "? (y/n)"
        if self.action == 'delete':
            self.query="You want to delete: " + self.web + "? (y/n)"
        if self.action =='create':
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
        while quit == False:
            nl = NaturalLanguage(raw_input('what do you wanna do? '))
            nl.get_action()
            nl.get_objects()
            quit = nl.derive_meaning()
        #r53 = Route53('us-east-1')
        #r53.enable_connection()
    
    if __name__ == '__main__':
        unittest.main(exit=False,verbosity=2)
        main()
