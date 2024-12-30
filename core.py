import yaml
from datetime import datetime
import json
import bs4
import requests
from pathlib import Path
from utilities import read_file, write_file, safe_filename

DATA_FOLDER = Path("/home/patrick/research")
TOPICS_FOLDER = DATA_FOLDER / Path('topics')
TOPIC_FILE_PATH = DATA_FOLDER / Path('topic')

def topic():
    """Returns the current topic."""
    return read_file(TOPIC_FILE_PATH).strip()

    
def topic_folder():
    """Returns the path to the topic folder."""
    return TOPICS_FOLDER / Path(topic())


    
def list_topics():
    """List available topics."""
    return [f.stem for f in TOPICS_FOLDER.iterdir() if f.is_dir()]


def set_topic(topic):
    """Set the topic by writing to the topic file."""
    topic = safe_filename(topic)
    write_file(TOPIC_FILE_PATH, topic)
    return topic

def make_request(url):
    r = requests.get(url)

    if not r.ok:
        print('not ok')
        raise Exception
    else:
        r = requests.get(url)

    return r


def parse_page(request):

    soup = bs4.BeautifulSoup(request.text, features='lxml')

    html = request.text
    title = soup.title.text
    links = soup.find_all('a', href=True)

    links = [str(link.get('href')) for link in links]
    external, internal = [], []
    for link in links:
        if link[:4] == 'http':
            external.append(link)
        else:
            internal.append(link)
    
    url = request.url
    captured = str(datetime.now())

    output = {
        'title': title,
        'html': html,
        'url': url,
        'internal': internal,
        'external': external,
        'captured': captured,
        }

    return output
        

def get_page(url):
    return parse_page(make_request(url))


def save_page(data):
    """Given data representing a page, save the data."""
    html = data.pop('html', None)
    breakpoint()
    url = data['url'].replace('https://', '').replace('http://', '')
    safe_url = safe_filename(url)
    page_path = topic_folder() / Path(safe_url)
    if (page_path / Path('metadata.yaml')).exists():
        archive_page(safe_url)

    if not topic_folder().exists():
        create_topic_folder()
    if not page_path.exists():
        page_path.mkdir()

    write_file(page_path / Path('index.html'), html)
    write_file(page_path / Path('metadata.yaml'),
               yaml.dump(data))

    overlog_data = {
        data['captured']: {
        'topic': topic(),
        'url': url,
            }
        }

    write_file(DATA_FOLDER / Path('overlog.yaml'), yaml.dump(overlog_data), 'a')
    return page_path

    
def capture_from_url(url):
    """Given a URL, capture URL data and save it."""

    request = make_request(url)
    data = parse_page(request)
    saved = save_page(data)

    return saved


def create_topic_folder():
    """Creates a folder for the current topic."""
    return topic_folder().mkdir(exist_ok=True)


def archive_page(url, topic=topic()):
    """Moves the page snapshot into the archive folder."""
    page_path = TOPICS_FOLDER / Path(topic) / Path(url)
    (page_path / Path('archived')).mkdir(exist_ok=True)
    data = yaml.load(read_file(page_path / Path('metadata.yaml')), Loader=yaml.FullLoader)

    captured = data.get('captured', 'no_capture_date')
    capture_archive_path = page_path / Path('archived') / Path(captured)
    capture_archive_path.mkdir()
    for file_or_folder in page_path.iterdir():
        if not file_or_folder == page_path / Path('archived'):
            file_or_folder.rename(capture_archive_path / file_or_folder.name)
