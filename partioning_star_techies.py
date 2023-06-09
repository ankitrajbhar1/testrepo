# -*- coding: utf-8 -*-
"""partioning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1h0rQjTSVHAOqmRhhHTbrPryPuWAsnOJX

Group: Star Techies
Problem statement 1: partioning
"""

!pip install fpgrowth

# Commented out IPython magic to ensure Python compatibility.
# %pip install mlxtend --upgrade

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx

from google.colab import files
uploaded = files.upload()

dataset = pd.read_csv('DataSetA.csv',error_bad_lines=False)
display(dataset.head())

num_partitions = 4

# Split dataset into partitions
partitions = np.array_split(dataset, num_partitions)

print(partitions)

len(dataset. index)

df2 = dataset.iloc[4362:]
print(df2)

len(df2. index)

# df2.itemDescription = df2.itemDescription.transform(lambda x: [x])
# df2 = df2.groupby(['Member_number','Date']).sum()['itemDescription'].reset_index(drop=True)

encoder = TransactionEncoder()
transactions = pd.DataFrame(encoder.fit(df2).transform(df2), columns=encoder.columns_)
display(transactions.head(23))

frequent_itemsets = apriori(transactions, min_support= 2/len(dataset), use_colnames=True, max_len = 2)
rules1 = association_rules(frequent_itemsets, metric="lift",  min_threshold = 1.5)
display(rules1.head(50))
print("Rules identified: ", len(rules1))

resultant = rules1[['antecedents', 'consequents' , 'support' , 'confidence' , 'lift' ]]
resultant

df3 = rules1.mean(axis=0)
print(df3)

resultant1 = resultant[resultant['confidence'] >=0.04]
resultant1

# Commented out IPython magic to ensure Python compatibility.
# %timeit apriori(transactions,min_support=0.4)

idx1 = pd.Index(resultant[['antecedents', 'consequents' , 'support' , 'confidence' , 'lift' ]])
idx2 = pd.Index(resultant1[['antecedents', 'consequents' , 'support' , 'confidence' , 'lift' ]])
(idx1.intersection(idx2))

df4 = dataset.iloc[5621:]
print(df4)

encoder = TransactionEncoder()
transactions = pd.DataFrame(encoder.fit(df4).transform(df4), columns=encoder.columns_)
display(transactions.head(23))

frequent_itemsets = apriori(transactions, min_support= 2/len(df4), use_colnames=True, max_len = 2)
rules = association_rules(frequent_itemsets, metric="lift",  min_threshold = 1.5)
display(rules.head(50))
print("Rules identified: ", len(rules))

sns.set(style = "whitegrid")
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection = '3d')


x = rules1['support']
y = rules1['confidence']
z = rules1['lift']

ax.set_xlabel("Support")
ax.set_ylabel("Confidence")
ax.set_zlabel("Lift")

ax.scatter(x, y, z)
ax.set_title("3D Distribution of Association Rules")

plt.show()

#Another type of visualizations to look at the relationship between the products is via Network Graph

def draw_network(rules, rules_to_show):
  # Directional Graph from NetworkX
  network = nx.DiGraph()
  
  # Loop through number of rules to show
  for i in range(rules_to_show):
    
    # Add a Rule Node
    network.add_nodes_from(["R"+str(i)])
    for antecedents in rules.iloc[i]['antecedents']: 
        # Add antecedent node and link to rule
        network.add_nodes_from([antecedents])
        network.add_edge(antecedents, "R"+str(i),  weight = 2)
      
    for consequents in rules.iloc[i]['consequents']:

        # Add consequent node and link to rule
        network.add_nodes_from([consequents])
        network.add_edge("R"+str(i), consequents,  weight = 2)

  color_map=[]  
  
  # For every node, if it's a rule, colour as Black, otherwise Orange
  for node in network:
       if re.compile("^[R]\d+$").fullmatch(node) != None:
            color_map.append('black')
       else:
            color_map.append('orange')
  
  # Position nodes using spring layout
  pos = nx.spring_layout(network, k=16, scale=1)
  # Draw the network graph
  nx.draw(network, pos, node_color = color_map, font_size=8)            
  
  # Shift the text position upwards
  for p in pos:  
      pos[p][1] += 0.12

  nx.draw_networkx_labels(network, pos)
  plt.title("Network Graph for Association Rules")
  plt.show()

draw_network(rules, 20)