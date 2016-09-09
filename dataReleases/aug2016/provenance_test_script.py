#Testing provenance in PsychENCODE data using Neo4j
#The script currently outputs a user defined csv file with information on the name of the bam file,
#along with the names and number of the fastq files it maps to for a given project inputted as 
#an argument. 

import argparse
import json
import pandas as pd
from py2neo import Graph, authenticate

# Build query
query = """
MATCH (a {{fileType:"{0}", parentId:"{1}"}})-[r]-(s)-[t]->(fq {{fileType:"{2}"}}) WHERE a.projectId="{3}"
   RETURN a.name, collect(distinct fq.name), count(distinct fq.name)
"""

def queryGraphDB(filename, filetypeA, parentId, filetypeB, projectId, graph):
    global query
    query = query.format(filetypeA, parentId, filetypeB, projectId)
    print 'Printing formatted query'
    print query
    print 'Sending query'

    # Send Cypher query
    df = pd.DataFrame(graph.run(query).data())
    df.to_csv(str(filename))
    print 'Done.'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
                'Please input the projectId to generate a csv relating to provenance')
    parser.add_argument('file', nargs='?', help='Input the filename to write results to')
    parser.add_argument('--fileType1', nargs='?', default='bam', help='Input the main file type for which provenance is being checked without period e.g. bam')
    parser.add_argument('--parent', nargs='?', default='syn7105852', help='Input parentId identifying folder of first file type')
    parser.add_argument('--fileType2', nargs='?', default='fastq', help='Input the secondary file type for which provenance is being checked against without period e.g. fastq')
    parser.add_argument('--project', nargs='?', help='Input the projectId in the following format #######.0: Default is PsychENCODE')
    args = parser.parse_args()

    # Connect to graph
    print 'Connecting to Neo4j and authenticating user credentials'
    with open('credentials.json') as json_file:
        db_info=json.load(json_file)
    authenticate(db_info['machine'], db_info['username'], db_info['password'])
    db_dir = db_info['machine'] + "/db/data"
    print db_dir
    graph = Graph(db_dir) #can remove db_dir if localhost

    filename = args.file
    filetypeA = args.fileType1
    parentId = args.parent
    filetypeB = args.fileType2
    if args.project:
        projId = args.project
    else:
        projId = str(4921369.0)
    
    try:
        queryGraphDB(filename, filetypeA, parentId, filetypeB, projId, graph)
    except:
        print 'Error involving transaction with Neo4j database'
        raise
