from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib #Only for parse.unquote and parse.unquote_plus.
import json
import base64
from typing import Union, Optional
import re
# If you need to add anything above here you should check with course staff first.

sale = ""
next_id = 2 # we have two test rows
contacts = []
contacts.append({"ID" : 1, "name" : "George", "email" : "george@google.com", "delivery_date" : "2023-12-10", "phone_model" : "Samsung S23 Ultra", "case" : "No"})
contacts.append({"ID" : 2, "name" : "Suleyman", "email" : "suley@boston.com", "delivery_date" : "2023-11-10", "phone_model" : "Pixel 8", "case" : "Yes"})

def extractPOST(arg_list):
    contact = {}
    for i in range(len(arg_list)):
        arg_list[i] = urllib.parse.unquote_plus(arg_list[i], encoding='utf-8')
        equals = arg_list[i].find("=")
        

        if arg_list[i][equals + 1:] == "on":  # if "case=on", change it to "case = yes"
            contact[arg_list[i][:equals]] = "Yes"
        else:
            contact[arg_list[i][:equals]] = arg_list[i][equals + 1:]

    global next_id  
    next_id = next_id+ 1
    contact["ID"]  = next_id 
    
    if contact.get("case") == None: # if case was not checked, add "case = No"
        contact['case'] = 'No'
    return contact

def testParam(contact):
    goodKeys = ['name', 'email', 'delivery_date', 'phone_model', 'case', 'order', 'ID']
    phones = ["iPhone 15 Pro Max", "iPhone 15", "S23 Ultra", "S23+", "OnePlus 12 5G", "Pixel 8"]
    data_recieved = True

    for i in contact: # check for garbage keys or empty values
        if "&" in i or "+" in i or "$" in i or (i not in goodKeys):
            return False
        if isinstance(contact[i], str) and contact[i] == "":  # if any key's don't have a value
            return False
        if isinstance(contact[i], int) and (contact[i] < 0 or contact[i] > 5000): # if negative num or > 5000, return False
            return False
        if not isinstance(contact[i], str) and not isinstance(contact[i], int):  # if the value type is not int or str, then return false
            # print("\n{}  and  {}\n".format(isinstance(contact[i], str), isinstance(contact[i], str)))
            return False
    
    # # check to see that each of these keys are in the dictionary
    # if contact.get("name") and contact.get("email") and contact.get("delivery_date") and contact.get("phone_model") and contact.get("case"):
    #     data_recieved = True
    # if any of the keys don't have a value, the data is not recieved
    # if contact.get("name")=="" or contact.get("email")=="" or contact.get("delivery_date")=="" or contact.get("phone_model")=="" or contact.get("case")=="":
    #     data_recieved = False
    
    # check that the Name, Email, and aren't too long
    # check Phone Model is valid, and Case is either Yes or No
    if (len(contact.get("email")) < 5 or len(contact.get("email")) > 40 or len(contact.get("name")) > 40 ):
        data_recieved = False
    if (contact.get("case") != "Yes" and contact.get("case") != "No"):
        data_recieved = False
    if (contact.get("phone_model") not in phones):
        data_recieved = False

    # check if the email is an actual email and not too long or too short
    # 1. emails should have only one "@"
    if (contact.get("email").count("@") != 1):
        data_recieved = False
    
    # 2. if emails doesn't end with a proper domain suffix
    if len(contact.get("email")) > 4:
        if contact.get("email")[-4] not in ".com.net.gov.edu.org" :
            data_recieved = False
    
    # check if the date format is YYYY-MM-DD  like 2023-10-30 -> Oct 30
    date = contact.get("delivery_date").split("-")    
    date = [int(date[0]), int(date[1]), int(date[2])]
    if len(date) != 3:
        data_recieved = False
    if (date[0] > 2000 and date[0] < 2500 and date[1] > 0 and date[1] <= 12 and date[2] > 0 and date[2] <= 31):
        pass
    else:
        data_recieved = False
    return data_recieved


