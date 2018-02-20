# CS101_SearchEngine_V1
# Hashtable Made by List


def get_page(url):
    if url == 'https://www.udacity.com/cs101x/index.html':
        return '<html> <body> This is a test page for learning to crawl! <p> It is a good idea to <a ' \
               'href="http://www.udacity.com/cs101x/crawling.html"> learn to crawl </a> before you try to <a ' \
               'href="http://www.udacity.com/cs101x/walking.html"> walk </a> or <a ' \
               'href="http://www.udacity.com/cs101x/flying.html"> fly </a>.</p> </body> </html> '
    elif url == 'https://www.udacity.com/cs101x/crawling.html':
        return '<html> <body> I have not learned to crawl yet, but I am quite good at <a ' \
               'href="http://www.udacity.com/cs101x/kicking.html"> kicking </a>.</body> </html> '
    elif url == 'https://www.udacity.com/cs101x/walking.html':
        return '<html> <body> I can not get enough <a href="http://www.udacity.com/cs101x/index.html"> crawling </a' \
               '>!</body> </html> '
    return ''
'''
def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url),read()
    except:
        return ''
'''


def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote


def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def union(p, q):
    for e in q:
        if e not in p:
            p.append(e)


def hashtable_update(htable, key, value):
    bucket = hashtable_get_bucket(htable, key)
    for entry in bucket:
        if entry[0] == key:
            if value not in entry[1]:
                entry[1].append(value)
            return
    bucket.append([key, [value]])


def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        hashtable_update(index, word, url)


def make_hashtable(nbuckets):
    table = []
    for unused in range(0, nbuckets):
        table.append([])
    return table


def hash_string(keyword, buckets):
    result = 0
    for s in keyword:
        result = (result + ord(s)) % buckets
    return result


def hashtable_get_bucket(htable, keyword):
    return htable[hash_string(keyword, len(htable))]


def hashtable_lookup(htable, key):
    bucket = hashtable_get_bucket(htable, key)
    for entry in bucket:
        if entry[0] == key:
            return entry[1]
    return None


def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    htable = make_hashtable(5)    # hashtable with 5 buckets
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(htable, page, content)
            union(tocrawl, get_all_links(content))
            crawled.append(page)
    return crawled, htable


crawled, htable = crawl_web('https://www.udacity.com/cs101x/index.html')
print crawled
print htable[0]
