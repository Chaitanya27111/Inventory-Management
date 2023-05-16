def metadata():
  '''
    Establishes the Master data - Material master and vendor master

    Returns
    -------
    None.

    '''
  import mysql.connector
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jamnagar",
    database="db1"
  )
  cursor = mydb.cursor()
  if (mydb.is_connected()):
    print ("Connected to Database...")

  

    
    query_del = "DROP Table masterdata"
    cursor.execute(query_del)
    
    mquery = 'create table masterdata (item_name varchar(20), item_code varchar(20), base_unit varchar(20) )'
    cursor.execute(mquery)
    query_ins = "INSERT INTO Masterdata (item_name, item_code, base_unit) VALUES(%s,%s,%s)"
    values = [("Coffee", "101", "Kg"), ("Sugar", "102", "Kg"),
              ("Flour", "103", "Kg"), ("Cups", "104", "Units"),
              ("Stirrer", "105", "Units")]
    cursor.executemany(query_ins, values)
    
    cursor.execute("select * from masterdata")
    rec = cursor.fetchall()
    print ("rows = ", cursor.rowcount)
    for row in rec:
      print (row[0]+" "+row[1]+" "+row[2])
    print ("table")

    #vendor table
    #cursor.execute("DROP Table vendor_data")
    #vquery = "CREATE TABLE Vendor_Data (name varchar(100), addr varchar(100), phone varchar(100), fax varchar(100), email varchar(100), inco_term varchar(20), payment_term varchar(20))"
    #cursor.execute(vquery)
    '''
    query_ins = "INSERT INTO Vendor_Data (name, addr, phone, fax, email, inco_term, payment_term) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    values = [('MegaMart Co.', '123 Main St, Anytown, USA', '+1 (555) 123-4567', '+1 (555) 987-6543', 'chaitanya27111@gmail.com', "DDP", "NET30"),  
              ('Greenfields Inc.', '45 Oak Ave, Somewhere, USA', '+1 (555) 987-6543', '+1 (555) 123-4567', 'chaitanya27111@gmail.com', "DDP", "NET30"), 
              ('Best Buy Supplies', '789 Elm St, Nowhere, USA', '+1 (555) 555-1212', '+1 (555) 121-5555','chaitanya.coding@gmail.com', "DDP", "COD"), 
              ('Excelent Deals LLC', '1 Pine St, Everywhere, USA', '+1 (555) 111-2222', '+1 (555) 222-1111','chaitanya.coding@gmail.com', "EXW", "CND"), 
              ('Superior Products Co.', '567 Maple Ave, Anytown, USA', '+1 (555) 555-5555', '+1 (555) 555-5555','chaitanya.coding@gmail.com', "EXW", "CND")]
    cursor.executemany(query_ins, values)

    cursor.execute("select * from Vendor_Data")
    rec = cursor.fetchall()
    print ("rows = ", cursor.rowcount)
    for row in rec:
      print (row[0]+", "+row[1]+", "+row[2]+", "+row[3]+", "+row[4]+", "+row[5]+", "+row[6])
    '''

    '''
    cursor.execute("DESCRIBE Vendor_Data")
    desc = cursor.fetchall()
    print (desc)'''
    '''
    #query = "ALTER TABLE Vendor_Data ADD COLUMN email varchar(100)"
    #cursor.execute(query)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    
    cursor.execute("select * from Vendor_Data")
    print ("rows = ", cursor.rowcount)
    rec = cursor.fetchall()
    for row in rec:
      print (row[0]+", "+row[1]+", "+row[2]+", "+row[3])

    ins_email_query = "INSERT INTO Vendor_Data (email) VALUES(%s)"
    values = ["chaitanya27111@gmail.com", "chaitanya.coding@gmail.com", "chaitanya27111@gmail.com", "chaitanya.coding@gmail.com", "chaitanya.coding@gmail.com"]
    #cursor.executemany(ins_email_query, [(val,) for val in values])
    for email in values:
      cursor.execute(ins_email_query, (email,))
    print ("rows = ", cursor.rowcount)

    cursor.execute("select email from Vendor_Data")
    rec = cursor.fetchall()
    for row in rec:
      #print (row[0]+", "+row[1]+", "+row[2]+", "+row[3])
      print (row)
    
    '''
    mydb.commit()
    print ("table")


def inventory():
  import mysql.connector
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jamnagar",
    database="db1"
  )
  cursor = mydb.cursor()
  if (mydb.is_connected()):
    print ("Connected to Database...")

  '''table_create = "CREATE TABLE Inventory (item_code INT, item_name varchar(40), level INT)"
  cursor.execute(table_create)'''

  query_ins = "INSERT INTO Inventory (item_code, item_name, level) VALUES(%s,%s,%s)"
  values = [(101, "Coffee", 600), (102, "Sugar", 500),
              (103, "Flour", 800), (104, "Cups", 850),
              (105, "Stirrer", 400)]
  cursor.executemany(query_ins, values)
  
  cursor.execute("select * from inventory")
  rec = cursor.fetchall()
  for row in rec:
    print (row)
  mydb.commit()

def transaction_table():
  import mysql.connector
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jamnagar",
    database="db1"
  )
  cursor = mydb.cursor()
  if (mydb.is_connected()):
    print ("Connected to Database...")

  '''table_create = "CREATE TABLE Transactions (RFQ_time varchar(50), Vendor varchar(40), GR_time varchar(50))"
  cursor.execute(table_create)'''
  '''modify_dt = "ALTER TABLE Transactions MODIFY COLUMN PO_time varchar(50), MODIFY COLUMN GR_time varchar(50)"
  cursor.execute(modify_dt)'''
  '''modify_dt = "ALTER TABLE transactions ADD COLUMN id varchar(40) FIRST "
  cursor.execute(modify_dt)'''
  '''qur= "ALTER TABLE Transactions ADD COLUMN PO_time DATETIME AFTER RFQ_time"
  cursor.execute(qur)'''
  #cursor.execute("ALTER TABLE Transactions DROP COLUMN RFQ_time")
  cursor.execute("DELETE FROM Transactions")

  '''query_ins = "INSERT INTO Inventory (item_code, item_name, level) VALUES(%s,%s,%s)"
  values = [(101, "Coffee", 600), (102, "Sugar", 500),
              (103, "Flour", 800), (104, "Cups", 850),
              (105, "Stirrer", 400)]
  cursor.executemany(query_ins, values)
  
  cursor.execute("select * from inventory")
  rec = cursor.fetchall()
  for row in rec:
    print (row)
  mydb.commit()'''
  mydb.commit()
  cursor.execute("describe Transactions")
  rec = cursor.fetchall()
  print (rec)
transaction_table()