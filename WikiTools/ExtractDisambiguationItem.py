# -*- coding: utf-8 -*-
__author__ = 'v-tedl'

import re
from xml.etree.ElementTree import iterparse

def ExtractDisambiguationItems(path):
    """
    extract disambiguation items from the wikipedia dump file
    :param path: dump file of wikipedia chinese
    :return: dictionary associate surface name with kb items
    """
    itemPattern = re.compile(r"\*\s{0,1}'{0,3}\[{2}(.+?)\]{2}'{0,3}")
    #searchPattern = re.compile(r'消歧義|消歧义', re.DOTALL)
    existPattern = re.compile(r'(disambig*|begriffsklärung)', re.IGNORECASE)
    #existPattern = re.compile(r'(disambiguation|disambigua|begriffsklärung|)')
    # mapping between surface name and kb item with no ambiguity
    SFName2WikiItem = dict()
    doc = iterparse(path, ('start', 'end'))
    count = 0
    for (event, ele) in doc:
        if event != 'start':
            ele.clear()
            continue
        if ele.tag != 'page':
            ele.clear()
            continue
        # at the beginning of the <page>
        # find the <title>
        TT = ele.find('title')
        if TT is None:
            # <title> is empty
            ele.clear()
            continue
        # default value is false, which means the page is not the disambiguation page
        isDisambiguation = False
        # surface name of the query, which may result in ambiguity
        SurfaceName = ''
        disambTitle = TT.text
        if disambTitle is None:
            # title is empty, ignore it
            ele.clear()
            continue
        revision = ele.find('revision')
        if revision is None or not [element for element in list(revision) if element.tag == 'text']:
            # <revision> is empty or no sub-element in <revision> named text
            ele.clear()
            continue
        txtTag = revision.find('text')
        if txtTag.text is None:
            # text is empty
            ele.clear()
            continue
        disambiguationText = txtTag.text.replace('\n', '')
        if not existPattern.search(disambiguationText):
            # this is not a disambiguation page, ignore it
            ele.clear()
            continue
        #print disambiguationText.encode('utf8')
        begPos = disambTitle.find('(') if disambTitle.find('(') != -1 else len(disambTitle)
        SurfaceName = disambTitle[0:begPos].strip(' ')
        count += 1
        if count % 100 == 0:
            print 'processed %s disambiguation pages' % count
        if SurfaceName not in SFName2WikiItem.iterkeys():
            SFName2WikiItem[SurfaceName] = []
        items = itemPattern.findall(disambiguationText.encode('utf8'))
        for item in items:
            SFName2WikiItem[SurfaceName].append(item)
        ele.clear()
    return SFName2WikiItem
