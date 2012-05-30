from distutils.core import setup
setup(name='md2ebook',
      version='1.0',
      description='Convert markdown to the popular ebook formats in a simple way',
      author='Jonathan Butcher',
      author_email='footley@gmail.com',
      url='https://github.com/footley/md2ebook',
      py_modules=['md2ebook'],
      data_files=[('templates', ['html-boilerplate.html',
                                 ]),
                  ('test-files', ['multiple-chapters.md',
                                  'one-chapter.md',
                                  'treasure-island.md',
                                  'revenge.500x800.jpg'
                                  ]),
                  ('kindlegen_linux_2.6_i386_v2_4', ['EULA.txt',
                                                     'kindlegen',
                                                     'KindleGen Legal Notices 2009-11-10 Linux.txt',
                                                     ]),
                 ],
      )

