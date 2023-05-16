
import logging as log
log.basicConfig(filename="main.log", filemode='w', level=log.DEBUG)
#this is used to generate a log file named main.log

def connect_to_db():
    '''
    Establishes connection with the database

    Returns
    -------
    mydb : object
        database object.

    '''
    log.info("Started connect_to_db()")

    import mysql.connector

    log.info("Imports successfull")

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root", 
        password = "jamnagar",
        database = "db1"
    )
    if (mydb.is_connected()):
        print ("\nConnected to Database...\n")

        log.info("Connected to Database...")

        return mydb
    else:
        print ("\nXXXXXXXXX Error in Connecting to Database XXXXXXXXX\n")

        log.error("Cannot connect to Database")

        return None
    
def disconnect_to_db(mydb, cursor):
    '''
    Disconnects from the database. 

    Parameters
    ----------
    mydb : object
        Database object.
    cursor : cursor
        Cursor to the database.

    Returns
    -------
    None.

    '''
    log.info("Started disconnect_to_db")
    mydb.close()
    cursor.close()
    log.info("Disconnected from database")

def reading_pdf(pdf_name):
    '''
    Extracts required data from the passed file
    Parameters
    ----------
    pdf_name : string
        Name of the file to be read.

    Returns
    -------
    l_code : list
        list of the item codes.
    l_name : list
        list of item names.
    l_quant : list
        list of the item quantities.
    l_unit_price : list
        list of item unit price.
    l_item_total : list
        list of item totals.
    net_amt : float
        Net amount payable.
    payment_terms : string
    inco_terms : string
    delivery_dt : string
    subtotal : float
    tax : float
    delivery_charge : float
    vname: string
        name of the vendor mentioned in the RFQ
    '''
    log.info("Started reading_pdf()")
    import tabula
    import PyPDF2
    import pandas as pd
    log.info("Imports successfull")
    # read PDF file into list of DataFrame objects
    tables = tabula.read_pdf(pdf_name, pages='all', multiple_tables=True)
    l_code = tables[4]['Item Code'].str.split('\r')
    print (l_code[0])
    l_name = tables[4]['Item Name'].str.split('\r')
    print (l_name[0])
    l_quant = tables[4]['Quantity'].str.split('\r')
    print (l_quant[0])
    l_unit_price = tables[4]['Unit Price'].str.split('\r')
    print (l_unit_price)
    l_item_total = tables[4]['Item Total'].str.split('\r')
    print (l_item_total)
    payment_terms = tables[3]['Payment Terms']
    print ("paymt term", payment_terms[0])
    inco_terms = tables[3]['Inco Terms']
    print ("inco term", inco_terms[0])
    delivery_dt = tables[3]['Delivery Date']
    print ("paymt term", delivery_dt[0])
    vname_str = tables[1]["Vendor"]
    print("***********", type(vname_str[0]))
    cmp_name_str = vname_str.str.split('\r')[0][0]
    pat = "Company Name: "
    strt_ind = cmp_name_str.find(pat)
    vname = cmp_name_str[strt_ind + len(pat) :]
    print(vname)


    pdf = open(pdf_name, 'rb')
    pdf_obj = PyPDF2.PdfReader(pdf)
    pg = pdf_obj.pages[0]
    text = pg.extract_text()
    pattern = 'Net Amount:'
    start_index = text.find(pattern)
    net_amt_str = text[start_index + len(pattern) :]
    net_amt = float(net_amt_str.split()[0])
    print (net_amt)

    pattern = 'Subtotal:'
    start_index = text.find(pattern)
    subtotal_str = text[start_index + len(pattern) :]
    subtotal = float(subtotal_str.split()[0])
    print (subtotal)

    pattern = 'Tax:'
    start_index = text.find(pattern)
    tax_str = text[start_index + len(pattern) :]
    tax = (tax_str.split()[0])
    tax = float(tax[:len(tax)-1])
    print (tax)

    pattern = 'Delivery:'
    start_index = text.find(pattern)
    delivery_str = text[start_index + len(pattern) :]
    delivery_charge = float(delivery_str.split()[0])
    print (delivery_charge)
    return l_code[0], l_name[0], l_quant[0], l_unit_price[0], l_item_total[0], net_amt, payment_terms[0], inco_terms[0], delivery_dt[0], subtotal, tax, delivery_charge, vname

