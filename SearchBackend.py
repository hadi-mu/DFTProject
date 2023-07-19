"""Outline of basic search backend

    Currently receives a query, filter spec and the requested data store (Unstructured collection of docs or website).

    TODO:Search type logic in startSearch for case of dual (both) search
         authorFilter logic for filter string building
         parse results together for case of dual (both) search, and investigate generative summary for web search
        
"""

# from os.path import basename
# from typing import List, Optional, Tuple

from google.cloud import discoveryengine  # , discoveryengine_v1beta
import datetime  # required for date filters
import consts


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
        serving_config=serving_config, query=searchQuery, filter=filter, page_size=pageSize
    )

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

    response_json = discoveryengine.SearchResponse.to_json(
        searchResponse, including_default_value_fields=False, indent=2
    )

    # summary = searchResponse.summary
    summary = "Placeholder generative summary for web search"

    return summary, response_json

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

    summary = searchResponse.results[0].document.derived_struct_data["extractive_answers"][0]["content"]

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


def startSearch(query, searchType, startDate=None, endDate=None, sources=None, authors=None, types=None):
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
    -summary -> str
    -response_json -> str/JSON like
    """
    # create search client
    client = discoveryengine.SearchServiceClient()

    # authorFilter
    filter = authorFilter(startDate=None, endDate=None,
                          sources=None, authors=None, types=None)

    # perform single search & parse results
    if (searchType == "Web"):
        response = performSingleSearch(
            client, consts.WEB_DATASTORE, query, filter)
        summary, parsedResults = parseWebResults(response)

    elif (searchType == "Unstructured"):
        response = performSingleSearch(
            client, consts.UNSTRUCT_DATASTORE, query, filter)
        summary, parsedResults = parseUnstructuredResults(response)

    # return all parsed and filtered results in desired format
    return summary, parsedResults
