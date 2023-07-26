"""Outline of basic search backend

    Currently receives a query, filter spec and the requested data store (Unstructured collection of docs or website).

    TODO:Search type logic in startSearch for case of dual (both) search
         authorFilter logic for filter string building
         parse results together for case of dual (both) search, and investigate generative summary for web search
        
"""

# from os.path import basename
# from typing import List, Optional, Tuple

from google.cloud import discoveryengine,storage,aiplatform # , discoveryengine_v1beta
import datetime  # required for date filters
import consts
import json
from blobtest import blob_metadata
import vertexai
from vertexai.language_models import TextGenerationModel
import requests
from bs4 import BeautifulSoup

STORAGE_CLIENT = storage.Client()
BUCKET = STORAGE_CLIENT.bucket(consts.BUCKET_NAME)

vertexai.init(project="gen-ai-sandbox", location="us-central1")
parameters = {
    "temperature": 0.5,
    "max_output_tokens": 1024,
    "top_p": 0.8,
    "top_k": 40
}
model = TextGenerationModel.from_pretrained("text-bison@001")


def authorFilter(startDate=None, endDate=None, sources=None, authors=None, types=None):
    """
    TODO
    Summary: Takes in list of criteria and produces correctly formatted filter as a string, as required in EBNF format.

    Arguments:
    -startDate -> datetime.date
    -endDate -> datetime.date
    -sources -> str
    -authors -> str
    -types -> str

    Returns:
    filter_string -> str: formatted filter in required EBNF format, see: https://cloud.google.com/retail/docs/filter-and-order#filter 

    """

    filter_string = ""

    # TODO: Logic for building string based on requirements

    if (startDate != None):
        # append start date to filter
        pass

    if (endDate != None):
        # append end date to filter
        pass

    if (sources != None):
        # append sources to filter
        pass

    if (authors != None):
        # append authors to filter
        pass

    if (types != None):
        # append types to filter
        pass

    return filter_string


def performSingleSearch(searchServiceClient, searchEngineID, searchQuery, filter, pageSize=50):
    """
    Summary: Takes in a SearchServiceClient, SearchEngine/Datastore/Enterprise Search App ID, filter and number of results to return.
    Performs a search on a single selected datastore, returning the results as a SearchResponse 
    object: https://cloud.google.com/dotnet/docs/reference/Google.Cloud.DiscoveryEngine.V1Beta/latest/Google.Cloud.DiscoveryEngine.V1Beta.SearchResponse

    Arguments:
    -searchServiceClient -> DiscoveryEngine.searchServiceClient
    -searchEngineID -> str
    -searchQuery -> str
    -filter -> str
    -pageSize -> int

    Returns:
    -response -> DiscoveryEngine.SearchResponse: A search response object containing all 
    key information about results of the search - but not yet parsed fully.
    """

    serving_config = searchServiceClient.serving_config_path(
        project=consts.PROJECT_ID,
        location=consts.LOCATION,
        data_store=searchEngineID,
        serving_config="default_config",
    )


    # Create search request using config and query
    request = discoveryengine.SearchRequest(
        serving_config=serving_config, query=searchQuery, filter=filter, page_size=pageSize,content_search_spec=discoveryengine.SearchRequest.ContentSearchSpec(summary_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
        summary_result_count=3,
        #include_citations=True
        )
        
    ))

    #Setting summary to be generated from all documents
    request.content_search_spec.extractive_content_spec.max_extractive_answer_count = 1 #number of single document summaries (extractive content) per document

    # Search performed and raw search results returned
    response_pager = searchServiceClient.search(request)


    # Creating Search Response object for easier parsing - can extract more info from SearchResponse if required
    response = discoveryengine.SearchResponse(
        results=response_pager.results,
        facets=response_pager.facets,
        guided_search_result=response_pager.guided_search_result,
        total_size=response_pager.total_size,
        attribution_token=response_pager.attribution_token,
        next_page_token=response_pager.next_page_token,
        corrected_query=response_pager.corrected_query,
        summary=response_pager.summary,)

    return response


def parseWebResults(searchResponse):
    """
    Summary: Parse discoveryengine.SearchResponse from a single search of URL resources into a more readable form.
    TODO: Research if a generative summary for websearch is possible at the moment - doesn't appear to be in the example:
    https://genappbuilder-demo-lnppzg3rxa-uc.a.run.app/search

    Arguments:
    -searchResponse -> DiscoveryEngine.SearchResponse

    Returns:
    -summary -> str
    -response_json -> str/JSON like
    """
    # request_json = discoveryengine.SearchRequest.to_json(
    #    searchRequest, including_default_value_fields=True, indent=2
    # )
    print("PARSING WEB RESULTS...")
    response_json = discoveryengine.SearchResponse.to_json(
        searchResponse, including_default_value_fields=False, indent=2
    )
    print("DONE PARSING WEB RESULTS...")

    return response_json

    """
    TODO:
    results = []
    for result in searchResponse.results:
            data = result.document.derived_struct_data

            # Grabbing source image if available
            cse_thumbnail = data["pagemap"].get("cse_thumbnail")
            if cse_thumbnail:
                image = cse_thumbnail[0]["src"]
            else:
                image = "https://www.google.com/images/errors/robot.png"
            results.append(
                {
                    "title": data["title"],
                    "htmlTitle": data["htmlTitle"],
                    "link": data["link"],
                    "htmlFormattedUrl": data["htmlFormattedUrl"],
                    "displayLink": data["displayLink"],
                    "snippets": [s["htmlSnippet"] for s in data["snippets"]],
                    "thumbnailImage": image,
                    "resultJson": discoveryengine.SearchResponse.SearchResult.to_json(
                        result, including_default_value_fields=True, indent=2
                    ),
                }
            )
    """


