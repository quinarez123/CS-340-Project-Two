import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import json



# Created the AnimalShelter classs. This class will have all the methods pertaining
# to CRUD when communicating with the animals database
class AnimalShelter(object):
   
 # The following are variabled that will be used to communicate with the databse   
    def __init__(self, USER, PASS):
        self.USER = USER
        self.PASS = PASS
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 34353
        DB = 'AAC'
        COL = 'animals'
        
# The following statements are also used to communicate with the database by replacing
# the special characters with the variables along with the personalized values specific
# to me
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]
        

# The create method takes a dictionary type and used the insert_one() method to insert it
# into the animals collection
    def create(self, data):
        if data is not None:
            self.database.animals.insert_one(data)
        else:
            raise Exception("Nothing to save, because data parameter is empty")
        
# The read method takes a query dictionary type ,(key:value) pair, and uses the find()
# method using the argument to find a list of matching queries. Once a list is retrieved then
# I use the animal variable to iterate through the cursor in order to print the entry, one
# at a time. If you only use {} as the query then it'll print out all the entries
    def read(self, query):
        animal_list = []
# Follwoing variable is used to count the # of records found and prints it
        records_count = self.database.animals.count_documents(query)
        print("Records found: ", records_count)
        print()
        cursor = self.database.animals.find(query)
        for animal in cursor:
            animal_list.append(animal)
            
        return animal_list
            
                
# The update method takes two argument, the first is the query that you want to update, and 
# the second is the value you want to replace it with
    def update(self, query_filter, update_operation):
# variable that will be used to display # of entries updated
        documents_modified = 0

        if query_filter is not None:
# records_count is used to count the # of documents updated
            records_count = self.database.animals.count_documents(query_filter)
# Compares the records_count value and compares to see if there isn't any matching entries
# then prints a statement
            if (records_count == 0):
                print("Sorry, couldn't find a matching entry")
# Else if one matching document found then it'll update it
            elif (records_count == 1):
                result = self.database.animals.update_one(query_filter, update_operation)
                documents_modified = result.modified_count
# Second else if statement that'll change multiples documents
            elif (records_count > 1):
                result= self.database.animals.update_many(query_filter, update_operation)
                documents_modified = result.modified_count
                  
            print(documents_modified, " documents modified")
                
# Delete method that takes a query argument. Works similar to the update method but using
# delete_one() and delete_many() methods instead
    def delete(self, query_filter):
        documents_deleted = 0
        
        if query_filter is not None:
            records_count = self.database.animals.count_documents(query_filter)
            if (records_count == 0):
                print("Sorry, couldn't find a matching entry")
            elif (records_count == 1):
                result = self.database.animals.delete_one(query_filter)
                documents_deleted = result.deleted_count
            elif (records_count > 1):
                result = self.database.animals.delete_many(query_filter)
                documents_deleted = result.deleted_count
                
            print(documents_deleted, " documents deleted")