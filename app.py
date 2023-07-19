from flask import Flask,render_template,url_for,request
import SearchBackend, consts

SEARCHLOCATIONS=['Web', 'Unstructured', 'Dual']
SOURCES=['gov.uk','BBC','SkyNews'] #possible sources, authors, types etc...
AUTHORS=['Reporters','Government']
TYPES=['Reports','Articles','Audits']
dateRange=""
sourcesToUse=[]
authorsToUse=[]
typesToUse=[]
sumText="Enter a query to see results..."
prevHeadings=["First Result","Second Result","Third Result"]
prevText=["Article summary goes here"]*3
app=Flask(__name__)
app.static_folder='./static'


@app.route('/',methods=['POST','GET'])
def index():
          if request.method == 'POST': #query posted to this method
                  query=request.form['query']
                  print("QUERY IS: " + request.form['query']) 
                  global sumText
                  sumText, jsonResults = SearchBackend.startSearch(query, SEARCHLOCATIONS[1])     #SEARCHLOCATIONS: 0 FOR WEB, 1 FOR UNSTRUC, 2 FOR BOTH(TODO)
                  print("SUMMARY IS: "+ sumText)
                  print("JSON IS: "+ jsonResults)

                  
          return render_template('main.html', sources=SOURCES, authors=AUTHORS,types=TYPES,summary=sumText,headings=prevHeadings,previewText=prevText
          )

@app.route('/date',methods=['POST','GET'])
def changeDate():
         if request.method == 'POST': #query posted to this method
                  dateRange=request.form['start']+':'+request.form['end']
                  print("Dates selected are " + dateRange)
         return render_template('main.html', sources=SOURCES, authors=AUTHORS,types=TYPES,summary=sumText,headings=prevHeadings,previewText=prevText
          )

@app.route('/filter',methods=['POST','GET'])
def changeFilters():
        if request.method == 'POST':
                req=request.form
                typesToUse=req.getlist('types[]')
                authorsToUse=req.getlist('authors[]')
                sourcesToUse=req.getlist('sources[]')
                print("Types" + str(typesToUse))
        return render_template('main.html', sources=SOURCES, authors=AUTHORS,types=TYPES,summary=sumText,headings=prevHeadings,previewText=prevText
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

        return summary, articleHeadings, articleSummaries, articleLinks

'''''''''
@app.route("/search_genappbuilder", methods=["POST"])
def search_genappbuilder(search_query) -> str:
    """
    Handle Search Gen App Builder Request
    """

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
        summary, jsonResults = SearchBackend.startSearch(query, SEARCHLOCATIONS[1])     #SEARCHLOCATIONS: 0 FOR WEB, 1 FOR UNSTRUC, 2 FOR BOTH(TODO)
        print(summary)
        return(jsonResults)

if __name__=="__main__":
        app.run(debug=True)

