#!/usr/bin/env python

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

boilerplate = None
def correct_html(title, body):
    def get_boilerplate():
        global boilerplate
        if boilerplate:
            return boilerplate
        with open('templates/html-boilerplate.html') as _file:
            boilerplate = _file.read()
        return boilerplate
    return get_boilerplate().format(title = title, body = body)

def slugify(str):
    str = unidecode.unidecode(str).lower()
    return re.sub(r'\W+','-',str)

class Chapter(object):
    def __init__(self, title, html):
        self.title = title
        self.slug = slugify(title)
        self.html = correct_html(title, html)

class HtmlParser(object):
    def __init__(self, html):
        self.soup = BeautifulSoup(html)
    
    def get_title(self):
        title = self.soup.find('h1')
        if not title:
            raise ValueError('Could not find title in provided html')
        return title.string
    
    def get_author(self):
        author = self.soup.find('h3')
        if not author:
            raise ValueError('Could not find author in provided html')
        return author.string
    
    def get_chapters(self):
        chapters = []
        chapter_titles = self.soup.find_all('h2')
        for title in chapter_titles:
            html = title.prettify()
            next = title.next_sibling
            while next and (not hasattr(next, 'name') or next.name != 'h2'):
                try:
                    html = html + next.prettify()
                except AttributeError:
                    html = html + next.string
                next = next.next_sibling
            chapters.append(Chapter(title.string, html))
        
        return chapters

class Md2Ebook(object):
    def __init__(self, md, cover=None):
        self.md = md
        self.cover = cover
        self.parser = HtmlParser(self.html)
    
    def _generate_html(self):
        html = markdown(self.md)
        parser = HtmlParser(html)
        return correct_html(parser.get_title(), html)
    
    def _generate_pdf(self):
        result = StringIO()
        pisa.pisaDocument(StringIO(self.html.encode("UTF-8")), result)
        return result.getvalue()
    
    def _generate_epub(self):
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
    
    def _generate_mobi(self):
        # save epub to temp file
        (_, epub_name) = tempfile.mkstemp(suffix='.epub')
        (_, mobi_name) = tempfile.mkstemp(suffix='.mobi')
        (_, mobi_file) = os.path.split(mobi_name)
        print epub_name
        print mobi_name
        try:
            with open(epub_name, 'w') as _file:
                _file.write(self.epub)
            
            subprocess.call(['kindlegen_linux_2.6_i386_v2_4/kindlegen', epub_name, '-c1', '-o', mobi_file])
            with open(mobi_name) as _file:
                return _file.read()
        finally:
            os.remove(epub_name)
            os.remove(mobi_name)
    
    def __getattr__(self, name):
        if name == "html":
            self.html = self._generate_html()
            return self.html
        elif name == "pdf":
            self.pdf = self._generate_pdf()
            return self.pdf
        elif name == "epub":
            self.epub = self._generate_epub()
            return self.epub
        elif name == "mobi":
            self.mobi = self._generate_mobi()
            return self.mobi
        else:
            raise AttributeError


from argparse import ArgumentParser
from os.path import splitext, split, join
def main():
    def get_cover(covers, idx):
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
        with open(path) as f:
            md = f.read()
            conv = Md2Ebook(md, get_cover(args.covers, idx))
            root, ext = splitext(path)
            if args.output:
                root = join(args.output, split(splitext(path)[0])[1])
            
            print root
            
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

