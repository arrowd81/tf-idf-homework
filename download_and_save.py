import os
from collections import deque

import wikipediaapi

# config
FOLDER_TO_DOWNLOAD = 'wikipedia_pages/'
DOWNLOAD_COUNT = 1000

# global vars
downloaded_pages = []


def save_downloaded_page(page):
    with open(FOLDER_TO_DOWNLOAD + page.title + '.txt', 'w', encoding='utf-8') as file:
        file.write(page.text)

    global downloaded_pages
    downloaded_pages.append(page.title)
    print(str(len(downloaded_pages)) + ': ' + page.title)


def download_and_save_dfs(page):
    save_downloaded_page(page)

    for link in page.links.values():
        global downloaded_pages
        if len(downloaded_pages) < DOWNLOAD_COUNT:
            if link.title not in downloaded_pages:
                download_and_save_dfs(link)
        else:
            break


def download_and_save_bfs(page):
    bfs_pages_to_download = deque((page,))
    save_downloaded_page(page)

    while len(bfs_pages_to_download) > 0:
        page = bfs_pages_to_download.popleft()
        for link in page.links.values():
            global downloaded_pages
            if len(downloaded_pages) < DOWNLOAD_COUNT:
                if link.title not in downloaded_pages:
                    save_downloaded_page(link)
                    bfs_pages_to_download.append(page)


def download():
    os.makedirs(FOLDER_TO_DOWNLOAD, exist_ok=True)

    wiki = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)', 'fa')

    title = 'ایران'

    first_page = wiki.page(title)

    download_and_save_bfs(first_page)


if __name__ == '__main__':
    download()
