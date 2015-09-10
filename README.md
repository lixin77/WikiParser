# WikiParser
Some tools that parse wikipedia dump file

ExtractRedirectItem.py --- parsing the wiki dump file in the specified "path", extracting the information of <redirect> page and 
write the (WikiTile, RedirectTitleList) key-value pair back to the disk. WikiTitle is the title with no ambiguity in the 
wikipedia and RedirectTitleList is the list of page title in wiki which will redirect to the WikiTitle