def dynamicContactlog():
    table = ""
    if (len(contacts) > 0):
        for i in contacts:
            table += """
                <tr id="row" class="{}">
                    <td>{}</td>
                    <td><a href="mailto:{}">{}</a></td>
                    <td id="date">{}</td>
                    <td id="timeTill"></td>
                    <td>{}</td>
                    <td>{}</td>
                    <td><button id="delete">Delete</button></td>
                </tr>
            """.format(i["ID"], i["name"], i["email"], i["email"], i["delivery_date"], i["phone_model"], i["case"])

    htmlFirstHalf = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Unfulfilled Orders</title>
        <link id="stylesheet" rel="stylesheet" href="/main.css">
        <script defer src="/js/main.js"></script>
        <script defer src="/js/table.js"></script>
    </head>
    <body>
        <div class="nav_links">
            <ul>
                <li><a href="http://localhost:4131/main">Home Page</a></li>
                <li><a href="http://localhost:4131/contact">Contact us</a></li>
                <li><a href="http://localhost:4131/testimonies">Testimonials</a></li>
                <li><a href="http://localhost:4131/admin/contactlog">Contacts List</a></li>
                <li><button id="toggle">Toggle</button></li>
            </ul>
        </div>
        <span id="sale"></span>
        

        <div id="set-sale-div">
            <p id="set-sale">Set sale</p>
            <label>Sale description:</label>
            <input type="text" name="sale-content" id="sale-content">
            <div id="buttons">
                <button id="sale-start">Set</button>
                <button id="sale-end">Delete</button>
            </div>
        </div>
        <h1>Unfulfilled Orders</h1>
        <span id="confirmationSale"></span>
        <span id="confirmationRowDel"></span>
        <div class="table">
            <table>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Delivery Date</th>
                    <th>Promised to deliver in</th>
                    <th>Phone</th>
                    <th>Ship with Case</th>
                    <th>Delete Row</th>
                </tr>
            """

    htmlSecondHalf = """
            </table>
        </div>
    </body> 