def conv_po_pdf(fname):
    '''
    Generates the pdf file of the Purchase Order based on the Quoataion PDF provided to it. 
    The quotation PDF is of the winning vendor. The function identifies by itself the items to be ordered from the quotation 
    and their price.
    
    Parameters
    ----------
    fname : string
        eg. 20230410234917844994_Quotation Superior Products Co.
    vname : string
        name of the vendor to whom the PO is to be mailed.

    Returns
    -------
    fname_po : string
        name of pdf file generated
    po_id : int
        id of the generated PO.

    '''
    log.info(f"Started conv_po_pdf() on {fname}")
    import jinja2
    import pdfkit
    from datetime import datetime
    import re
    log.info("Imports successfull")

    '''
    d = datetime.now()
    i = str(d)
    po_id = ''
    for n in i:
        if (n.isnumeric()):
            po_id=po_id+n
    '''
    item_code=["", "", "", ""]
    item_name=["", "", "", ""]
    item_unit=["", "", "", ""]
    item_qty=["", "", "", ""]
    item_price=["", "", "", ""]
    item_total=["", "", "", ""]

    po_id_list = re.split(r'[_ ]', fname)
    po_id = po_id_list[0]
    print ("PO id",po_id_list)
    vname = " ".join(po_id_list[2:-1]) + " "+po_id_list[-1][:-4]
    log.info(f"Winning vendor name: {vname}")
    fname_po = po_id+'_PO.pdf'
    log.info(f"PO filename: {fname_po}")
    po_id = int(po_id)
    log.info(f"PO id: {po_id}")
    mydb = connect_to_db()
    cursor = mydb.cursor()
    log.info("Back to conv_po_pdf()")
    log.info(f"Extracting data from {fname}")
    '''item_code = ["--", "--", "--", "--"]
    item_name = ["--", "--", "--", "--"]
    item_qty = ["--", "--", "--", "--"]
    item_price = ["--", "--", "--", "--"]
    item_total = ["--", "--", "--", "--"]'''

    d = datetime.now()
    formatted_datetime = d.strftime('%d-%m-%Y %H:%M:%S')
    print (formatted_datetime)
    #ins_quer_transaction = f"INSERT INTO Transactions (id, PO_time) VALUES (%s, %s)"
    ins_quer_transaction = f"UPDATE Transactions SET PO_time = %s where id = %s"
    cursor.execute(ins_quer_transaction, (d, po_id))
    mydb.commit()
    rec = cursor.fetchall()
    print (rec)


    item_code, item_name, item_qty, item_price, item_total, net_amt, payment_term, inco_term, delivery_date, subtotal, tax, delivery_charge, v = reading_pdf(fname)
    item_code.extend([""]*(4-len(item_code)))
    item_name.extend([""]*(4-len(item_name)))
    item_qty.extend([""]*(4-len(item_qty)))
    item_price.extend([""]*(4-len(item_price)))
    item_total.extend([""]*(4-len(item_total)))
    log.info("Back to conv_po_pdf()")
    item_name = list(item_name)
    i=0
    for key in item_name:
        print(key)
        query = f"SELECT * FROM masterdata WHERE item_name = '{key}'"
        print(query)
        cursor.execute(query)
        rec = cursor.fetchall()
        print(rec)

        #item_name[i]=rec[0][0]
        #item_code[i]=rec[0][1]
        #item_unit[i]=rec[0][2]
        #item_qty[i]=str(item_qty[i])+" "+item_unit[i]

        ##############get form the rfq, for this u need rfqid as input arg.
        i=i+1

    #############get these details from the awarded RFQ
    print ("***",item_code[0])
    print ("***",item_name[0])
    print ("***",item_price[0])
    print ("***",item_qty[0])
    print ("***",item_total[0])
    print ("***",item_unit[0])
    
    vquery = f"SELECT * FROM Vendor_Data where name='{vname}'"
    cursor.execute(vquery)
    rec = cursor.fetchall()
    print(rec)
    print (vname)
    vendor_name = rec[0][0]
    vendor_addr = rec[0][1]
    vendor_no = rec[0][2]
    vendor_fax = rec[0][3]

    cmp_name = "Chaitanya Enterprise"
    cmp_addr = "123 Main St., Mumbai, Maharashtra, India, 400001"
    cmp_no = "+91-9876543210"
    cmp_fax = "+91-8765432109"


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

    template = template_env.get_template('PO_format.html')
    output_text = template.render(context)
    print ("strt")
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    pdfkit.from_string(output_text, f'{fname_po}', configuration=config)
    print ("end")
    disconnect_to_db(mydb, cursor)

    log.info("Back to conv_po_pdf()")
    log.info("Operation successfull from conv_po_pdf")
    return fname_po,po_id

