import requests
import re
import shutil
import os
import io


def convertRawHtmlToCharset(raw_html, ori_encoding, charset):
    return raw_html.encode(r.encoding, 'ignore').decode(charset, 'ignore')


def extractFilename(path):
    regex_cover_image_filename = r'.+/(.+)'
    matches = re.search(regex_cover_image_filename,
                        cover_image_url, re.M | re.I | re.S)
    cover_image_filename = None
    if matches:
        print 'found cover image'
        cover_image_filename = matches.group(1)


# print r.text

# extract body charset

regex_book_id = r".+\/m(.+?)\.html"
regex_charset = r"<meta charset=(.+)\".+"
regex_cover_image = r"<meta property=\"og:image\" content=\"(.+?)\"/>"


book_id = '80668'
main_url = "https://m.101novel.com/ck101/80668/"

# book_id = None
# matches = re.search(regex_book_id, main_url, re.M|re.I|re.S)
# if matches:
#     book_id = matches.group(1)

# if book_id is None:
#     print "cannot extract book_id from", main_url
#     exit()

# read book index page
r = requests.get(main_url)
raw_html = r.text


matches = re.search(regex_charset, raw_html, re.M | re.I)
charset = 'utf-8'
if matches:
    charset = matches.group(1)

# charset = 'big5'
print 'encoding', r.encoding, charset
raw_html = convertRawHtmlToCharset(raw_html, r.encoding, charset)


# cover_image = None
# matches = re.search(regex_cover_image, raw_html, re.M|re.I|re.S)
# if matches:
#     print 'found cover image'
#     cover_image_url = matches.group(1)

# print "cover_image", cover_image_url
# regex_cover_image_filename = r'.+/(.+)'
# matches = re.search(regex_cover_image_filename, cover_image_url, re.M|re.I|re.S)
# cover_image_filename = None
# if matches:
#     print 'found cover image'
#     cover_image_filename  = matches.group(1)
# r = requests.get(cover_image_url, stream=True)
# with open(cover_image_filename, 'wb') as out_file:
#     shutil.copyfileobj(r.raw, out_file)
# del r


#replacement = """<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />"""
#raw_html = re.sub(regex_charset, replacement, raw_html)
# print convertRawHtmlToCharset(raw_html, r.encoding, charset)

# start getting all chapters page by page
def process_one_page(book_id, page_no, chapter_no, out_dir):
    chapter_index_url = "http://m.101novel.com/%s/%s_%d/" % (
        'ck101', book_id, page_no)
    print chapter_index_url

    r = requests.get(chapter_index_url)
    raw_html = convertRawHtmlToCharset(r.text, r.encoding, charset)

    chapter_list = []
    regex_chapter_url_in_index = r"<li><a href=.+?\/(.+?)\.html.+?>(.+?)\<"
    matches = re.findall(regex_chapter_url_in_index,
                         raw_html, re.M | re.I | re.S)
    if matches:
        print 'found chapter url', len(matches)
        for m in matches:
            chapter = {
                'url': m[0] + ".html",
                'title': m[1],
            }
            chapter_list.append(chapter)
            print m[0] + ".html", m[1]

    # print chapter_list

    for chapter in chapter_list:
        filename = '%s/%d.html' % (out_dir, chapter_no)
        if os.path.isfile(filename):
            chapter_no += 1
            continue

        chapter_url = 'http://m.101novel.com/' + chapter['url']
        print 'download %s - %s' % (chapter_url, chapter['title'])

        r = requests.get(chapter_url)
        raw_html = convertRawHtmlToCharset(r.text, r.encoding, charset)
        regex_chapter_content = r"(<div id=\"nr1\">.+?</div>)"

        chapter_content = None
        matches = re.search(regex_chapter_content,
                            raw_html, re.M | re.I | re.S)
        if matches:
            # print 'found chapter content'
            chapter_content = matches.group(1)
        # print chapter_content

        with io.open('%s/index.csv' % (out_dir), 'a') as f:
            print "write index %s" % (chapter['title'])
            f.write(u'%s,%s\n' % (filename, chapter['title']))

        with io.open(filename, 'w') as f:

            f.write(u'''
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh-hant">
	<head><meta http-equiv="Content-Type" content="text/html;charset=utf-8" /><title>%s</title></head><body>
''' % (chapter['title']))
            # f.write('<meta name="cover" content="%s">' % (cover_image_filename).decode('utf-8'))
            f.write(chapter_content)
            f.write('</body></html>'.decode('utf-8'))

        chapter_no += 1
    return chapter_no

if __name__ == '__main__':
    chapter_no = 1
    page_no = 1
    while True:
        next_chapter_no = process_one_page(
            book_id, page_no, chapter_no, out_dir='book')
        if next_chapter_no == chapter_no:
            break
        chapter_no = next_chapter_no
        page_no += 1

    print 'next chapter ', chapter_no
