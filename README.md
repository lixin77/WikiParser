# WikiParser
Some tools that parse wikipedia dump file

ExtractRedirectItem.py --- parsing the wiki dump file in the specified "path", extracting the information of <redirect> page and 
write the (WikiTile, RedirectTitleList) key-value pair back to the disk. WikiTitle is the title with no ambiguity in the 
wikipedia and RedirectTitleList is the list of page title in wiki which will redirect to the WikiTitle

ExtractDisambiguationItem.py --- parsing the wiki dump file in the specified 'path', extract the surface form title in wikipedia 
and some disambiguation item related to it, for example, the title "中山大学" is ambiguous, it may refer to "浙江大学(国立第三中山大学)",
"国立中山大学（高雄）" or "莫斯科中山大学", so we can extract "中山大学" and its disambiguation list

chinese wikipedia dump file is at: https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2, which contains 
all of the page information in zh-wiki

