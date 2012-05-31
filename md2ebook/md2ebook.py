#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Converts a simple markdown document into the main ebook formats: 
    epub, mobi\prc, html and pdf.

Assumptions:

* The title of the book is the first h1 element.
* Each Chapter starts with an h2 element.
* The authors name is the first h3
* If only one Chapter is present no Table of Contents is generated.

Therefore valid markdown must contain at least one h1, h2 and h3.
"""

from markdown2 import markdown
from xhtml2pdf import pisa
from StringIO import StringIO
from epubbuilder.epubbuilder import EpubBook
from bs4 import BeautifulSoup

import os
import re
import tempfile
import unidecode
import subprocess

class LazyProperty(object):
    """
    automagically makes a function lazy loading and behave like an attribute
    """
    def __init__(self, func):
        self._func = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj, klass=None):
        if obj is None: 
            raise ValueError("""LazyProperty decorator should only be used 
on class methods with no arguments""")
        result = obj.__dict__[self.__name__] = self._func(obj)
        return result

class HTMLWrapper(object):
    """
    Wraps provided html in boilerplate
    """
    @LazyProperty
    def boilerplate(self):
        """
        retrieves the correct boilerplate
        """
        path = os.path.join(
            os.path.split(__file__)[0], "templates/html-boilerplate.html")
        with open(path) as _file:
            return _file.read()
    
    def wrap_html(self, title, body):
        """
        wraps the provided html fragment in the correct boilerplate
        """
        return self.boilerplate.format(title = title, body = body)
        
HTMLWRAP = HTMLWrapper()

def slugify(_str):
    """
    turns any string into a valid url/filename slug
    """
    _str = unidecode.unidecode(_str).lower()
    return re.sub(r'\W+', '-', _str)

class Chapter(object):
    """
    Represents a chapter
    """
    def __init__(self, title, html):
        self.title = title
        self.slug = slugify(title)
        self.html = HTMLWRAP.wrap_html(title, html)

class HtmlParser(object):
    """
    Parses the provided HTML to give easy access to the title, author and 
    chapters
    """
    def __init__(self, html):
        self.soup = BeautifulSoup(html)
    
    def get_title(self):
        """
        Retrieves the title from the provided html.
        That is to say the contents of the first h1
        """
        title = self.soup.find('h1')
        if not title:
            raise ValueError('Could not find title in provided html')
        return title.string
    
    def get_author(self):
        """
        Retrieves the author from the provided html.
        That is to say the contents of the first h3
        """
        author = self.soup.find('h3')
        if not author:
            raise ValueError('Could not find author in provided html')
        return author.string
    
    def get_chapters(self):
        """
        Retrieves the author from the provided html.
        That is to say the contents of the first h3
        """
        chapters = []
        chapter_titles = self.soup.find_all('h2')
        for title in chapter_titles:
            html = title.prettify()
            next_sib = title.next_sibling
            while next_sib and \
                    (not hasattr(next_sib, 'name') or next_sib.name != 'h2'):
                try:
                    html = html + next_sib.prettify()
                except AttributeError:
                    html = html + next_sib.string
                next_sib = next_sib.next_sibling
            chapters.append(Chapter(title.string, html))
        
        return chapters

class Md2Ebook(object):
    """
    Converts from markdown to a variety of ebook formats: 
        html, pdf, epub and mobi
    Usage:
        >>> book = Md2Ebook(md_content)
        >>> open(path, 'w').write(book.html)
        >>> open(path, 'w').write(book.pdf)
        ...
    """
    def __init__(self, md_content, cover=None):
        self.markdown = md_content
        self.cover = cover
        self.parser = HtmlParser(self.html)
    
    @LazyProperty
    def html(self):
        """
        Converts markdown to html and returns the char stream
        """
        html = markdown(self.markdown)
        parser = HtmlParser(html)
        return HTMLWRAP.wrap_html(parser.get_title(), html)
    
    @LazyProperty
    def pdf(self):
        """
        Converts html to pdf and returns the char stream
        """
        result = StringIO()
        pisa.pisaDocument(StringIO(self.html.encode("UTF-8")), result)
        return result.getvalue()
    
    @LazyProperty
    def epub(self):
        """
        Converts html to epub and returns the char stream
        """
        book = EpubBook()
        book.set_title(self.parser.get_title())
        book.add_creator(self.parser.get_author())
        
        chapters = self.parser.get_chapters()
        book.add_title_page()
        
        if len(chapters) > 1:
            book.add_toc_page()
        
        if self.cover:
            book.add_cover(self.cover)
        
        # add chapters
        for chapter in chapters:
            item = book.add_html('{0}.html'.format(chapter.slug), chapter.html)
            book.add_spine_item(item)
            
            if len(chapters) > 1:
                book.add_toc_map_node(item.dest_path, chapter.title)
        
        stream = StringIO()
        book.create_book(stream)
        return stream.getvalue()
    
    @LazyProperty
    def mobi(self):
        """
        Converts epub to mobi and returns the char stream
        """
        # save epub to temp file
        (_, epub_name) = tempfile.mkstemp(suffix='.epub')
        (_, mobi_name) = tempfile.mkstemp(suffix='.mobi')
        (_, mobi_file) = os.path.split(mobi_name)
        
        try:
            with open(epub_name, 'w') as _file:
                _file.write(self.epub)
            
            kindlegen_path = os.path.join(os.path.split(__file__)[0], 
                'kindlegen_linux_2.6_i386_v2_4/kindlegen')
            subprocess.call([kindlegen_path, epub_name, '-c1', '-o', mobi_file])
            with open(mobi_name) as _file:
                return _file.read()
        finally:
            os.remove(epub_name)
            os.remove(mobi_name)


from argparse import ArgumentParser
from os.path import splitext, split, join
def main():
    """
    Treat the command line options
    """
    def get_cover(covers, idx):
        """
        retrieve the cover at the same index as the book to convert, 
        if no cover at said index return None
        """
        if len(covers) == 0 or len(covers) <= idx:
            return None
        else:
            return covers[idx]
            
    parser = ArgumentParser(
        description='Convert provided markdown to html, pdf, epub and mobi')
    parser.add_argument('files', nargs='+', 
        help='list the markdown files to be converted')
    parser.add_argument('--covers', '-c', nargs='*', default=[], 
        help='provide the paths for the covers to be used')
    parser.add_argument('--output', '-o',  
        help='output directory, if different from input files directory')
    parser.add_argument('-html', action='store_false', 
        help='suppress convertion to html')
    parser.add_argument('-pdf', action='store_false', 
        help='suppress convertion to pdf')
    parser.add_argument('-epub', action='store_false', 
        help='suppress convertion to epub')
    parser.add_argument('-mobi', action='store_false', 
        help='suppress convertion to mobi')
    parser.add_argument('-prc', action='store_false', 
        help='suppress convertion to prc')
    
    args = parser.parse_args()
    
    for idx, path in enumerate(args.files):
        with open(path) as _file:
            conv = Md2Ebook(_file.read(), get_cover(args.covers, idx))
            root, _ = splitext(path)
            if args.output:
                root = join(args.output, split(splitext(path)[0])[1])
            
            # save html
            if args.html:
                with open(root+'.html', 'w') as html:
                    html.write(conv.html)
            # save pdf
            if args.pdf:
                with open(root+'.pdf', 'w') as pdf:
                    pdf.write(conv.pdf)
            # save epub
            if args.epub:
                with open(root+'.epub', 'w') as epub:
                    epub.write(conv.epub)
            # save mobi
            if args.mobi:
                with open(root+'.mobi', 'w') as mobi:
                    mobi.write(conv.mobi)
            # save prc
            if args.prc:
                with open(root+'.prc', 'w') as prc:
                    prc.write(conv.mobi)


if __name__ == "__main__":
    main()

