import chanutils.torrent
from chanutils import get_doc, get_json, select_all, select_one, get_attr
from chanutils import get_text, get_text_content, replace_entity, byte_size
from chanutils import movie_title_year, series_season_episode
from playitem import PlayItem, PlayItemList, MoreEpisodesAction

_BASE_URL = "https://einthusan.tv"
_SEARCH_URL = "http://kat.cr/json.php"

_FEEDLIST = [
  {'title':'Malayalam', 'url': _BASE_URL + '/movie/results/?decade=2010&find=Decade&lang=malayalam'},
  {'title':'Tamil', 'url':_BASE_URL + '/movie/results/?decade=2010&find=Decade&lang=tamil'},
  {'title':'Hindi', 'url':_BASE_URL + '/movie/results/?decade=2010&find=Decade&lang=hindi'},
]

def name():
  return 'Einthusan'

def image():
  return 'icon.png'

def description():
  return "Einthusan Channel (<a target='_blank' href='https://einthusan.tv/movie/browse/?lang=malayalam'>https://einthusan.tv/movie/browse/?lang=malayalam</a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  doc = get_doc(_FEEDLIST[idx]['url'], proxy=True)
  main = select_one(doc, 'section[id="UIMovieSummary"]')
  rtree = select_all(doc, 'li')
  results = PlayItemList()
  for l in rtree:
	el = select_one(l, 'div[class="block1"]')
	if el is None:
		continue
	else:
		url = _BASE_URL + get_attr(select_one(el, 'a'), 'href')
		img = "http://" + get_attr(select_one(el, 'img') , 'src')
		el = select_one(l, 'div[class="block2"]')
		title = get_text_content(select_one(el, 'h3'))
		synopsis = get_text_content(select_one(l, 'p[class="synopsis"]'))
		item = PlayItem(title, img, url, None, synopsis)
		results.add(item)
  return results

def search(q):
  doc = get_doc(_SEARCH_URL, params = { 'q':q })
  return _extract(doc)
