# Automatic Knowledge Graph construction

## Objective

1. Extract concepts and relationships from a Biology textbook to construct a knowledge graph

2. Provide a natural language interface to query the knowledge graph

## Deployed app

The deployed app is accessible at https://chinese-news-ner.onrender.com 

## Running the app on your local

1. Clone this repository

	`git clone https://github.com/quissuiven/kg-construction.git`

2. Build and run Docker Image

	```
	cd kg-construction
	docker build -f Dockerfile.txt -t kg-app .
	docker run --name flask1 -d --publish 5000:5000 kg-app
	```

3. View the rendered app at http://localhost:5000/

