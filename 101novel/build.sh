title='雙世寵妃原著︰爺我等你休妻'
author='梵缺'
cover='cover.jpg'

# remove non-content text
sed -i -e 's/&nbsp;&nbsp;&nbsp;&nbsp;戀上你看書網 630book .*//g' book/*
sed -i -e 's/&nbsp;&nbsp;&nbsp;&nbsp;看清爽的就到//g' book/*

python gen_toc.py
ebook-convert  book/toc.html  $title.mobi --breadth-first
ebook-meta --title "$title"\
       --authors "$author"\
       --language "zh-hant"\
       --cover "$cover"\
       $title.mobi

