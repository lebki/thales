import xml.etree.ElementTree as ElementTree
from dbconn import *

db_results = []
xml_results = []
xml_result_count = 0

results_in_db = [] # dla wyników, które sa w xml i pojawiły się w bazie
results_not_in_db = [] # dla wyników, które nie pojawiły się w bazie a są w XML
tree = 0
root = 0

db = DB()
def compare_results(xml, db):
    for xml_el in xml:
        for db_element in db:
            if xml_el == db_element:
                results_in_db.append(xml_el)
            else:
                results_not_in_db.append(xml_el)

    for element in results_in_db:
        print("Results written into DB: {0}".format(element))

    print("Summary: Results that, should be in DB: {0}. Results currently written into DB {1}".format(len(xml_results),len(results_in_db)))

def read_db_data(cursor):
    try:
        cursor.execute("""SELECT * FROM measure.measure_configurations;""")
        rows = cursor.fetchall()
        print("The results size: {0}".format(len(rows)))
    except Exception as e:
        print("Error while fetching the cursor {0}".format(e))

def read_file(file):
    try:
        f = open(file, "r")
        for line in f:
            db_result = f.readline()
            if(len(db_result)>0):
                db_results.append(db_result.rstrip()) #rstrip ucina znak końca linii
    except FileExistsError:
        print("Brak pliku")

def read_xml(xml_file):
    global counter
    global failCounter
    print("Try to open the xml file")
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()
    counter = 0
    failCounter = 0
    for elements in root.iter('Event'):
        counter+=1
        description = elements.find('Description').text
        category = elements.find('Category').text
        xml_results.append(description)
        print("NR[{0}] Name: {1} Category: {2}".format(counter,description,category))

        if category =='failure':
            failCounter+=1 #fail count increase

    print("---------------------------------------------------------------------------------------------------------")
    print("Global stats: Failures {0} Others {1} All {2}".format(failCounter,(counter-failCounter),counter))

db.conn_with_db("mdc_db", "mdc", "mdc_mdc", "192.168.10.203")
#read_db_data(db.cursor)
read_file('db_results.txt')
for element in db_results:
    print(element)
read_xml('dictionary.xml')

compare_results(xml_results,db_results)