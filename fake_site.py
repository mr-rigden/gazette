import argparse
from faker import Faker
import logging
import os
import random
import yaml


fake = Faker()

parser = argparse.ArgumentParser(description='Generates fake content for Gazette')
parser.add_argument("-c", "--count", help="Number of posts to generate", type=int, required=True)
parser.add_argument('path', help="path to site")
args = parser.parse_args()

log_level = logging.INFO
logging.basicConfig(format='%(message)s', level=log_level)

def generate_title():
    number = random.randint(4,7)
    title = fake.sentence(nb_words=number, variable_nb_words=True, ext_word_list=None)
    return title

def generate_tags():
    number = random.randint(0,8)
    tags = fake.words(nb=number, ext_word_list=None, unique=False)
    #tags = []
    return tags


def generate_content(content_path):
    header = {}
    header['title'] = generate_title()
    header['date'] = fake.date(pattern="%m/%d/%Y", end_datetime=None)
    header['tags'] = generate_tags()
    number = random.randint(5,50)
    body = fake.paragraph(nb_sentences=number, variable_nb_sentences=True, ext_word_list=None)

    file_name = str(random.randint(0,1000000000)) + ".html"
    file_path = os.path.join(content_path, file_name)
    output = yaml.dump(header) + '==========\n' +  body
    with open(file_path, 'w') as f:
        f.write(output)




if __name__ == "__main__":
    site_path = args.path
    content_path = os.path.join(args.path, "content")
    if not os.path.exists(content_path):
        logging.info('Content directory not found')
        exit()
    if os.listdir(content_path) :
        print("Content directory already contains files")
        exit()
    logging.info('Generating content')
    for each in range(args.count):
        logging.info("  " + str(each +1) + " of " + str(args.count))
        generate_content(content_path)
