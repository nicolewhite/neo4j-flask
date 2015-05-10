from .models import graph

nodes = [
    ('User', 'username'),
    ('Post', 'id'),
    ('Tag', 'name')
]

for label, property in nodes:
    try:
        graph.schema.create_uniqueness_constraint(label, property)
    except:
        continue