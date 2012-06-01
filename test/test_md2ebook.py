import os
import re
import codecs
import filecmp
import unittest
import md2ebook.md2ebook as md2ebook

def get_path(path):
    return os.path.join(os.path.split(__file__)[0], path)

def get_file_content(path):
    with open(get_path(path)) as _file:
        ret = _file.read()
    return ret
    
def compare_html_files(testcase, test_file):
    try:
        md_path = get_path(os.path.join('test-files/', test_file+'.md'))
        with open(md_path) as _file:
            conv = md2ebook.Md2Ebook(_file.read())
        
        temp_path = get_path(
            os.path.join('test-files/correct_output/', test_file+'.html.temp'))
        with codecs.open(temp_path, 'w', 'utf-8') as _file:
            _file.write(conv.html)
        
        correct_path = get_path(
            os.path.join('test-files/correct_output/', test_file+'.html'))
        testcase.assertTrue(filecmp.cmp(temp_path, correct_path))
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass

class TestHTML(unittest.TestCase):
    
    def test_html_multi_chapter(self):
        compare_html_files(self, 'multiple-chapters')
                
    def test_html_single_chapter(self):
        compare_html_files(self, 'one-chapter')
    
    def test_html_unicode(self):
        compare_html_files(self, 'treasure-island')


class TestEpub(unittest.TestCase):
    
    def test_repeat_chapter_names(self):
        with open(get_path('test-files/repeat-chapters.md')) as _file:
            conv = md2ebook.Md2Ebook(_file.read())
            conv.epub # just to actualize the property
            # check there are the right number of spine items
            self.assertEqual(len(conv._epub.spine), 17)
            # and there are the correct number of html_items
            self.assertEqual(len(conv._epub.html_items.keys()), 17)
            # check the html_items keys are all either
            # chapter-name-that-will-be-repeated-till-the-end-of-time
            # or title-page.html or toc.html
            import pdb; pdb.set_trace()
            chapter = 'chapter-name-that-will-be-repeated-till-the-end-of-time'
            for slug in conv._epub.html_items.keys():
                if slug in ['title-page.html', 'toc.html']:
                    continue
                else:
                    self.assertTrue(re.match(chapter+'-*\.html', slug))


def main():
    return unittest.main()

if __name__ == '__main__':
    main()
