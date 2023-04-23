
import spacy
from fuzzywuzzy import process
import json

similarity_match_rel_list = ["comprises", "produces", "requires", "contains", "states", "example", "property"]
exact_match_rel_list = ["is a", "same as"]
nlp = spacy.load("en_core_web_sm", disable=['ner', 'parser'])

with open("./data/nodes_list.json", 'r') as f:
    nodes_list_unique = json.load(f)

class QueryConversionModel(object):
	def get_cypherquery(self, query_term):
		"""Given text input, apply model to return cypher query."""
		noun_list_query = []
		verb_list_query = []
		noun_list_result = []
		rel_list_result = []
		verb_b4_noun = 0

		#Extract nouns and verbs from query, and whether verb occurs before noun
		if len(query_term.split()) == 1:
		  noun_list_query.append(query_term)
		else:
		  doc = nlp(query_term)
		  for token in doc:
		      if token.pos_ == "NOUN":
		        if len(verb_list_query) >= 1 and len(noun_list_query) == 0:
		          verb_b4_noun = 1
		        noun_list_query.append(token.text)
		        
		      if token.pos_ == "VERB":
		        verb_list_query.append(token.text)
		# print(noun_list_query)

		#Identify nodes in query based on similarity match
		for noun in noun_list_query:
		  top_sim_node = process.extractOne(noun, nodes_list_unique)
		  if top_sim_node[1] >= 70:
		    noun_list_result.append(top_sim_node[0])

		#Identify relationships in query based on exact and similarity match
		rel_list_result = [str.replace(rel," ","_") for rel in exact_match_rel_list if rel in query_term]
		if len(rel_list_result) == 0:
		  sim_rel_text, sim_rel_score = process.extractOne(query_term, similarity_match_rel_list)
		  if sim_rel_score >= 70:
		    if sim_rel_text in ["property","example"]:
		      sim_rel_text = "has_" + sim_rel_text
		    rel_list_result.append(sim_rel_text)

		# print(noun_list_result)
		# print(rel_list_result)

		#If node identified, no relationship identified, return KG for node
		if len(noun_list_result) > 0 and len(rel_list_result) == 0:
		  return "MATCH (c:concept{ name: '%(node_1)s'})-[r]-(m) RETURN *"%{'node_1': noun_list_result[0]}
		#If node identified, relationship identified
		elif len(noun_list_result) > 0 and len(rel_list_result) >= 1:
		  #If relationship before noun, return directed KG where edge is leading to node
		  if verb_b4_noun == 1 and rel_list_result[0] in ["comprises", "produces", "requires", "contains"]:
		    return "MATCH (c)-[r:relationship{type: '%(relationship)s'}]->(m:concept{ name: '%(node_2)s'}) RETURN *"%{'relationship': rel_list_result[0], 'node_2': noun_list_result[0]}
		  #Otherwise, return directed KG where edge is pointing away from node 
		  else:
		    return "MATCH (c:concept{ name: '%(node_1)s'})-[r:relationship{type: '%(relationship)s'}]->(m) RETURN *"%{'node_1': noun_list_result[0], 'relationship': rel_list_result[0]}
		else:
		  return "No knowledge graph found. Please refine your query."