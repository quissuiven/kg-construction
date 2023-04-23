import openai

openai.api_key = "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"

INSTRUCTION_tocypher = """
#What is a chloroplast?
MATCH (c:concept{ name: 'chloroplasts'})-[r:relationship{type: 'is_a'}]->(m) RETURN *

#What are the properties of chloroplasts?
MATCH (c:concept{ name: 'chloroplasts'})-[r:relationship{type: 'has_property'}]->(m) RETURN *

#Tell me everything about chloroplasts.
MATCH (c:concept{ name: 'chloroplasts'})-[r]->(m) RETURN *

#Give me some examples of cells.
MATCH (c:concept{ name: 'cell'})-[r:relationship{type: 'has_example'}]->(m) RETURN *

#What does photosynthesis require?
MATCH (c:concept{ name: 'photosynthesis'})-[r:relationship{type: 'requires'}]->(m) RETURN *
"""

class QueryConversionModel(object):
	def get_cypherquery(self, text_input):
		"""Given text input, apply model to return cypher query."""
	    response = openai.ChatCompletion.create(
	     model="gpt-3.5-turbo",
	       messages=[
	         {"role": "user", "content": INSTRUCTION_tocypher + text_input + "\n\noutput:\n\n"}],
	     max_tokens=1900,
	     temperature=0,
	     top_p=1,
	     stop=[" END"]
	    )
	    extracted_text = response["choices"][0]["message"]["content"]

		# response = openai.Completion.create(
		#   model="text-davinci-003",
		#   prompt=INSTRUCTION_tocypher + text_input + "\n\noutput:\n\n",
		#   temperature=0,              
		#   max_tokens=2300,          
		#   top_p=1,                      
		#   frequency_penalty=0.0,
		#   presence_penalty=0.0
		# )
		# extracted_text = response['choices'][0]['text']
		return extracted_text