def conv_rfq_pdf(items, vname):
    '''
    Generates the pdf file of the Request for Quotation(RFQ) based on the items list and the vendor name provided.

    Parameters
    ----------
    items : Dictionary
        {"name":qty}
                qty : int.
    vname : string
        name of the vendor to whom the PO is to be mailed.

    Returns
    -------
    fname_rfq : string
        name of pdf file generated
    rfq_id : int
        id of the generated RFQ.

    '''
    
    import jinja2
    import pdfkit
    from datetime import datetime
    import smtplib

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
        item_price[i]=""
        item_total[i]=""
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
    delivery_date = ''

    cmp_name = "Chaitanya Enterprise"
    cmp_addr = "123 Main St., Mumbai, Maharashtra, India, 400001"
    cmp_no = "+91-9876543210"
    cmp_fax = "+91-8765432109"

    delivery_charge = ''
    tax = ''
    subtotal = ''


    d = datetime.now()
    i = str(d)
    rfq_id = ''
    for n in i:
        if (n.isnumeric()):
            rfq_id=rfq_id+n

    

    fname_rfq = rfq_id+'_RFQ.pdf'
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
            'delivery':delivery_charge, 'tax':tax, 'subtotal':subtotal}

    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template('RFQ_format.html')
    output_text = template.render(context)
    print ("strt")
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    pdfkit.from_string(output_text, f'{fname_rfq}', configuration=config)
    print ("end")
    disconnect_to_db(mydb, cursor)
    return fname_rfq,rfq_id

# mailing
def mail(fname, ereceiver, esubject, ebody):
    '''
    Mails the file.

    Parameters
    ----------
    fname : string
        Name of the file to be mailed.
    ereceiver : string
        email id  of receiver.
    esubject : string
        Subject of the mail.
    ebody : string
        Body of the mail.

    Returns
    -------
    None.

    '''
    import yagmail
    esender   = 'chaitanya.coding@gmail.com'
    print (esender)
    yag = yagmail.SMTP(esender, 'mokklygwarbaigky')
    print (ereceiver)
    yag.send(to=ereceiver, subject=esubject, contents=ebody, attachments=fname)
    print (esubject)
    yag.close()
    
    
    '''import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.application import MIMEApplication

    # Set up email details
    sender = 'chaitanya.coding@gmail.com'
    recipient = ereceiver
    subject = esubject
    body = ebody
    attachment_file = fname

    # Create a multi-part message container
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    # Attach the message body
    msg.attach(MIMEText(body))

    # Attach the file
    with open(attachment_file, 'rb') as f:
        part = MIMEApplication(f.read(), Name=attachment_file)
        part['Content-Disposition'] = f'attachment; filename="{attachment_file}"'
        msg.attach(part)

    # Connect to the SMTP server and send the message
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'chaitanya.coding@gmail.com'
    smtp_password = 'mokklygwarbaigky'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, recipient, msg.as_string())
    '''

