from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import re
import requests
from decouple import config
from bs4 import BeautifulSoup
import os
class TikTokDownloader:
    def __init__(self):
        self.URI_BASE = 'https://ssstik.io'
        self.cookies = {
            '_ga': 'GA1.1.1912336417.1703419416',
            '_ga_ZSF3D6YSLC': 'GS1.1.1703419416.1.1.1703420307.0.0.0',
        }

        self.headers = {
            'authority': 'ssstik.io',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'hx-current-url': 'https://ssstik.io/en',
            'hx-request': 'true',
            'hx-target': 'target',
            'hx-trigger': '_gcaptcha_pt',
            'origin': 'https://ssstik.io',
            'referer': 'https://ssstik.io/en',
            'sec-ch-ua': '"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0',
        }

    def download_tiktok_video(self, link):
        params = {'url': 'dl'}
        data = {
            'id': link,
            'locale': 'en',
            'tt': 'VHk4eWs3',
        }

        response = requests.post(f'{self.URI_BASE}/abc', params=params, cookies=self.cookies, headers=self.headers, data=data)
        download_soup = BeautifulSoup(response.text, 'html.parser')
        download_link = download_soup.a['href']

        return download_link

def handle_media_links(update: Update, context: CallbackContext):
    tiktok_downloader = TikTokDownloader()
    text = update.message.text
    link_match = re.search(r'(https?://[^\s]+)', text)

    if link_match:
        link = link_match.group(1)
        if 'tiktok.com' in link:
            video_url = tiktok_downloader.download_tiktok_video(link)
            if video_url:
                # Send the video directly without saving it locally
                response = requests.get(video_url, stream=True)
                if response.status_code == 200:
                    context.bot.send_video(chat_id=update.effective_chat.id, video=response.raw)
            else:
                update.message.reply_text('Error processing TikTok video.')
        else:
            update.message.reply_text('Not a TikTok link.')
    else:
        update.message.reply_text('No valid link found.')

def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    BOT_TOKEN = config("BOT_TOKEN")
    updater = Updater(BOT_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_media_links))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
