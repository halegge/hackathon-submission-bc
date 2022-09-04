# Project name
Search Engine Comparison/Graph Modeller

## Team Members
disco-johnny & HLegge :-)

## Tool Description
Honestly just went and looked at the handy GDrive link you gave us with people's wishes for tools, someone at the very top put in that they wanted a tool to compare results and we thought aye, could do that.
Pings a query to both Google and Bing before seeing how many keywords in the query occur in the snippets of each result from each engine. 
Then lists the results side by side (admittedly unordered) so you can compare which engine is more "relevant". 
The functionality exists on the backend to build an undirected multigraph where the set of nodes consists of the returned results and the set of edges consists of shared keywords enabling you to observe links with the least or most in common with the other links provided.

So the two features would be, a basic relevancy scoring for results from different engines as well as second feature of potentially identifying search results more unique than the rest or even more aligned with the other results.

## Installation
This section includes detailed instructions for installing the tool, including any terminal commands that need to be executed and dependencies that need to be installed. Instructions should be understandable by non-technical users (e.g. someone who knows how to open a terminal and run commands, but isn't necessarily a programmer), for example:

1. Make sure you have Python version 3.8 or greater installed. And clone the repo with:
		
		git clone https://github.com/halegge/hackathon-submission-bc.git

2. Move to the tool's directory and install the tool

        cd hackathon-submission-bc
        pip install -r requirements.txt
		
3. Replace "_BING_KEY" with your Azure API key, and "SEARCH_KEY" and "SEARCH_ID" with your Google Search API creds.
		
3. Run the Flask server 

		flask run
		
4. Visit 127.0.0.1/5000 to see the result

## Usage
The "tool" has no CLI interface, and does not accept user input, upon loading the page it automatically queries a local cache of the google API result of the query: "how many neutrons in an argon molecule" as well as the Bing Web Search API

## Additional Information
Next steps:
- Add user input
- Add interface for accessing the graph function on the front end in order to provide insight about the relationship between results
- Dynamic JS charting of the resulting networkx graph