#fname, po_id= conv_rfq_pdf()
#print (fname, po_id)
#mail(f'{fname}','chaitanya27111@gmail.com','Test2','PFA the PO')

def mail_rfq(fname, vname):
    '''
    Mails the RFQ to the specified vendor using mail() function

    Parameters
    ----------
    fname : string
        Name of file to be mailed.
    vname : string
        Name of the file to whom the file is to be mailed.

    Returns
    -------
    None.

    '''
    mydb = connect_to_db()
    cursor = mydb.cursor()
    '''cursor.execute("select name, email from Vendor_Data")
    rec = cursor.fetchall()
    for row in rec: 
        esub = "Request for Quotation"
        ebody = f"Dear {row[0]},\n PFA the Request for Quotation.\nHoping to hear from you soon.\nRegards\nChaitanya Enterprise"
        ereceiver = row[1]
        mail(fname, ereceiver, esub, ebody)'''
    query = f"SELECT name, email FROM Vendor_Data WHERE name = '{vname}'"
    cursor.execute(query)

    row = cursor.fetchall()
    print ("row=", row)
    esub = "Request for Quotation"
    ebody = f"Dear {row[0][0]},\n PFA the Request for Quotation.\nHoping to hear from you soon.\nRegards\nChaitanya Enterprise"
    ereceiver = row[0][1]
    mail(fname, ereceiver, esub, ebody)
    disconnect_to_db(mydb, cursor)

def mail_po(fname, vname):
    '''
    Mails the PO to the specified vendor using mail() function

    Parameters
    ----------
    fname : string
        Name of file to be mailed.
    vname : string
        Name of the file to whom the file is to be mailed.

    Returns
    -------
    None.

    '''
    mydb = connect_to_db()
    cursor = mydb.cursor()
    '''cursor.execute("select name, email from Vendor_Data")
    rec = cursor.fetchall()
    for row in rec: 
        esub = "Request for Quotation"
        ebody = f"Dear {row[0]},\n PFA the Request for Quotation.\nHoping to hear from you soon.\nRegards\nChaitanya Enterprise"
        ereceiver = row[1]
        mail(fname, ereceiver, esub, ebody)'''
    query = f"SELECT name, email FROM Vendor_Data WHERE name = '{vname}'"
    cursor.execute(query)

    row = cursor.fetchall()
    print ("row=", row)
    esub = "Purchase Order"
    ebody = f"Dear {row[0][0]},\nWe are glad to inform you that your company has won the contract. PFA the Purchase Order.\nHoping to have a good busineess with you.\nRegards\nChaitanya Enterprise"
    ereceiver = row[0][1]
    mail(fname, ereceiver, esub, ebody)
    disconnect_to_db(mydb, cursor)

def mail_all_vendors(items):
    '''
    Generates the RFQs of all vendors using conv_rfq_pdf() and mails the RFQ to all vendors using mail_rfq() function

    Parameters
    ----------
    items : dictionary
        list of items based on which the PO is to be generated
        {"item_name":qty}
        qty - int.

    Returns
    -------
    rfq_ids : list[int]
        IDs of the generated RFQs.
    fname : list[string]
        Name of the RFQ files generated.

    '''
    log.info("Started mail_all_vendors()")
    mydb = connect_to_db()
    query = "SELECT name FROM Vendor_Data"
    cursor = mydb.cursor()
    cursor.execute(query)
    rec = cursor.fetchall()
    i=0
    fnames = []
    rfq_ids = []
    for vname in rec:
        vname = vname[0]
        fname, rfq_id = conv_rfq_pdf(items, vname)
        fnames.append(fname)
        rfq_ids.append(rfq_id)
        mail_rfq(fname, vname)
    disconnect_to_db(mydb, cursor)
    log.info("Mailed RFQs to all vendors")
    return rfq_ids, fnames

