# -*- coding: utf-8 -*-
__author__ = 'v-tedl'

import os
from xml.etree.ElementTree import iterparse
import threading
import re

class MyThread(threading.Thread):
    pnumber = int
    data = []
    def __init__(self, pnumber, data):
        threading.Thread.__init__(self)
        self.pnumber = pnumber
        self.data = data

    def run(self):
        """
        save the data sepatately
        """
        path = '%s/redirect%s.txt' % (os.getcwd(), self.pnumber)
        print 'process file %s...' % path
        fp = open(path, 'w+')
        fp.writelines(self.data)
        fp.close()

def ExtractRedirectItem(path, filename):
    """
    extract the redirect tile from the wiki dump file which is in the form of xml
    :param path: directory of wiki dump file
    :param filename: name of wiki dump file
    :return:
    """
    doc = iterparse(path + filename, ('start', 'end'))
    searchPattern = re.compile(r'消歧義|消歧义', re.DOTALL)
    count = 1
    pnumber = 0
    lines = []
    lines.append('KBItem\tQueryItem\n')
    # traverse the whole xml file
    for (event, ele) in doc:
        if ele.tag != 'page':
            continue
        if event == "end":
            continue
        # event == begin and ele.tag == 'page'
        all_subs = list(ele)
        for sub in all_subs:
            if not (sub.tag == 'title' or sub.tag == 'redirect'):
                continue
            if sub.tag == "title" and sub.text:
                redirect_item = sub.text
            if sub.tag == "redirect" and sub.get('title'):
                KBItem = sub.get('title')
                # if the title contains "消歧义" or "消歧義", then page is the disambiguation page, we can ignore it
                if searchPattern.search(KBItem.encode('utf8')) or searchPattern.search(redirect_item.encode('utf8')):
                    break
                count += 1
                lines.append('%s\t%s\n' % (KBItem.encode('utf8'), redirect_item.encode('utf8')))
                if count % 1000 == 0:
                    print "process %s pages" % count
                if count % 100000 == 0:
                    MyThread(pnumber, lines).start()
                    pnumber += 1
                    # garbage collection
                    del lines
                    lines = []
                    lines.append('KBItem\tQueryItem\n')
        # release the current element, otherwise, out of memory will occur
        ele.clear()
    # write the remainder of the wiki-redirect-items
    if lines:
        fp = open('%s/redirect%s.txt' % (os.getcwd(), pnumber), 'w+')
        fp.writelines(lines)
        fp.close()
