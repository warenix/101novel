Directory structure

- book: Chapters xhtmls. Each xhtml must be valid
- cover.jpg: Book cover
- book/toc.html: Defines all chapters
- build.sh: build mobi output
- gen_toc.py: generate book/toc.html from all book chapters in book

# Usage

```sh
sh build.sh
```
This command will start download all chapters of a novel, generate TOC file, then build a mobi book.

# Requirements

## Binary

- ebook-convert
- ebook-meta

## Python library

- requests
