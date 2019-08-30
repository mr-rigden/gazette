import argparse
from datetime import datetime
import logging
import os
from shutil import copyfile
import re


import dateutil.parser
import jinja2
import markdown
from slugify import slugify
import yaml

####################
# Global Constants
####################

VERSION = "0.1.1"
CONTENT_SEPARATOR = '=========='
GENERATOR = 'redmercury '+ VERSION +' (https://github.com/jrigden/redmercury)'


####################
# Setup
####################

site_path = ''
home_path = os.path.dirname(os.path.realpath(__file__))
templats_path = os.path.join(home_path, "templates")
file_loader = jinja2.FileSystemLoader(templats_path)
env = jinja2.Environment(loader=file_loader)

parser = argparse.ArgumentParser(description='A static site generator for blogs and podcasts. v' + VERSION)
parser.add_argument("-v", "--verbose",  help="increase verbosity", action="store_true")
parser.add_argument("-i", "--initialize", help="initialize site", action="store_true")
parser.add_argument('path', help="path to site")
args = parser.parse_args()

##############################
# Path Functions
##############################
def get_config_path():
    return os.path.join(site_path, "config.yaml")

def get_content_path():
    return os.path.join(site_path, "content")

def get_footer_path():
    return os.path.join(site_path, "footer.html")

def get_header_path():
    return os.path.join(site_path, "header.html")

def get_post_ending_path():
    return os.path.join(site_path, "post_ending.html")

def get_output_path():
    return os.path.join(site_path, "output")

def get_resource_path():
    return os.path.join(home_path, "resources")

def get_tag_path():
    return os.path.join(site_path, "tag")

##############################
# Load Site Functions
##############################

def read_config():
    with open(get_config_path()) as f:
        data = yaml.safe_load(f)
    return data

def read_footer():
    reader = open(get_footer_path(), "r")
    footer = reader.read()
    reader.close
    return footer

def read_header():
    reader = open(get_header_path(), "r")
    header = reader.read()
    reader.close
    return header

def read_post_ending():
    reader = open(get_post_ending_path(), "r")
    ending = reader.read()
    reader.close
    return ending


##############################
# Read Post Functions
##############################

def get_post_paths():
    paths = []
    for each in os.listdir(get_content_path()):
        if each.endswith(".html"):
            post_path = os.path.join(get_content_path(), each)
            paths.append(post_path)
    return paths

def load_post(file_path):
    post = {}
    with open(file_path) as f:  
        raw_data = f.read()
    split_data = raw_data.split(CONTENT_SEPARATOR)
    meta = yaml.safe_load(split_data[0])
    meta['slug'] = slugify(meta['title'])
    meta['datetime'] = dateutil.parser.parse(meta['date'])
    meta['pubDate'] = meta['datetime'].strftime("%a, %d %b %Y %H:%M:%S") + " GMT"
    #post['body'] = markdown.markdown(split_data[1])
    post['body'] = split_data[1]
    meta['description'] = re.sub(re.compile('<.*?>'), '', post['body'])[:160]
    post['meta'] = meta
    post['meta']['tags'] = process_tags(post['meta']['tags'])
    return post

def get_posts():
    posts = []
    for file_path in get_post_paths():
        post = load_post(file_path)
        posts.append(post)
    posts = sorted(posts, key = lambda i: i['meta']['datetime'], reverse=True)
    return posts


##############################
# Render Functions
##############################

def render_site():
    site = read_config()
    site['version'] = VERSION
    site['footer'] = read_footer()
    site['header'] = read_header()
    site['post_ending'] = read_post_ending()
    make_robots_txt()
    copy_favicon(site)
    render_404(site)
    make_tag_dir()
    posts = get_posts()
    render_front_page(site, posts)
    render_site_map(site, posts)
    render_rss(site, posts)
    render_css(site)

    for post in posts:
        render_post(site, post)

    tags = get_all_tags(posts)
    for tag in tags:
        render_tag(site, posts, tag)

def render_css(site):
    file_name = 'v' + site['version'] + "-gazette.css"
    file_path = os.path.join(get_output_path(), file_name)
    template = env.get_template('style.css')
    output = template.render()
    with open(file_path, 'w') as f:
        f.write(output)


def render_front_page(site, posts):
    file_path = os.path.join(get_output_path(), "index.html")
    template = env.get_template('frontpage.html')
    output = template.render(site=site, posts=posts)
    with open(file_path, 'w') as f:
        f.write(output)

def render_post(site, post):
    dir = os.path.join(get_output_path(), post['meta']['slug'])
    if not os.path.exists(dir):
        os.mkdir(dir)
    post_path = os.path.join(dir, "index.html")
    template = env.get_template('post.html')
    output = template.render(site=site, post=post)
    with open(post_path, 'w') as f:
        f.write(output)

