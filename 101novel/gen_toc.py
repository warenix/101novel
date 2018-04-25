import csv
import os

with open('book/toc.html', 'w') as tocfile:
    tocfile.write('''
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    </head>
    <body>
    <h1>Table of Contents</h1>
    <p style="text-indent:0pt">''')

    with open('book/index.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            # line = '<a href="file://%s/%s">%s</a><br/>' % (
            #     os.path.dirname(os.path.abspath(__file__)),
            #     row[0],
            #     row[1]
            # )

            # line = '<a href="file://%s/%s">%s</a><br/>' % (                
            line = '<a href="%s">%s</a><br/>' % (
                row[0].replace('book/', ''),
                row[1]
            )
            tocfile.write(line)
    tocfile.write('''
    </body>
    </html>
    ''')

# # gen toc index
# toc_html = '''
# <html>
# <head>
# <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
# </head>
# <body>
#     <h1>Table of Contents</h1>
#      <p style="text-indent:0pt">
#              <a href="file:///home/warenix/code/repo/github/myxs/src/1.html">First File</a><br/>
#              <a href="file:///home/warenix/code/repo/github/myxs/src/2.html">Second File</a><br/>
#     </p>
# </body>
# </html>
# '''
