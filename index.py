from flask import Flask
from db import *

mysql = MySQLUtil()

app = Flask(__name__)
from flask import request
import pymysql

pics_per_page = 50

@app.route("/ajax/<id>/<new_value>", methods=["POST"])
def ajax(id, new_value):
    """
    This is deprecated
    """
    whitelist = ['astronaut', 'aurora', 'black', 'city', 'none', 'stars']
    return_message = ''
    if new_value not in whitelist:
        return_message = 'An error occurred.'
    else:
        return_message = 'Updated!'

    return '<p style="display:inline;">%s</p>' % return_message

@app.route("/ajax/insert/<page>", methods=["POST", "GET"])
def insert(page):
    whitelist = ['astronaut', 'aurora', 'black', 'city', 'none', 'stars']

    stringy = ''
    for r in request.form:
        id = r
        value = request.form[r].strip()
        stringy += '%s&nbsp;&nbsp;%s<br />' % (id, value)
        # if value in whitelist:
        query = 'INSERT INTO corrected_groundtruth VALUES(%s, %s, CURRENT_TIMESTAMP(), %s)'
        params = (id, value, page)
        mysql.insert_value(query, params)

    # Update current position
    # Note that the third person has ID of 0, so I can use id % 3
    # Getting rid of this for a while whilst we use it for the seminar

    # query = 'UPDATE current_position SET position=%s WHERE id=%s'
    # page = int(page)
    # group = page % 3
    # params = ((page + 3), group)
    # mysql.update_value(query, params)
    return stringy
    # return "Inserted"

def check_current_page(page):
    id = int(page) % 3    
    query = 'SELECT position FROM current_position WHERE id = %s'
    params = (id,)
    cursor = mysql.select_as_list(query, params)
    return cursor[0][0]

@app.route("/<page>", methods=['GET'])
def hello(page=1):
    stringy = ''
    classifications = get_classifications()
    if 'favicon.ico' in page:
        return ''
    page = int(page)
    # current_min = check_current_page(page)
    # if current_min > page:
    #     return """
    #     <html><body>
    #     <h1>You have already processed these pictures</h1>
    #     <p>Please move on to <a href="/%d">Page %d</a></p>
    #     </body></html>""" % (current_min, current_min)


    offset = (page -1) * 50
    cursor = get_pictures(offset=offset)
    for c in cursor:
        id = c[0]
        labelclass = c[2]

        options = render_classification_options(classifications, labelclass, id)
        if not labelclass:
            labelclass = 'unclassified'
        form_render = '<label for="%s">Classification</label>%s ' % (id, options)
        stringy += '''
        <div class="container %s">
            <img src="%s" width="320" />
                <div>%s</div>
                <p id="p_%s"></p>
            ID: %s
        </div>''' % (labelclass, get_picture_src(id), form_render, id, id)
    return """
    <html>
        <head>
            <title>Darkskies Images</title>
            <link href="/static/style.css" rel="stylesheet" />
        <body>
	    <form id="imageForm" method="POST">
            <input type="hidden" id="currentPage" value="%d" />
            %s
            <br style="clear:both;" />
            <div style="margin:2em;text-align:right;">
                <a href="/%d" id="next">Next</a>
            </div>
            
	    </form>
        
            <script src="https://code.jquery.com/jquery-2.2.4.min.js"
              integrity="sha256-BbhdlvQf/xTY9gja0Dq3HiwQF8LaCRTXxZKRutelT44="
              crossorigin="anonymous"></script>
            <script src="/static/ajax.js"></script>

        </body>
    </html>
    """ % (page, stringy, page + 15)


def get_pictures(limit=50, offset=0):
    query = 'SELECT * FROM groundtruth_5_1_classification ORDER BY id DESC LIMIT %s OFFSET %s'
    pics = mysql.select_as_list(query, (limit, offset))
    return pics


#def get_picture_src(id):
#    return get_new_picture_id(id)
#    id = '0' + id
#    n = 3
#    path = '/static/images/000/000/'
#    for i in range(0,len(id), n):
#        chunk = id[i:i + n]
#        path += '%s/' % chunk
#    return '%s000000%s.jpg' % (path, id)


def get_new_picture_id(id):
    n = 3
    path = '/static/images/'
    # 21 0s and append ID.  Get the last 21 characters
    image_id = ''
    for i in range(21):
        image_id += '0'
    image_id += id
    print('%s\t' % image_id)
    image_id = image_id[-21:]
    print(image_id)
    for i in range(0, 21, n):
        chunk = image_id[i:i + n]
        path += '%s/' % chunk
    return '%s%s.jpg' % (path, image_id)
	
def get_picture_src(id):
    return get_new_picture_id(id)


def get_classifications():
    query = 'SELECT DISTINCT labelclass FROM groundtruth_5_1_classification ORDER BY labelclass ASC'
    return mysql.select_as_list(query)

def render_classification_options(classifications, selected, id):
    options = ''
    for c in classifications:
        clas = c[0]
        clas_value = clas;
        selected_string = ''
        if clas == selected:
            selected_string = ' selected'
        if not clas:
            clas = 'Please Select'
            clas_value = 'unclassified'
        options += '<option value="%s"%s>%s</option>' % (clas_value, selected_string, clas)

    return '<select id="%s" name="%s">%s</select>' % (id, id, options)