def parseUnstructuredResults(searchResponse):
    """
    Summary: Parse discoveryengine.SearchResponse from a single search of unstructured resources into a more readable form.

    Arguments:
    -searchResponse -> DiscoveryEngine.SearchResponse

    Returns:
    -summary -> str
    -response_json -> str/JSON like
    """
    # request_json = discoveryengine.SearchRequest.to_json(
    #    searchRequest, including_default_value_fields=True, indent=2
    # )

    response_json = discoveryengine.SearchResponse.to_json(
        searchResponse, including_default_value_fields=False, indent=2
    )

    summary = searchResponse.summary.summary_text
    return summary, response_json
    """
    TODO:
    results = []
    for result in searchResponse.results:
            data = result.document.derived_struct_data
            results.append(
                {
                    "resultJson": discoveryengine.SearchResponse.SearchResult.to_json(
                        result, including_default_value_fields=True, indent=2
                    ),
                }
            )
    """

def parseLink(link):
    """
    Converts google cloud storage link to a searchable url

    Arguments:
    -link-> gs link to be converted

    Returns:
    -newLink-> converted link
    """

    newLink=link.replace(" ","%20")
    newLink=newLink.replace("gs://","https://storage.cloud.google.com/")
    return newLink



def titleFromLink(link):
    """
    Extracts document title from url

    Arguments:
    -link-> Document url

    Returns:
    -title-> Extracted title
    """

    linkSplit=link.split('/')
    title=linkSplit[-1]
    return title

def getTags(blob_name):

    """
    Extracts metadata from a google bucket blob

    Arguments:
    blob_name-> Name of the blob

    Returns:
    types,source,date,author-> blob metadata tags
    """

    print("GETTING TAGS...")
    blob = BUCKET.get_blob(blob_name)
    print("GOT THE BLOB")
    metadata=blob.metadata
    print("GOT THE METADATA")

    try:

        types=metadata["type"]
        author=metadata["author"]
        date=metadata["date"]
        source=metadata["source"]
    except:
        print("Error with " + blob.name )
        types=source=date=author='ERROR'
    return types,source,date,author


def checkDateInRange(date,start,end,web=False):
    """
    Checks if a date. Processes dates from web results and unstructured results differently.

    Arguments:
    date-> Date to check
    start-> Start of range
    end-> End of range
    web-> Whether date is in web format or not

    Returns:
    True or false
    """

    try:

        if web:
            date=date.split('-')
        else:
            date=date.split('/')
            date.reverse()

        start=start.split('-')
        end=end.split('-')

        start=list(map(int,start))
        date=list(map(int,date))
        end=list(map(int,end))

        start=datetime.datetime(*start)
        date=datetime.datetime(*date)
        end=datetime.datetime(*end)


        #print(start)
        #print(end)
        #print(date)


        if date=="":
            return True
        
        if start<date<end:
            return True
        else:
            return False

    except:
        return False



def startSearch(query, searchType, startDate="", endDate="", sources="", authors="", types=""):
    """
    Summary:
    -If filters required then create correct filter string
    -Calls performSingleSearch for each search location requested, with required filters.
    -Receives full response objects
    -Passes results into parseResults for each response object
    -TODO: Combines parsed result from multiple sources if searchType = "Dual"
    -returns parsed results to frontend

    Arguments:
    -query -> str
    -searchType -> str: "Web", "Unstructured" or "Dual"
    -startDate -> datetime.date
    -endDate -> datetime.date
    -sources -> str
    -authors -> str
    -types -> str


    Returns: 
    -unstSummary -> Summary for unstructured search.
    -unstParsedResults -> str/JSON like
    -unstTitleArr -> Titles for all unstructured results
    -unstPreviewArr -> arr containing document content from results
    -unstLinkArr -> arr containing document links 
    -webSum -> Summary for web search.
    -webTitleArr -> Titles for all web results
    -webConts -> arr containing individual webpage summaries
    -webLinkArr -> arr containing web links 


    """

    # create search client
    print("SEARCH SUBMITTED")

    client = discoveryengine.SearchServiceClient()

    # authorFilter
    filter = authorFilter(startDate=None, endDate=None,
                          sources=None, authors=None, types=None)

    # perform single search & parse results
    webResponse = performSingleSearch(
            client, consts.WEB_DATASTORE, query, filter)
    webParsedResults = parseWebResults(webResponse)
    unstResponse = performSingleSearch(
            client, consts.UNSTRUCT_DATASTORE, query,filter)
    unstSummary, unstParsedResults = parseUnstructuredResults(unstResponse)

    print("RESULTS RECIEVED")
    unstSummary=model.predict('Reword the following text to sound better, put it into one paragraph: '+unstSummary).text
    
    unstTitleArr,unstLinkArr,unstPreviewArr=extractFromJSON(unstParsedResults,True,startDate,endDate,sources,authors,types)            
    webTitleArr,webLinkArr,webConts=extractFromJSON(webParsedResults,False,startDate,endDate,sources,authors,types)            
    
    webSum=webSummary(webTitleArr,webLinkArr)

    # return all parsed and filtered results in desired format
    return unstSummary, unstParsedResults, unstTitleArr, unstPreviewArr, unstLinkArr, webTitleArr,webLinkArr,webConts, webSum







