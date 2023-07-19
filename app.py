from flask import Flask,render_template,url_for,request,redirect
import SearchBackend, consts
import json


SEARCHLOCATIONS=['Web', 'Unstructured', 'Dual']

#Constants containing possible choices for filters
SOURCES=['gov.uk','BBC','SkyNews','DFT'] 
AUTHORS=['Reporters','Government','DFT']
TYPES=['Reports','Articles','Audits','Statistics']


#filters selected by user
dateRange=""
startDate=""
endDate=""
sourcesToUse=[]
authorsToUse=[]
typesToUse=[]

#results from search to be rendered on page
sumText="Enter a query to see results..."
prevHeadings=["First Result","Second Result","Third Result"]
prevText=["Article summary goes here"]*3
links=[]


app=Flask(__name__)
app.static_folder='./static'


@app.route('/',methods=['POST','GET'])
def index():
          
          if request.method == 'POST': #query posted to this method
                  
                  query=request.form['query']#extracts search query from form
                                    
                  #update global variables that contain content to be displayed on frontend - performing search and getting results
                  
                  global sumText,prevHeadings,prevText,links
                  sumText, jsonResults, prevHeadings, prevText,links = SearchBackend.startSearch(query, SEARCHLOCATIONS[1],startDate,endDate,sourcesToUse,authorsToUse,typesToUse)     #SEARCHLOCATIONS: 0 FOR WEB, 1 FOR UNSTRUC, 2 FOR BOTH(TODO)          

                  
          return render_template('main.html', length=len(prevHeadings),sources=SOURCES, authors=AUTHORS,types=TYPES,summary=sumText,headings=prevHeadings,previewText=prevText,hyperlinks=links
          )



#Method to change date range
@app.route('/date',methods=['POST','GET'])
def changeDate():
         
         if request.method == 'POST': 
                  global startDate,endDate
                  #update dateRange with dates specified in form
                  startDate=request.form['start']
                  endDate=request.form['end']
                  dateRange=request.form['start']+':'+request.form['end']
                  print("Dates selected are " + dateRange)

         return render_template('main.html', length=len(prevHeadings),sources=SOURCES, authors=AUTHORS,types=TYPES,summary=sumText,headings=prevHeadings,previewText=prevText,hyperlinks=links
          )



#Updates all filters with selections
@app.route('/filter',methods=['POST','GET'])
def changeFilters():
        
        if request.method == 'POST':

                req=request.form
                global typesToUse,sourcesToUse,authorsToUse
                typesToUse=req.getlist('types[]')
                authorsToUse=req.getlist('authors[]')
                sourcesToUse=req.getlist('sources[]')

                #print("Types" + str(typesToUse))

        return render_template('main.html', length=len(prevHeadings),sources=SOURCES, authors=AUTHORS,types=TYPES,summary=sumText,headings=prevHeadings,previewText=prevText,hyperlinks=links
          )
        





def searchQuery(query, searchType,startDate=None,endDate=None,sources=None,authors=None,types=None):
        
        #TO IMPLEMENT
        #PASS IN QUERY STRING, FILTER INFORMATION, AND WHETHER TO SEARCH WEB OR UNSTRUCTURED DATA (eg UPLOADED DOCS)
        #searchType takes in a string of value given by SEARCHLOCATIONS. We need to connect to a different search engine
        #for a search of webpages, or of unstructured/ uploaded docs (eg pdfs). 
        # If both is selected then both locations will be searched seperately - NOT YET IMPLEMENTED

        #Method creates searchQuery, performs relevant searches, applies filters, and returns results as required, including extractive answer.
        

        ###---HOW TO CALL BACKEND---###
        #summary, jsonResults = SearchBackend.startSearch(query, searchType, startDate, endDate, sources, authors, types)
        #return summary, jsonResults

        #return summary, articleHeadings, articleSummaries, articleLinks

 '''''''''
@app.route("/search_genappbuilder", methods=["POST"])
def search_genappbuilder(search_query) -> str:
    """
    Handle Search Gen App Builder Request
    """fal

    # Check if POST Request includes search query
    if not search_query:
        return render_template('main.html', sources=SOURCES, authors=AUTHORS,types=TYPES
          )

    results, request_url, raw_request, raw_response = search_enterprise_search(
        project_id=PROJECT_ID,
        location=LOCATION,
        search_engine_id=CUSTOM_UI_DATASTORE_IDS[0]["datastore_id"],
        search_query=search_query,
    )

    return render_template(
        "search.html",
        nav_links=NAV_LINKS,
        message_success=search_query,
        results=results,
        request_url=request_url,
        raw_request=raw_request,
        raw_response=raw_response,
    )
'''''''''





#Test path for backend
@app.route('/test_search')
def testSearch():
        query = "How many accidents were there in 2021?"
        summary, jsonResults, titleArr, previewArr, linkArr = SearchBackend.startSearch(query, SEARCHLOCATIONS[1])     #SEARCHLOCATIONS: 0 FOR WEB, 1 FOR UNSTRUC, 2 FOR BOTH(TODO)
        print(summary)
        return(jsonResults)

if __name__=="__main__":
        app.run(debug=True)