def render_rss(site, posts):
    rss = {}
    rss['lastBuildDate'] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S") + " +0000"
    rss['pubDate'] = posts[0]['meta']['datetime'].strftime("%a, %d %b %Y %H:%M:%S") + " +0000"
    rss['generator'] = GENERATOR

    file_path = os.path.join(get_output_path(), "rss.xml")
    template = env.get_template('rss.xml')
    output = template.render(site=site, posts=posts, rss=rss)
    with open(file_path, 'w') as f:
        f.write(output)

def render_site_map(site, posts):
    file_path = os.path.join(get_output_path(), "sitemap.xml")
    template = env.get_template('sitemap.xml')
    output = template.render(site=site, posts=posts)
    with open(file_path, 'w') as f:
        f.write(output)

def render_404(site):
    dir = os.path.join(get_output_path(), "404")
    file_path = os.path.join(dir, "index.html")
    if not os.path.exists(dir):
        os.mkdir(dir)
    template = env.get_template('404.html')
    output = template.render(site=site)
    with open(file_path, 'w') as f:
        f.write(output)



def render_tag(site, posts, tag):
    selected_posts = []
    for post in posts:
        for each in post['meta']['tags']:
            if each['name'] == tag:
                selected_posts.append(post)
    #file_name = slugify(tag) + ".html"
    dir = os.path.join(get_output_path(), 'tag', slugify(tag))
    if not os.path.exists(dir):
        os.mkdir(dir)

    file_path = os.path.join(dir, 'index.html')
    template = env.get_template('tag.html')
    output = template.render(tag=tag, site=site, posts=posts)
    with open(file_path, 'w') as f:
        f.write(output)
    


##############################
# Initialize New Site Functions
##############################

def make_config_file():
    logging.info('      Creating config file')
    config_template = {
        "author": "",
        "baseURL": "",
        "title": "",
        "links": [{
            "url": "",
            "name": ""
            },]
    }
    with open(get_config_path(), 'w') as f:
        f.write(yaml.dump(config_template))

def make_site_directories():
    os.mkdir(get_content_path())
    logging.info('      Creating content directory')

    os.mkdir(get_output_path())
    logging.info('      Creating output directory')


def make_empty_files():
    logging.info('      Creating empty files')
    with open(get_footer_path(), 'w') as f:
        f.write("")
    with open(get_header_path(), 'w') as f:
        f.write("")
    with open(get_post_ending_path(), 'w') as f:
        f.write("")



def make_robots_txt():
    robots_txt = os.path.join(get_resource_path(), "robots.txt")
    if os.path.isfile(robots_txt):
        return

    body = """# www.robotstxt.org/

# Allow crawling of all content
User-agent: *
Disallow:   /tag/* """
    robots_path = os.path.join(get_output_path(), "robots.txt")
    with open(robots_path, 'w') as f:
        f.write(body)

def copy_favicon(site):
    site_ico_path = os.path.join(get_output_path(), "favicon.ico")
    custom_ico_path = os.path.join(get_content_path(), "favicon.ico")
    default_ico_path = os.path.join(get_resource_path(), "favicon.ico")

    if os.path.isfile(site_ico_path):
        return
    if os.path.isfile(custom_ico_path):
        copyfile(custom_ico_path, site_ico_path)
        return
    copyfile(default_ico_path, site_ico_path)

    



def initialize_new_site():
    make_config_file()
    make_site_directories()
    make_empty_files()

##############################
# Taxonomy Functions 
##############################

def process_tags(raw_tags):
    tags = []
    for each in raw_tags:
        tag = {}
        tag['name'] = each.lower()
        tag['slug'] = slugify(tag['name'])
        tags.append(tag)
    return tags

def get_all_tags(posts):
    tags = []
    for post in posts:
        for tag in post['meta']['tags']:
            tags.append(tag['name'])
    tags = list(set(tags))
    return tags


def make_tag_dir():
    path = os.path.join(get_output_path(), 'tag')
    if not os.path.exists(path):
        os.mkdir(path)

##############################
# Main
##############################

if __name__ == "__main__":
    if args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(format='%(message)s', level=log_level)

    site_path = args.path

    if args.initialize:
        logging.info('Initializing new site: ' + site_path)

        if os.path.exists(args.path):
            logging.info('  Directory already exits')

        else:
            logging.info('  Creating site directory')
            os.makedirs(site_path)

        if os.listdir(site_path):
            logging.info('  Directory already contains files')
            logging.info('  Initialization caneled')
            exit()
        
        initialize_new_site()
        exit()
    else:
        logging.info('Rendering site: ' + site_path)
        render_site()

        