def extractFromJSON(jsonFile,unstructured,start,end,sources,authors,types):

    """
    Extracts information including titles,links and contents from search result json file.

    Arguments:
    -jsonFile-> results json file
    -unstructured-> whether search was unstructured or not
    -start,end,sources,authors,types-> filters

    Returns:
    -titles,links,contents-> Titles, urls and previews for all results
    """
    titles=[]
    links=[]
    contents=[] 
    parsedDict=json.loads(jsonFile)
    resultsArr=parsedDict["results"]
    passCount=0
    for result in resultsArr:

        if passCount<3:
            documentDict=result["document"]
            docDataDict=documentDict["derivedStructData"]
            if unstructured:
                 success,title,link,content=processUnstructuredDocDict(docDataDict,start,end,sources,authors,types)
                 if success:
                     passCount+=1
                     titles.append(title)
                     links.append(link)
                     contents.append(content)
                 else:
                     print("DOC REJECTED")
            else:
                if webFilters(docDataDict,start,end,types):
                        passCount+=1
                        title,link,content=processWebDataDict(docDataDict)
                        titles.append(title)
                        links.append(link)
                        contents.append(content)
                        print("SITE ACCEPTED")
                else:
                    print("SITE REJECTED")
                
    return titles,links,contents


def processUnstructuredDocDict(dataDict,startDate="", endDate="", sources="", authors="", types=""):

    print("PROCESSING UNSTRUCTURED...")
    append=True
    docDataArr=dataDict["extractive_answers"]
    docData=docDataArr[0]
    docContent=docData["content"]
    docLink=dataDict["link"]
    print("PROCESSED, NOW GETTING LINK")
    title=titleFromLink(docLink)
    docLink=parseLink(docLink)
    docTypes,source,date,author=getTags(title)
    print("DONE GETTING LINK")
    if types!=[]:
                if not(docTypes in types):
                    append=False


    if sources!=[]:
        if not(source in sources):
            append=False
    
    if authors!=[]:
        if not(author in authors):
            append=False
    
    if startDate or endDate:
        if not(checkDateInRange(date,startDate,endDate)):
            append=False

    if append:
        print("DOC ACCEPTED")

        return True,title,docLink,model.predict('Provide a brief summary for the following text:' + docContent ).text
    else:
        return False,[],[],[]
    
def processWebDataDict(dataDict):
    title=dataDict["title"]
    link=dataDict["link"]
    snip=dataDict["snippets"][0]["snippet"]
    return title,link,snip

def webFilters(dataDict,startDate,endDate,type):
    try:
        passed=True
        map=dataDict["pagemap"]
        tags=map["metatags"][0]
        date=tags["govuk:first-published-at"]
        date=date[0:9]
        pageType=tags["og:type"].capitalize()
        if startDate or endDate:
            if not(checkDateInRange(date,startDate,endDate,True)):
                passed=False
        if type:
            if not(pageType in type):
                passed=False
        return passed
    except:
        print("ERROR FILTERING WEBPAGE")
        return True
    
def webSummary(titles,links):
    joined=''
    for i in range(len(links)):
        content=getPageContent(links[i])
        initial="Provide a brief summary for the following article:" + content +'.'
        summ=model.predict(initial).text
        joined+=summ + ', '
    final = model.predict("Provide a brief summary for the following article: " + joined + '.').text

    return final


def getPageContent(url):

    page=requests.get(url).text

    soup=BeautifulSoup(page)

    # Get text from all <p> tags.
    p_tags = soup.find_all(['p','ul','li'])
    
    # Get the text from each of the "p" tags and strip surrounding whitespace.
    p_tags_text = [tag.get_text().strip() for tag in p_tags]
    # Filter out sentences that contain newline characters '\n' or don't contain periods.
    sentence_list = [sentence for sentence in p_tags_text if not '\n' in sentence]

    article = ' '.join(sentence_list)

    return article

