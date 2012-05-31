import re
from distutils.core import setup

def parse_requirements(file_name):
    """
    Simple requirements parsing, only works for reqs of form:
    genshi==0.6
    genshi
    git://github.com/footley/epubbuilder.git#egg=epubbuilder
    etc.
    """
    requirements = []
    with open(file_name) as _file:
        for line in _file.readlines():
            line = line.strip()
            if re.match(r'(\s*#)|(\s*$)', line): # skip comments/empty lines
                continue
            elif re.match(r'.*#egg=', line):
                requirements.append(re.sub(r'.*#egg=', '', line))
            else:
                requirements.append(line)
    
    return requirements
    
def parse_dependency_links(file_name):
    """
    retrives the dependancies in the form of 
    git://github.com/footley/epubbuilder.git#egg=epubbuilder
    """
    dependency_links = []
    with open(file_name) as _file:
        for line in _file.readlines():
            line = line.strip()
            if re.match(r'.*#egg=', line):
                dependency_links.append(line)
    
    return dependency_links

with open('README.md') as _file:
    long_desc = _file.read()

setup(name='md2ebook',
      version='1.0',
      description='Convert markdown to the popular ebook formats in a simple way',
      long_description = long_desc,
      author='Jonathan Butcher',
      author_email='footley@gmail.com',
      url='https://github.com/footley/md2ebook',
      install_requires=parse_requirements('requirements.txt'),
      dependency_links=parse_dependency_links('requirements.txt'),
      scripts=['scripts/md2ebook'],
      packages=['md2ebook'],
      package_data={'md2ebook': [
                         'templates/html-boilerplate.html', 
                         'kindlegen_linux_2.6_i386_v2_4/EULA.txt',
                         'kindlegen_linux_2.6_i386_v2_4/kindlegen',
                         'kindlegen_linux_2.6_i386_v2_4/KindleGen Legal Notices 2009-11-10 Linux.txt',
                        ],
                   },
      )

