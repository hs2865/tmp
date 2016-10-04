import urllib2
import lxml.html

url = 'https://www.sec.gov/Archives/edgar/data/1288776/000128877615000008/goog2014123110-k.htm'
request = urllib2.urlopen(url)
html = unicode(request.read(), 'utf-8')

dom = lxml.html.fromstring(html)
main_doc = dom[0][0][0][0][0]

## Getting dom information at each page (separated by hr tag(line break))
pages = {}
page = []
num_page = 0 # This is not actual page number, need to be converted
for i in range(len(main_doc)):
    # create html again to parse html again
    if main_doc[i].tag != 'hr':
        page.append(main_doc[i])
    else:
        pages[num_page] = page
        num_page = num_page + 1
        page = []


## Getting table of contents information, it should be located at page 2
page2 = pages[1]
for element in page2:
    if element.tag == 'div' and element[0].tag == 'div':
        if element[0][0].tag == 'table':
             table_contents = element[0][0]


# TODO(hs2865) Need to remove html entity like 'Item\xa01.'
contents = [] # x-y matrix, ["title", "name", "page"]
              # something like ["Item1.", "Business", "1"]
count = 0
for tr in table_contents:
    # At the third td tag, it should contain actual page number
    # if it does not contain it, the row does not contain actual page num
    if len(tr) == 2:
        if len(tr[1]) == 1 and tr[1][0].tag == 'div':
            if len(tr[1][0]) == 1 and tr[1][0][0].tag == 'a':
                contents.append([])
                contents[count].append("Top")
                contents[count].append(tr[0][0][0].text_content())
                contents[count].append(tr[1][0][0].text_content())
                count = count + 1

    if len(tr) == 3:
        if len(tr[2]) == 1 and tr[2][0].tag == 'div':
            if len(tr[2][0]) == 1 and tr[2][0][0].tag == 'a':
                contents.append([])
                contents[count].append(tr[0][0][0].text_content())
                contents[count].append(tr[1][0][0].text_content())
                contents[count].append(tr[2][0][0].text_content())
                count = count + 1

## Accessing actual text
offset = 2 # Where the content will begin

# For example, show text of "ITEM 1. BUSINESS"
item1_begin = int(contents[1][2]) + offset - 1 # Page number of "ITEM 1. BUSINESS"
item1_end = int(contents[2][2]) - 1 + offset - 1
item1_str = ''
for i in range(item1_begin, item1_end + 1):
    tmp_page = pages[i]
    for element in tmp_page:
        print(element.text_content())
