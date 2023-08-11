from flask import Flask,render_template,url_for,request,redirect
import SearchBackend, consts
import json
import requests
from bs4 import BeautifulSoup
import numpy
import js2py

redirectFunc=""
SEARCHLOCATIONS=['Web', 'Unstructured', 'Dual']

#Constants containing possible choices for filters
SOURCES=['DFT'] 
AUTHORS=['DFT']
TYPES=['Reports','Article','Statistics']


#filters selected by user
dateRange=""
startDate=""
endDate=""
sourcesToUse=[]
authorsToUse=[]
typesToUse=[]

#results from search to be rendered on page
sumText="Enter a query to see results..."
prevHeadings=["  ","  "," "]
prevText=[" "]*3
links=[]
webs=[" "]*3
webLinks=[]
webContents=[]
webSumTex=''


app=Flask(__name__)
app.static_folder='./static'
app.template_folder='./templates'


@app.route('/')
def index():
    print("RENDERING INDEX")
    return render_template('main.html', length=len(prevHeadings),sources=SOURCES, authors=AUTHORS,types=TYPES,summary=sumText,headings=prevHeadings,previewText=prevText,hyperlinks=links,webFindings=webs,webLinks=webLinks,webConts=webContents,webSum=webSumTex
                        )


#Performs a search query
@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST':
         print("SEARCH SUBMITTED FROM FRONTEND")
         print(request.form)
         query=request.form['searchQueryInput']#extracts search query from form
         #update global variables that contain content to be displayed on frontend - performing search and getting results
         global sumText,prevHeadings,prevText,links,webs,webLinks,webContents,webSumTex
         sumText, jsonResults, prevHeadings, prevText,links,webs,webLinks,webContents,webSumTex= SearchBackend.startSearch(query, SEARCHLOCATIONS[1],startDate,endDate,sourcesToUse,authorsToUse,typesToUse)     #SEARCHLOCATIONS: 0 FOR WEB, 1 FOR UNSTRUC, 2 FOR BOTH(TODO)   
         print("RESULTS RECEIVED AT FRONT END")
         return redirect(url_for("index"))
    return render_template('loading.html')


#Displays a loading screen
@app.route('/loading')
def loading():
       print("LOADING.")
       return render_template('loading.html')




#Method to change date range
@app.route('/date',methods=['POST'])
def changeDate():
         if request.method == 'POST': 
                  print(request.form)
                  print("DATE HAS BEEN CHANGED AT FRONT END.")
                  global startDate,endDate
                  startDate=request.form['start']
                  endDate=request.form['end']
         return render_template('loading.html')




#Updates all filters with selections
@app.route('/filter',methods=['POST'])
def changeFilters():
        if request.method == 'POST':
                print("FILTERS UPDATED AT FRONT END.")
                req=request.form
                global typesToUse,sourcesToUse,authorsToUse
                try:
                        typesToUse=req.getlist('types[]')
                except:
                       pass
                try:
                        authorsToUse=req.getlist('authors[]')

                except:
                       pass
                try:
                        sourcesToUse=req.getlist('sources[]')
                except:
                       pass
                
        return render_template('loading.html')

    

if __name__=="__main__":
        app.run(debug=True)

