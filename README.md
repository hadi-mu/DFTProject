# DFTPrototype


This is a search engine used for searching through and summarising findings from DFT data. It searches through uploaded pdfs and listed websites.

The unstructured documents it has access to are contained within the following bucket intern_test within the gen-ai-sanbox project. 

>NOTE: When uploading documents to this bucket you need to add custom metadata for each of them. You need to add the four following fields as shown below:
><img width="1176" alt="image" src="https://github.com/hadi-mu/GOREPLY-DFTSEARCHENGINE/assets/61840032/03ae4225-9157-4a96-99e7-ad288d953acd">
><img width="1178" alt="image" src="https://github.com/hadi-mu/GOREPLY-DFTSEARCHENGINE/assets/61840032/cd0660cc-6fd2-47a8-8a9e-ca850b2e45e8">
><img width="594" alt="image" src="https://github.com/hadi-mu/GOREPLY-DFTSEARCHENGINE/assets/61840032/fe786681-a386-4bc8-8ed3-8d2495263712">




The two generative apps used for searching are the dft-open-data (ID:dft-open-data-test_1685004630707) for websites and internTest (ID:interntest_1688551513897) for unstructured data. To add additional websites to search over, open the dft-open-data app, go to the data tab and the add in the required urls:
<img width="1181" alt="image" src="https://github.com/hadi-mu/GOREPLY-DFTSEARCHENGINE/assets/61840032/70baeb30-6102-47aa-844d-6082a73801c3">


To run the website:

1. Install the requirements by running the following in the terminal

   `pip install -r requirements.txt`

2. To launch the website, run the following in the terminal

   `flask run`

3. Type the url seen in the command line into your browser
   <img width="832" alt="image" src="https://github.com/hadi-mu/GOREPLY-DFTSEARCHENGINE/assets/61840032/3aa545bd-dbc7-4223-95be-5593f8fe1680">


When running the website, type your query into the searchbox to perform a search. Use the dropdowns underneath the searchbar to set up any filters you want. After entering, there will be a loading application and your search results will be rendered.

<img width="1169" alt="image" src="https://github.com/hadi-mu/GOREPLY-DFTSEARCHENGINE/assets/61840032/98128240-edca-488c-8673-047e4d8e5c51">




 


