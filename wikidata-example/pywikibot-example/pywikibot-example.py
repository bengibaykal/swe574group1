import pywikibot

site = pywikibot.Site("en", "wikipedia")
page = pywikibot.Page(site, "Douglas Adams")
item = pywikibot.ItemPage.fromPage(page)

print(item)
# [[wikidata:Q42]]