</html>
                """
    
    return htmlFirstHalf + table + htmlSecondHalf


def adminAuthentication(headers): # m, r, h are the user protected response :message, response code, and header
    if headers.get("Authorization") and headers.get("Authorization").startswith("Basic "): 
        userPass = ""
        try:
            userPass = base64.b64decode((headers.get("Authorization"))[6:]).decode("utf-8")
        except:
            return json.dumps({"Authenticatation":'Bad encryption encoding'}), 403, {"Content-Type":"text/html; charset=utf-8"}
        idx = userPass.find(":")
        # print("\n" + userPass + "\n")
        if userPass[:idx] == "admin" and userPass[idx + 1:] == "password":
            return " ", " ", " "
        else:
            return json.dumps({"Authenticatation":'Wrong username or password'}), 403, {"Content-Type":"text/html; charset=utf-8"}
    else:
        return json.dumps({"Privilaged Access": "Credentials?"}), 401, {"Content-Type": "text/html; charset=utf-8" ,"WWW-Authenticate":'Basic realm="User Visible Realm"'}


# The method signature is a bit "hairy", but don't stress it -- just check the documentation below.
def server(method: str, url: str, body: Optional[str], headers: dict[str, str]) -> tuple[Union[str, bytes], int, dict[str, str]]:    
    """
    method will be the HTTP method used, for our server that's GET, POST, DELETE url is the partial url, just like seen
    in previous assignments body will either be the python special None (if the body wouldn't be sent) or the body will
    be a string-parsed version of what data was sent. headers will be a python dictionary containing all sent headers.
    
    This function returns 3 things:
    The response body (a string containing text, or binary data)
    The response code (200 = ok, 404=not found, etc.)
    A _dictionary_ of headers. This should always contain Content-Type as seen in the example below.
    """
    # Parse URL -- this is probably the best way to do it. Delete if you want.
    # url, *parameters = url.split("?", 1)
    global sale
    idx, link = 0, ""
    if (len(url) >= 1):
        idx = max(url.find("?"), url.find("#"))  # Link, query_params = url.split(‘?’, 1)
        if idx == -1:
            link = url
        else:
            link = url[:idx]    # return the site portion to return

    # if the request i sot access these endpoints, ask for authorization
    if (link == "/api/contact" and method == "DELETE") or (link == "/api/sale" and method == "DELETE") or (link == "/api/sale" and method == "POST") or  (link == "/admin/contactlog" and method == "GET"):
        m, r, h = adminAuthentication(headers)
        # if there is no authorization, return with the proper response
        if m != " " and r != " " and h != " ":
            return m, r, h

        
    if method == "POST":
        arg_list = []
        if (len(body) >= 1):
                arg_list = body.split("&")

        # only check the parameters of the website if they come from the contact page
        contact = {}
        data_recieved = False
        if url == "/contact" and len(arg_list) > 0: 
            contact = extractPOST(arg_list)
            # only add the data to contats if all data is recieved correctly
            data_recieved = testParam(contact)
            if data_recieved:
                contacts.append(contact)
            print("    good data?  {}\n".format(data_recieved))
            print("    info in contact: {}\n\n".format(contact))
            arg_list = []

        if "api" in link and (body and len(body.strip()) > 0):
            body = json.loads(body)
        # API   
        if link == "/api/sale":
            if not headers.get("Content-Type") == "application/json":
                return json.dumps({"message":"not valid JSON"}), 400, {"Content-Type":"text/plain"}
            if "message" not in body:
                return json.dumps({"message":"no message provided"}), 400, {"Content-Type":"text/plain"}
            else:
                sale = body["message"]
                return json.dumps({"message":"sale activated"}), 200, {"Content-Type":"application/json"}


        # HTML
        if url == "/contact" and data_recieved:
            return open("static/html/postContactConfirmation.html").read(), 201, {"Content-Type": "text/html; charset=utf-8"}
        elif url == "/contact" and not (data_recieved):
            return open("static/html/postContactError.html").read(), 400, {"Content-Type": "text/html; charset=utf-8"}
        else:
            return open("static/html/404.html").read(), 404, {"Content-Type": "text/html; charset=utf-8"}



    if method == "DELETE":
        if body and len(body.strip()) > 0:
            try:
                body = json.loads(body)
            except:
                return json.dumps({"message":"can't parse this, send valid JSON"}), 400, {"Content-Type":"text/plain"}

        if link == "/api/contact":
            if not headers.get("Content-Type") == "application/json":
                return json.dumps({"message":"not valid JSON"}), 400, {"Content-Type":"text/plain"}
            if "id" not in body:
                return json.dumps({"message":"no ID provided"}), 400, {"Content-Type":"text/plain"}

            for i in contacts:
                if int(i["ID"]) == int(body["id"]):
                    contacts.remove(i)
                    return json.dumps({"message":"ok"}), 200, {"Content-Type":"application/json"}
            return json.dumps({"message":'ID not in contacts'}), 404, {"Content-Type":"application/json"}
    
        if link == "/api/sale":
            if not headers.get("Content-Type") == "application/json":
                return json.dumps({"message":"not valid JSON"}), 400, {"Content-Type":"application/json"}
            sale = ""
            return json.dumps({"message":"sale deleted"}), 200, {"Content-Type":"application/json"}

            
            
    if method == "GET":
        # HTML
        if ("/main" == link or "/"  == link):
            return open("static/html/mainpage.html").read(), 200, {"Content-Type": "text/html; charset=utf-8"}
        elif "/admin/contactlog" == link:
            return dynamicContactlog(), 200, {"Content-Type": "text/html"}
        elif "/contact" == link:
            return open("static/html/contactform.html").read(), 200, {"Content-Type": "text/html; charset=utf-8"}
        elif "/testimonies"  == link:
            return open("static/html/testimonies.html").read(), 200, {"Content-Type": "text/html; charset=utf-8"}
        # IMG
        elif "/images/main" == link:
            return open("static/images/Apple-Regent-Street-London-iPhone-15-lineup.jpg", "rb").read(), 200, {"Content-Type": "image/jpeg"}
        # CSS
        elif "/main.css"  == link :
            return open("static/css/main.css").read(), 200, {"Content-Type": "text/css; charset=utf-8"}
        elif "/main.dark.css"  == link :
            return open("static/css/main.dark.css").read(), 200, {"Content-Type": "text/css; charset=utf-8"}
        # JavaScript
        elif "/js/table.js"  == link :
            return open("static/js/table.js").read(), 200, {"Content-Type": "text/javascript; charset=utf-8"}
        elif "/js/contact.js"  == link :
            return open("static/js/contact.js").read(), 200, {"Content-Type": "text/javascript; charset=utf-8"}
        elif "/js/main.js"  == link :
            return open("static/js/main.js").read(), 200, {"Content-Type": "text/javascript; charset=utf-8"}
        elif "/js/sale.js"  == link :
            return open("static/js/sale.js").read(), 200, {"Content-Type": "text/javascript; charset=utf-8"}
        # API
        elif link == "/api/sale":
            if len(sale) == 0:
                return json.dumps({"active":"false"}), 200, {"Content-Type":"application/json"}
            else:
                return json.dumps({"active":"true", "message": sale}), 200, {"Content-Type":"application/json"}

    return open("static/html/404.html").read(), 404, {"Content-Type": "text/html; charset=utf-8"}
    
    # And another freebie -- the 404 page will probably look like this.
    # Notice how we have to be explicit that "text/html" should be the value for
    # header: "Content-Type" now?]
    # I am sorry that you're going to have to do a bunch of boring refactoring.
    # return open("static/html/404.html").read(), 404, {"Content-Type": "text/html; charset=utf-8"}

# You shouldn't need to change content below this. It would be best if you just left it alone.


class RequestHandler(BaseHTTPRequestHandler):
    def c_read_body(self):
        # Read the content-length header sent by the BROWSER
        content_length = int(self.headers.get("Content-Length", 0))
        # read the data being uploaded by the BROWSER
        body = self.rfile.read(content_length)
        # we're making some assumptions here -- but decode to a string.
        body = str(body, encoding="utf-8")
        return body

    def c_send_response(self, message, response_code, headers):
        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")
        
        # Send the first line of response.
        self.protocol_version = "HTTP/1.1"
        self.send_response(response_code)
        
        # Send headers (plus a few we'll handle for you)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", len(message))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        

    def do_POST(self):
        # Step 1: read the last bit of the request
        try:
            body = self.c_read_body()
        except Exception as error:
            # Can't read it -- that's the client's fault 400
            self.c_send_response("Couldn't read body as text", 400, {'Content-Type':"text/plain"})
            raise
                
        try:
            # Step 2: handle it.
            message, response_code, headers = server("POST", self.path, body, self.headers)
            # Step 3: send the response
            self.c_send_response(message, response_code, headers)
        except Exception as error:
            # If your code crashes -- that's our fault 500
            self.c_send_response("The server function crashed.", 500, {'Content-Type':"text/plain"})
            raise
        

    def do_GET(self):
        try:
            # Step 1: handle it.
            message, response_code, headers = server("GET", self.path, None, self.headers)
            # Step 3: send the response
            self.c_send_response(message, response_code, headers)
        except Exception as error:
            # If your code crashes -- that's our fault 500
            self.c_send_response("The server function crashed.", 500, {'Content-Type':"text/plain"})
            raise


    def do_DELETE(self):
        # Step 1: read the last bit of the request
        try:
            body = self.c_read_body()
        except Exception as error:
            # Can't read it -- that's the client's fault 400
            self.c_send_response("Couldn't read body as text", 400, {'Content-Type':"text/plain"})
            raise
        
        try:
            # Step 2: handle it.
            message, response_code, headers = server("DELETE", self.path, body, self.headers)
            # Step 3: send the response
            self.c_send_response(message, response_code, headers)
        except Exception as error:
            # If your code crashes -- that's our fault 500
            self.c_send_response("The server function crashed.", 500, {'Content-Type':"text/plain"})
            raise



def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()
