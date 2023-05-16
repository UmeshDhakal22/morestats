#importing necessary libraries
import osmium #osmium to handle the OSM data
import pandas as pd  
from collections import defaultdict, Counter 
import json

#a simple OsmHandler class to handle the nodes
class OsmHandler(osmium.SimpleHandler):
  def __init__(self):
        super().__init__()
        self.nodes = defaultdict(set)

  def node(self, n):
        tags = {tag.k: tag.v for tag in n.tags}
        for k, v in tags.items():
            if k != 'created_by':
                self.nodes[k + '=' + v].add(n.id)


#read the corresponding data from the directory and assign to respective handlers
handler = OsmHandler()
reader1=osmium.io.Reader('initial.osm.pbf')
osmium.apply(reader1,handler)
handler2 = OsmHandler()
reader2=osmium.io.Reader('latest.osm.pbf')
osmium.apply(reader2,handler2)

#finding the tags that were added, removed and modified over the time 
added_tags = {tag: handler2.nodes[tag] for tag in handler2.nodes if tag not in handler.nodes}
removed_tags = {tag: handler.nodes[tag] for tag in handler.nodes if tag not in handler2.nodes}
modified_tags = {tag: (handler.nodes[tag], handler2.nodes[tag]) for tag in handler.nodes if tag in handler2.nodes and handler.nodes[tag] != handler2.nodes[tag]}

#special dictionaries 
added=Counter(added_tags)
removed=Counter(removed_tags)
modified=Counter(modified_tags)


#function to count the number of occurence of added keys
def return_count(mykey):
    if mykey in added.keys():
        try:
            return len(added[mykey])
        except:
            return 1 
    else:
        return 0 
    
add = {}
for key in added.keys():
    add[key] = return_count(key)

#function to count the number of occurence of removed keys
def retur_count(mykey):
    if mykey in removed.keys():
        try:
            return len(removed[mykey])
        except:
            return 1 
    else:
        return 0 

remove = {}

for key in removed.keys():
    remove[key] = retur_count(key)

#function to count the number of occurence of modified keys
def ret_count(mykey):
    if mykey in modified.keys():
        try:
            return len(modified[mykey])
        except:
            return 1 
    else:
        return 0 

mody = {}

for key in modified.keys():
    mody[key] = ret_count(key)

#chnaging the dictioaries into dataframe
df = pd.DataFrame([add, remove, mody], index=['add', 'remove', 'mody']).T

#giving name to the index column
df=df.rename_axis('keys')

#replacing NaN values with 0
df=df.fillna(0)

#creating new column called Total
df['Total']=df['add']+df['remove']+df['mody']

#assigning index column also as a column
df=df.reset_index()

#opening Json file and loding the list into data
with open('/home/umesh/Desktop/KLL/list.json', 'r') as json_file:
    data = json.load(json_file)

#searching if the keys in list is also in the dataframe
search = (df[df['keys'].isin(data)])

#changing float into integer
columns=['add','remove','mody','Total']
df[columns]=df[columns].astype(int)

#If the list has keys that are not in the dataframe then those keys will have all the values 0
missing_keys = pd.DataFrame({'keys': list(set(data).difference(set(search['keys']))),
                                'add': 0,
                                'remove': 0,
                                'mody': 0,
                                'Total': 0})
result_df = pd.concat([search, missing_keys])

#printing the result
print(result_df)
