from sqlalchemy import create_engine, text  # to connect to sql
import pandas as pd  # manipulate data

url = 'mysql+mysqlconnector://root:melindasql@localhost/MyGallery'
engine = create_engine(url)  # sql connection

# this uses pandas to run the query
# """ these are for doing multi-line string
# rs = pd.read_sql("""SELECT MAX(E.salary) AS MaxSal, AVG(E.salary) AS AvgSal, MIN(E.salary) AS MinSal
#                     FROM Employee AS E, Department as D
#                     WHERE E.DepartmentID = D.Did AND D.Dname = 'Marketing'""", engine)
# print(rs)
#
# this uses the quotation 'value'  "select * from table where bla ='boo'"
# this uses the connector to the sql workbench
# rs is an object
# with engine.connect() as con:
#     rs = con.execute(text("""SELECT MAX(E.salary) AS MaxSal, AVG(E.salary) AS AvgSal, MIN(E.salary) AS MinSal
#                     FROM Employee AS E, Department as D
#                     WHERE E.DepartmentID = D.Did AND D.Dname = 'Marketing'"""))
#     for row in rs:
#         print(row)
# #
for table in ["Artwork", "Exhibit", "Customer", "Transactions", "Registered", "SellTo", "Artist"]:
    df = pd.read_excel('ArtGalleryDataBase.xlsx', sheet_name=table, skiprows=1) # reads from excel file, skips forst row cause we dont want it
    df.to_sql(table, engine, if_exists='replace', index=False) # this writes the tables to sql. It'll also update any changes we make to the excel file
    print(df)



# print("1. Display name and ID of Artist who use “oil paint” as a medium for their artwork")
# with engine.connect() as con:
#      rs = con.execute(text("""SELECT DISTINCT   A.artistID, A.artistName
#                 FROM     Artist AS A, Artwork AS R
#                 WHERE    A.artistID=R.artistID AND R.medium='oil paint'"""))
#      for row in rs:
#          print(row)
# print()
#
# print("2. Display name of Customers, Transaction ID, and transactionPrice who purchase artwork between the range of $50000000 - $100000000")
# with engine.connect() as con:
#     rs2 = con.execute(text("""SELECT   C.customerName, T.transactionID, T.transactionPrice
#                 FROM   Customer AS C, Transactions AS T
#                 WHERE  C.customerID = T.customerID AND T.transactionPrice >=50000000 AND T.transactionPrice<=100000000"""))
#     for row in rs2:
#         print(row)
# print()
#
# print("3. Count the number of transactions with price higher than $20000000 per artwork medium")
# with engine.connect() as con:
#     rs3 = con.execute(text("""SELECT  R.medium,  COUNT(T.transactionID) AS TotTrans
#             FROM   Artwork AS R, Exhibit AS E, SellTo AS S, Customer AS C, Transactions AS T
#             WHERE  R.exhibitID = E.exhibitID AND E.exhibitID =S.exhibitID AND S.customerID = C.customerID AND C.customerID=T.customerID AND T.transactionPrice >= 20000000
#             GROUP BY  R.medium"""))
#     for row in rs3:
#         print(row)
# print()
#
# print("4. Display name and ID of artists who doesn’t create artwork in the ‘realism’ genre ")
# with engine.connect() as con:
#     rs4 = con.execute(text("""SELECT  artistName, artistID
#         FROM Artist AS A
#         WHERE  artistID   NOT IN  (SELECT  artistID
#                                    FROM   Artwork
#                                    WHERE  genre = 'Realism')"""))
#     for row in rs4:
#         print(row)
# print()
#
# print("5. Display the number of exhibits each artwork has been to sorted by their titles")
# with engine.connect() as con:
#     rs6 = con.execute(text("""SELECT  artTitle, COUNT(DISTINCT exhibitID) AS ExhibitCount
#             FROM   Artwork
#             GROUP BY  artTitle"""))
#     for row in rs6:
#         print(row)
# print()
#
# print("6. Display the total revenue each exhibit has generated per exhibitID")
# with engine.connect() as con:
#     rs6 = con.execute(text("""SELECT    E.exhibitID, sum(T.transactionPrice)AS TotalRev
#                 FROM Exhibit AS E, SellTo AS S, Customer AS C, Transactions AS T
#                 WHERE 	E.exhibitID = S.exhibitID AND S.customerID = C.CustomerID AND C.customerID = T.customerID
#                 GROUP BY    E.exhibitID"""))
#     for row in rs6:
#         print(row)
# print()
#
# print("7. Display the highest transaction price per medium ")
# with engine.connect() as con:
#     rs7 = con.execute(text(""" SELECT  R.medium, max(T.transactionPrice) AS MaxPrice
#          FROM    Artwork AS R, Transactions AS T
#          WHERE   R.artID = T.artID
#          GROUP BY    R.medium"""))
#     for row in rs7:
#         print(row)
# print()


print("7. Display the highest transaction price per medium ")
with engine.connect() as con:
    rs7 = con.execute(text(""" SELECT  R.medium, max(S.transactionPrice) AS MaxPrice
         FROM    Artwork AS R, SellTo as S
         WHERE   R.exhibitID = S.exhibitID AND R.artID = S.artID
         GROUP BY    R.medium"""))
    for row in rs7:
        print(row)
print()
#
# print("8. Display the names and count of all the artists who have been to the most exhibits sorted by the artist name. ")
# # with engine.connect() as con:
#     rs8 = con.execute(text("""SELECT A.artistName, COUNT(E.exhibitID) AS MostArt
# 	    FROM  Artist AS A, Exhibit AS E, Registered AS G
# 	    WHERE A.artistID = G.artistID AND G.exhibitID = E.exhibitID;
# 	    GROUP BY A.artistName"""))
#     for row in rs8:
#         print(row)
# print()