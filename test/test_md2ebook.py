import os
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

class TestHTML(unittest.TestCase):
    
    def test_html_multi_chapter(self):
        conv = md2ebook.Md2Ebook(get_file_content('test-files/multiple-chapters.md'))
        self.assertEqual(conv.html, 
            get_file_content(
                'test-files/correct_output/multiple-chapters.html'))
                
    def test_html_single_chapter(self):
        conv = md2ebook.Md2Ebook(get_file_content('test-files/one-chapter.md'))
        self.assertEqual(conv.html, 
            get_file_content(
                'test-files/correct_output/one-chapter.html'))
    
    def test_html_unicode(self):
        with open(get_path('test-files/treasure-island.md')) as _file:
            conv = md2ebook.Md2Ebook(_file.read())
        
        temp_path = get_path('test-files/correct_output/treasure-island.html.temp')
        with codecs.open(temp_path, 'w', 'utf-8') as _file:
            _file.write(conv.html)
        
        correct_path = get_path('test-files/correct_output/treasure-island.html')
        self.assertTrue(filecmp.cmp(temp_path, correct_path))
        
        os.remove(temp_path)
        
def main():
    return unittest.main()

if __name__ == '__main__':
    main()
