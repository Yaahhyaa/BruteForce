from py2neo import Graph, Node, Relationship

# Connect to the Neo4j database
graph = Graph("bolt://10.115.2.22:7687", auth=("neo4j", "Test123!"))

# Create nodes for motorcycle brands
brands = [
    Node("Brand", name="Harley-Davidson", country="USA"),
    Node("Brand", name="Ducati", country="Italy"),
    Node("Brand", name="BMW Motorrad", country="Germany"),
    Node("Brand", name="Yamaha", country="Japan"),
    Node("Brand", name="KTM", country="Austria"),
]

# Define relationships between brands
relationships = [
    Relationship(brands[0], "COLLABORATES_WITH", brands[2]),  # Harley-Davidson collaborates with BMW
    Relationship(brands[1], "LOVES", brands[4]),             # Ducati loves KTM
    Relationship(brands[3], "HATES", brands[0]),             # Yamaha hates Harley-Davidson
    Relationship(brands[4], "COLLABORATES_WITH", brands[3]), # KTM collaborates with Yamaha
    Relationship(brands[2], "RESPECTS", brands[1]),          # BMW respects Ducati
]

# Add nodes and relationships to the graph
for brand in brands:
    graph.create(brand)

for rel in relationships:
    graph.create(rel)

# Query the database to display relationships between brands
query = """
MATCH (b1:Brand)-[r]->(b2:Brand)
RETURN b1.name AS Brand1, type(r) AS Relationship, b2.name AS Brand2
"""

results = graph.run(query)
for record in results:
    print(f"Brand: {record['Brand1']} {record['Relationship']} {record['Brand2']}")
