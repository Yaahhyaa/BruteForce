from py2neo import Graph
graph = Graph("bolt://10.115.2.22:7687", auth=("neo4j", "Test123!"))

nodes = graph.run("Match (n) Return n LIMIT 10").data()
for node in nodes:
    print(node)
