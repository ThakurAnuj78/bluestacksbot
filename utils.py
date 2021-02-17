from googleapiclient.discovery import build
import os

CX = os.getenv('CX')
API_KEY = os.getenv('API_KEY')


def google_search(search, dbms=None):

  '''
  This function searches the text on Google's custom search engine,
  and returns links and title of top 5 results.
  '''
  resource = build("customsearch", 'v1', developerKey=API_KEY).cse()
  quote = resource.list(q=search, cx=CX, num=5).execute()
  
  # Format result
  result = "These are top 5 results from your google search"
  for item in quote.get('items'):
    result += '\n\n' + item.get('title') + '\n' + item.get('link')
  
  # Todo: Store the result in db
  if dbms:
    dbms.insert_to_recent(search)
  
  return(result)

def recent_search(search, dbms=None):

  '''
  This functions searches in the search history for the given keyword.
  '''
  if not dbms:
    return "No MyDatabase object passed"

  return dbms.print_recent_data(search)