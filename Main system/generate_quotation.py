
def quotation(vname, items):
    '''
    Generates the pdf file of the Quoatation for the vendor  based on the rfq provided for that vendor

    Parameters
    ----------
    rfq_fname : string
      
    Returns
    -------
    fname_rfq : string
        name of pdf file generated
    rfq_id : int
        id of the generated RFQ.

    '''
    
    import jinja2
    import pdfkit
    from datetime import datetime, timedelta, date
    from mail_send import connect_to_db
    from mail_send import disconnect_to_db

    #fetching details of item from the database
    mydb = connect_to_db()
    cursor = mydb.cursor()

    item_code=["", "", "", ""]
    item_name=["", "", "", ""]
    item_unit=["", "", "", ""]
    item_qty=["", "", "", ""]
    item_price=["", "", "", ""]
    item_total=["", "", "", ""]
    i=0
    
    s = 0
    ########## change for each vendor###########
    '''item_price[0]=10
    item_price[1]=20
    item_price[2]=0.1
    item_price[0]=15
    item_price[1]=20
    item_price[2]=0.1
    item_price[0]=12
    item_price[1]=18
    item_price[2]=0.1
    item_price[0]=11
    item_price[1]=15
    item_price[2]=0.2'''
    item_price[0]=10
    item_price[1]=15
    '''item_price[2]=0.2'''
    print ("a", type(item_price[0]))
    for key, value in items.items():
        print(key)
        print(value)
        query = f"SELECT * FROM masterdata WHERE item_name = '{key}'"
        print(query)
        cursor.execute(query)
        rec = cursor.fetchall()
        print(rec)

        item_name[i]=rec[0][0]
        item_code[i]=rec[0][1]
        item_unit[i]=rec[0][2]
        item_qty[i]=str(value)+" "+item_unit[i]
        item_total[i]=item_price[i]*value
        print ("b",type(s))
        s = s+item_total[i]
        i=i+1

    vquery = f"SELECT * FROM Vendor_Data where name='{vname}'"
    cursor.execute(vquery)
    rec = cursor.fetchall()
    vendor_name = rec[0][0]
    vendor_addr = rec[0][1]
    vendor_no = rec[0][2]
    vendor_fax = rec[0][3]
    
    payment_term = rec[0][6]
    inco_term = rec[0][5]
    ########## change for each vendor###########
    '''delivery_date = date.today()+timedelta(days=7)
    delivery_date = date.today()+timedelta(days=5)
    delivery_date = date.today()+timedelta(days=6)
    delivery_date = date.today()+timedelta(days=7)'''
    delivery_date = date.today()+timedelta(days=3)

    cmp_name = "Chaitanya Enterprise"
    cmp_addr = "123 Main St., Mumbai, Maharashtra, India, 400001"
    cmp_no = "+91-9876543210"
    cmp_fax = "+91-8765432109"

    ########## change for each vendor###########
    '''delivery_charge = 200
    delivery_charge = 250
    delivery_charge = 300
    delivery_charge = 275'''
    delivery_charge = 300
    tax = 18
    subtotal=s
    net_amt = s+delivery_charge+tax*(s+delivery_charge)/100
    tax = str(tax)+'%'


    d = datetime.now()
    i = str(d)
    rfq_id = ''
    for n in i:
        if (n.isnumeric()):
            rfq_id=rfq_id+n
    
    fname_rfq = rfq_id+'_Quotation '+vname+'.pdf'
    rfq_id = int(rfq_id)
    print ("RFQ id: ", rfq_id)
    
    context = {"vendor_name":vendor_name, 'vendor_addr':vendor_addr,
            'vendor_no':vendor_no, 'vendor_fax':vendor_fax,
            'cmp_name':cmp_name, 'cmp_addr':cmp_addr,
            'cmp_no':cmp_no, 'cmp_fax':cmp_fax,
            'payment_term':payment_term, 'inco_term':inco_term,
            'delivery_date':delivery_date,
            'item1_code':item_code[0], 'item1_name':item_name[0], 'item1_qty':item_qty[0], 'item1_price':item_price[0], 'item1_total':item_total[0],
            'item2_code':item_code[1], 'item2_name':item_name[1], 'item2_qty':item_qty[1], 'item2_price':item_price[1], 'item2_total':item_total[1],
            'item3_code':item_code[2], 'item3_name':item_name[2], 'item3_qty':item_qty[2], 'item3_price':item_price[2], 'item3_total':item_total[2],
            'item4_code':item_code[3], 'item4_name':item_name[3], 'item4_qty':item_qty[3], 'item4_price':item_price[3], 'item4_total':item_total[3],
            'delivery':delivery_charge, 'tax':tax, 'subtotal':subtotal, 'net_amt':net_amt}

    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template('Quotation_format.html')
    output_text = template.render(context)
    print ("strt")
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    pdfkit.from_string(output_text, f'{fname_rfq}', configuration=config)
    print ("end")
    disconnect_to_db(mydb, cursor)
    return fname_rfq,rfq_id

def connect_to_db():
    '''
    Establishes connection with the database

    Returns
    -------
    mydb : object
        database object.

    '''
    
    import mysql.connector

    

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root", 
        password = "jamnagar",
        database = "db1"
    )
    if (mydb.is_connected()):
        print ("\nConnected to Database...\n")

        
        return mydb
    else:
        print ("\nXXXXXXXXX Error in Connecting to Database XXXXXXXXX\n")

        

        return None
    
def read_items():
    import json

    # Define the file path
    file_path = "items_dict.json"

    # Open the file in read mode
    with open(file_path, 'r') as f:
        # Load the JSON data from the file
        it = json.load(f)

    items={'Coffee':0, 'Sugar':0, 'Flour':0, 'Cups':0}
    i=0
    for key, value in items.items():
        items[key] = int(float(it['predictions'][i]['labels'][0]['results'][0]['value']))
        i = i+1
    # Print the data
    #print(data)
    return items

def items_order(items):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    items_to_order = {}
    i=0
    for item_name, net_qty_req in items.items():
        query = f"SELECT level from Inventory where item_name = '{item_name}' "
        cursor.execute(query)
        rec = cursor.fetchall()
        #print(rec[0])
        current_lvl = rec[0][0]
        print (current_lvl)
        required_qty = net_qty_req-current_lvl
        if (required_qty>0):
            items_to_order[item_name] = required_qty
        i = i+1
    return items_to_order


#print (quotation('Superior Products Co.'))
#print (quotation('Greenfields Inc.', items))
it = read_items()
items=items_order(it)
print ("items: ")
print (it)
print (items)
print (quotation('Superior Products Co.', items))