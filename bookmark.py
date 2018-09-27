from langdetect import detect
import codecs

def output_file(html_file, folder_name, bookmark_name=None,
                         domain=None, lang=None):
    '''(file name string, str, str, str, str) -> (file) 
    This function scraps all the desired links that matches the folder
    name and bookmark name and the domain name.
    bookmark_name, domain and lang defaults to None and are optional
    '''
    # bookmark name, domain name and lang name search function wont be
    # implemented soon xd
    file = codecs.open('output.txt', 'w', 'utf-8-sig')
    try:
        all_data = scrape_bookmark_html(html_file)
        keys = all_data.keys()
        for key in keys:
            if (key == folder_name):
                bookmarks = all_data[key]
                for list_of_data in bookmarks:
                    file.write(list_of_data[0]+ '\n')

    finally:
        file.close()

def scrape_bookmark_html(html_file):
    '''(str) -> dict of (str: list of ((list of str)))
    This function scraps all the links and their data: 
    '''

    # open the file and read every single line
    html = codecs.open(html_file, 'rU', 'utf-8')
    all_strings = html.readlines()

    # create the list that contains all the dictionaries
    # folder_name:list of bookmarks
    all_bookmarks = {}
    folder_name = ''

    # we dont need the first 8 lines, index 0-7 but w/e
    for item in all_strings:
        # first thing is to remove all the <DT> beginning tags
        item = item.strip()
        item = item.strip('<DT>')
        # remove < and >
        item = item.strip('<')
        item = item.strip('>')

        # check if it's a folder name
        if (check_folder(item) != ''):
            folder_name = check_folder(item)
            all_bookmarks[folder_name] = []
        # check if it's a bookmark instead
        elif (len(check_bookmark(item)) != 0 and folder_name != ''):
            bookmark = check_bookmark(item)
            # since there is no way folder_name is ever empty if
            # there is a bookmark
            # then we add the bookmark to the list that for the current
            # folder
            # curr_list = all_bookmarks[folder_name] 
            # curr_list.append(bookmark)
            all_bookmarks[folder_name].append(bookmark)

    return all_bookmarks

def check_folder(row):
    '''(str) -> (str)
    Checks if a given row is a bookmark folder, if it is it will return
    the bookmark folder name, otherwise return ''
    '''

    folder_name = ''
    # check if it contains the <H3> tag that is unique for bookmark folders
    if ('/H3' not in row):
        return ''
    else:
        # start scrapping for the folder name
        # strip away </H3>
        # split the string at >
        folder = row.strip('</H3>')
        folder_list = folder.split('>')
        folder_name = folder_list[1]
        return folder_name

def check_bookmark(row):
    '''(str) -> list of [str, str, str, str]
    this will return the url, domain, title and language in that order.
    Returns empty list if it's not a row
    '''

    # initialize all the strings
    url = ''
    domain = ''
    title = ''
    lang = ''
    data = []

    # check it if containst the </A> tag that is unique for bookmarks
    if ('/A' not in row):
        return data
    else:
        # start by gettin the title
        all_data = row.strip('</A>')
        splitted_data = all_data.split('>')
        title = splitted_data[1]

        # now obtain the language using langdetect
        # if it's not one of our preferred language, change it to English
        try:
            lang = detect(title)
        except:
            lang = 'en'
        if (lang != 'en' or lang != 'ja' or lang != 'ko'
            or lang != 'zh-cn' or lang != 'zh-tw' or lang != 'fr'):
            lang = 'en'

        # obtain the url
        splitted_data = splitted_data[0].split('"')
        url = splitted_data[1]

        # obtain the domain
        if ('www.' not in url):
            splitted_data = url.split('/')
            splitted_data = splitted_data[2].split('.')
            domain = splitted_data[0].lower()
        else:
            splitted_data = url.split('.')
            domain = splitted_data[1].lower()

        data = [url, domain, title, lang]
        return data

output_file('bookmarks_9_21_18.html', 'Music')