def download_attachment(vname, rfq_id):
    '''
        Downloads the attachment from the mail of specified vendor
        
        Parameters
        ----------
        vname : string
            Name of the vendor.
        rfq_id : int
            id of the RFQ to that vendor

        Returns
        -------
        filename : string
            Name of the downloaded file.
    '''
    import imaplib
    import email

    # Set up IMAP details
    imap_server = 'imap.gmail.com'
    imap_port = 993
    imap_username = 'chaitanya.coding@gmail.com'
    imap_password = 'mokklygwarbaigky'

    # Connect to the IMAP server and select the inbox folder
    with imaplib.IMAP4_SSL(imap_server, imap_port) as mail:
        mail.login(imap_username, imap_password)
        mail.select('inbox')

        # Search for emails with the desired subject
        srch_str = vname+" Quotation "+str(rfq_id)
        search_criteria = f'SUBJECT "{srch_str}"'
        status, msg_ids = mail.search(None, search_criteria)
        print(msg_ids)
        print ("in")
        # Get the most recent email message
        msg_id_list = msg_ids[0].split()
        latest_msg_id = msg_id_list[-1]
        status, msg_data = mail.fetch(latest_msg_id, '(RFC822)')
        raw_email = msg_data[0][1]

        # Parse the email message with the email library
        email_msg = email.message_from_bytes(raw_email)

        # Look for attachments and download them
        for part in email_msg.walk():
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                if filename:
                    with open(filename, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    print(f'Downloaded attachment: {filename}')
    return filename

def winning_vendor (rfq_ids):
    """Downloads the quotations from all vendors and finds the vendor who has won the bid

    Args:
        rfq_ids (list): list of the RFQ ids of all the vendors
    """    
    log.info("Started winning_vendor()")
    mydb = connect_to_db()
    cursor = mydb.cursor()
    query = "SELECT name from Vendor_Data"
    cursor.execute(query)
    row = cursor.fetchall()
    i=0
    win_vendor = ""
    win_rfq_id = -1
    win_fname = ""
    min_amt = 999999999
    for vname_tup in row:
        vname = vname_tup[0]
        print (vname)
        fname = download_attachment(vname, rfq_ids[i])
        print (fname)
        l = reading_pdf(fname)
        print (l)
        net_amt = l[5]
        print(net_amt)
        if (net_amt<min_amt):
            min_amt = net_amt
            win_vendor = vname
            win_rfq_id = rfq_ids[i]
            win_fname = fname
        i=i+1
    print ("Winning vendor: ", win_vendor)
    log.info(f"Winning vendor: {win_vendor}")
    log.info(f"Winning RFQ id: {win_rfq_id}")
    log.info(f"Winning RFQ File name : {win_fname}")
    win_rfq_id_str = str(win_rfq_id)
    insert_vendor = f"INSERT INTO Transactions (id, vendor) VALUES(%s, %s)"
    #insert_vendor = f"UPDATE Transactions SET vendor = %s where id = %s"
    cursor.execute(insert_vendor, (win_rfq_id_str,win_vendor))
    mydb.commit()
    disconnect_to_db(mydb, cursor)
    return win_vendor, win_rfq_id, win_fname

def change_quot_name(rfq_ids):
    '''returns = list of new filenames'''
    import os
    mydb = connect_to_db()
    cursor = mydb.cursor()
    fnames = []
    query = "SELECT name FROM Vendor_Data"
    cursor.execute(query)
    row = cursor.fetchall()
    i=0
    for vname_l in row:
        vname = vname_l[0]
        print(vname)
        folder_path = "D:/study PDF/SAP/SAP BTP/Demand forecasting project/Python_related"
        #old_pattern = 'change'
        old_pattern = "_Quotation " + vname

        for filename in os.listdir(folder_path):
            if old_pattern in filename:
                old_path = os.path.join(folder_path, filename)
                new_name = str(rfq_ids[i])+"_Quotation " + vname + ".pdf"
                i=i+1
                fnames.append(new_name)
                new_filename = filename.replace(filename, new_name)
                new_path = os.path.join(folder_path, new_filename)
                os.rename(old_path, new_path)
    return fnames

#change_quot_name([1, 2, 3, 4, 5])
#print (winning_vendor([20230410235402773474, 20230410235604203413, 20230410235800802903, 20230411000042612176, 20230410234917844994]))
def mail_from_vendors(fnames):

    mydb = connect_to_db()
    cursor = mydb.cursor()
    query = "SELECT name FROM Vendor_Data"
    cursor.execute(query)
    row = cursor.fetchall()
    i=0
    for vname_l in row:
        vname = vname_l[0]
        esub = vname + ' Quotation ' + fnames[i][:20]
        print (f"fname={fnames[i]}  esub = {esub}")
        eb = "Dear Chaitanya Enterprise\nGreetings of the Day!\nPFA the quotation in responst to the RFQ shared with us.\n\nThank you\nRegards"
        mail(fname=fnames[i], ereceiver='chaitanya.coding@gmail.com', esubject=esub, ebody=eb)
        i=i+1

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

def goods_receipt(id):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    from datetime import datetime
    print ("\n\n*********************Goods Receipt***********************\n\n")
    print ("Are the goods received?(y/n) : ")
    res = input().lower()
    while (res!='y'):
        print ("Are the goods received?(y/n) : ")
        res = input().lower()
    
    d = datetime.now()
    qur = f"UPDATE Transactions SET GR_time = %s where id = %s"
    cursor.execute(qur, (d, id))
    mydb.commit()

    
def main():

    print ("Type of Transaction: \npress 1 - Ordering new items\npress 2 - Goods Receipt\npress 3 - Viewing Transaction history")
    sel = int(input())
    if (sel == 1):
        it = read_items()
        print ("Predicted values: - ")
        for k, v in it.items():
            print (k, v, sep=": ")
        ito = items_order(it)
        print ("Items to be ordered: -")
        for k, v in ito.items():
            print (k, v, sep=": ")

        rfq_ids, fnames = mail_all_vendors(ito)
        print (rfq_ids)
        new_names = change_quot_name(rfq_ids)
        mail_from_vendors(new_names)
        win_vname, win_rq_id, win_rfq_fname = winning_vendor(rfq_ids)
        po_fname, po_id = conv_po_pdf(win_rfq_fname)
        mail_po(po_fname, win_vname)
    
    elif (sel == 2):
        print ("Enter the ID of PO: ")
        id = input ()
        goods_receipt(id)

    else:
        mydb  = connect_to_db()
        cursor = mydb.cursor()
        from tabulate import tabulate

        qur = "SELECT * from Transactions"
        cursor.execute(qur)
        rec = cursor.fetchall()
        cols = [col[0] for col in cursor.description]
        table = tabulate(rec, headers = cols, tablefmt="fancy_grid")
        print (table)

        
    
'''def test():
    it = read_items()
    print ("Predicted values: - ")
    for k, v in it.items():
        print (k, v, sep=": ")
    ito = items_order(it)
    print ("Items to be ordered: -")
    for k, v in ito.items():
        print (k, v, sep=": ")
    for item in it["predictions"]:
        l = item['labels']
        res = l[0]['results']
        print(res[0]['value'])'''
        
def test():
    mydb = connect_to_db()
    cursor = mydb.cursor()
    conv_po_pdf("20230515111647871128_Quotation Superior Products Co..pdf")
    qur = "SELECT * from Transactions"
    cursor.execute(qur)
    rec = cursor.fetchall()
    print (rec)

if __name__ == '__main__':
    main()
    #test()

















'''
items={'Sugar':500, 'Flour':100, 'Cups':10000}
vname = 'Superior Products Co.'
print (conv_po_pdf("20230410234917844994_Quotation Superior Products Co..pdf"))
'''
#print (conv_rfq_pdf(d, vname) )  
'''d={'Sugar':50, 'Flour':"10", 'Cups':10000}
vname = 'Superior Products Co.'

#mail_all_vendors(d)
fname, po_id = conv_po_pdf(d, vname)
print ("typ=",fname)
mail_po(fname, vname)
print (fname)
#mail_rfq(fname)
'''
