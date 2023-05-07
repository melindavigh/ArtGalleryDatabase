from flask import render_template, redirect, request
from sqlalchemy import create_engine, text
import pandas as pd
from WebArtGallery import app
import os

def connect():
    user = os.getenv('EXHIBIT_SQL_USER')
    password = os.getenv('EXHIBIT_SQL_PASSWORD')
    database = os.getenv('EXHIBIT_SQL_DATABASE')
    server = os.getenv('EXHIBIT_SQL_SERVER')
    url = f'mysql+mysqlconnector://{user}:{password}@{server}/{database}'
    engine = create_engine(url)
    return engine

def display_function(queery):
    engine = connect()
    # print(queery)
    with engine.connect() as con:
        rs = con.execute(text(queery))
        return_sting = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Table</title>
            <style>
               table {
                    margin: 0 auto;
                    font-size: large;
                    border: 1px solid white;
                }
        
                h1 {
                    text-align: center;
                    color: white;
                    font-size: xx-large;
                    font-family: 'Gill Sans', 'Gill Sans MT',
                    ' Calibri', 'Trebuchet MS', 'sans-serif';
                }
        
                td {
                    text-align: center;
                    color: white;
                    border: 1px solid white;
                }
        
                th{
                    text-align: center;
                    color: white;
                    font-size: xx-large;
                    font-family: 'Gill Sans', 'Gill Sans MT',
                    ' Calibri', 'Trebuchet MS', 'sans-serif';
                },
                td {
                    font-weight: bold;
                    border: 1px solid white;
                    padding: 10px;
                    text-align: center;
                }
        
                td {
                    font-weight: lighter;
                }
                
                body {
                    background-image: url("static/img/bluesplash.jpg");
                }

            </style>
        
        </head>
        <body> 
        <table><tr>"""

        for col in rs.keys():
            return_sting += "<th>" + str(col) + "</th>"
        return_sting += "</tr>"

        for row in rs:
            return_sting += "<tr>"
            for x in row:
                return_sting += "<td>" + str(x) + "</td>"
            return_sting += "</tr>"
                    # """"<table>
                    #     <tr>
                    #         <th></th>
                    #     </tr>
                    #     <tr>
                    #         <td></td>
                    #     </tr>
                    # </table>"""
            print(row)
        return_sting += "</table>" + "</body></html>"

    return return_sting
@app.route("/", methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        query_data = request.form
        # first queery
        if query_data['onechoice'] == 'queery 1':
            print(query_data['mediumList'])
            return display_function(f"""SELECT DISTINCT   A.artistID, A.artistName
                           FROM     Artist AS A, Artwork AS R
                           WHERE    A.artistID=R.artistID AND R.medium='{query_data['mediumList']}'""")

        # second queery goes here
        elif query_data['onechoice'] == 'queery 2':
            #print(query_data['priceRanges'])
            return display_function(f"""SELECT   C.customerName, S.transactionPrice
                 FROM   Customer AS C, SellTo AS S
                 WHERE  C.customerID = S.customerID AND {query_data['priceRanges']}""")

        # third queery goes here
        elif query_data['onechoice'] == 'queery 3':
            return display_function(f"""SELECT  R.medium,  COUNT(S.transactionQuantity) AS TotTrans
                            FROM   Artwork AS R, Exhibit AS E, SellTo AS S, Customer AS C
                            WHERE  R.exhibitID = E.exhibitID AND E.exhibitID =S.exhibitID AND S.customerID = C.customerID AND C.customerID=S.customerID AND S.transactionPrice >= 20000000
                            GROUP BY  R.medium""")

        # forth queery goes here
        elif query_data['onechoice'] == 'queery 4':
            print(query_data['genraRange'])
            return display_function(f"""SELECT  artistName, artistID
                        FROM Artist 
                        WHERE  artistID   NOT IN  (SELECT  artistID
                                   FROM   Artwork
                                   WHERE  genre = '{query_data['genraRange']}')""")

        # fifth queery goes here
        elif query_data['onechoice'] == 'queery 5':
            return display_function(f"""SELECT  artTitle, COUNT(DISTINCT exhibitID) AS ExhibitCount
                FROM   Artwork
                GROUP BY  artTitle""")
        # print(query, medium)

        # sixth queery goes here
        elif query_data['onechoice'] == 'queery 6':
            return display_function(f"""SELECT    E.exhibitID, sum(T.transactionPrice)AS TotalRev
                FROM Exhibit AS E, SellTo AS S, Customer AS C, Transactions AS T
                WHERE 	E.exhibitID = S.exhibitID AND S.customerID = C.CustomerID AND C.customerID = T.customerID
                GROUP BY    E.exhibitID""")

        # seventh queery goes here
        elif query_data['onechoice'] == 'queery 7':
            return display_function(f"""SELECT E.address, R.artTitle 
                FROM Exhibit AS E, Artwork as R    
                WHERE E.exhibitID = R.exhibitID 
                ORDER BY E.address""")

        # eight queery goes here
        elif query_data['onechoice'] == 'queery 8':
            return display_function(f"""SELECT A.artistName, COUNT(A.artistID) AS Ct
                FROM  Artist AS A, Exhibit AS E, Registered AS R
                WHERE A.artistID = R.artistID AND R.exhibitID = E.exhibitID
                GROUP BY  A.artistName
                HAVING COUNT(A.artistID) >= 3""")

        # nineth queery goes here
        elif query_data['onechoice'] == 'queery 9':
            print(query_data['exhibitList'])
            return display_function(f"""SELECT A.artistID, A.artistName
                FROM Artist AS A, Exhibit AS E, Registered AS R
                WHERE A.artistID=R.artistID AND E.exhibitID=R.exhibitID AND E.exhibitName='{query_data['exhibitList']}'""")

    return render_template("helloworld.html")

@app.route("/sayhello/<name>")
def sayhello(name):
    return render_template("helloworld.html", name = name)