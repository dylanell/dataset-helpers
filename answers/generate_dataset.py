"""
Generate a dataset of question-answer pairs on a singular topic from
answers.com.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse

from text_utils import process_text


def test_qa_is_good(q, a):
    # reject if question or answer is None
    if (q is None) or (a is None):
        # print('[INFO]: qa rejected (None value)')
        return False

    # reject if answer contains a link
    link_flags = ['http', 'https', 'www', '.net', '.com', '.org', '.gov']
    if any(flag in a.text for flag in link_flags):
        # print('[INFO]: qa rejected (link flagged)')
        return False

    # if we got here qa pair is all good
    return True


def main():
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('read_url', help='answers.com topic url page')
    parser.add_argument('write_dir', help='dataset write directory')
    parser.add_argument('--min_samples', type=int, default=1000,
                        help='minimum number of samples to scrape')
    args = parser.parse_args()

    page_num = 0

    # create dataframe to hold question answer pairs
    df = pd.DataFrame(columns=['Question Raw', 'Answer Raw',
                               'Question Processed', 'Answer Processed'])

    print('[INFO]: scraping pages for \'{}\''.format(args.read_url))

    while len(df) < args.min_samples:
        # get page content using a mozilla user header string
        headers = {'User-Agent': 'Mozilla/5.0'}
        page = requests.get(
            args.read_url + '/best?page={}'.format(page_num),
            headers=headers)
        assert page.status_code == 200, 'page download unsuccessful'

        # make soup
        soup = BeautifulSoup(page.content, 'html.parser')

        print(f"[INFO]: scraping \'{soup.title.text}\', page: {page_num}")

        #question_blocks = soup.find_all('div', {'typeof': 'Question'})
        question_blocks = soup.find_all(
            'div', 
            {"class": "grid grid-cols-1 cursor-pointer justify-start items-start qCard my-4 p-4 bg-white md:rounded shadow-cardGlow"}
        )

        # check if questions on this page, otherwise break loop
        if len(question_blocks) > 0:
            for i, block in enumerate(question_blocks):
                # extract question and answer blocks
                q = block.find('h1', {'property': 'name'})
                a = block.find('div', {'property': 'content'})

                # if both question and answer present
                if test_qa_is_good(q, a):
                    # append q-a pair to dataframe
                    df = df.append({
                        'Question Raw': q.text,
                        'Answer Raw': a.text,
                        'Question Processed': process_text(q.text),
                        'Answer Processed': process_text(a.text)
                    }, ignore_index=True)

            page_num += 1
        else:
            print('[INFO]: end of content')
            break

    print('[INFO]: scraped {} pages and collected {} samples'.
          format(page_num + 1, len(df)))

    # write raw question/answers to csv
    df[['Question Raw', 'Answer Raw']].to_csv('{}qa_pairs_raw.csv'
                                              .format(args.write_dir),
                                              index=False)

    # write processed questions/answers to csv
    df[['Question Processed', 'Answer Processed']].applymap(
        lambda x: ' '.join(x)).to_csv(
        '{}qa_pairs_processed.csv'.format(args.write_dir), index=False)


if __name__ == '__main__':
    main()
