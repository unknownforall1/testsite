import os
import yt_dlp
import tempfile
from flask import Flask, render_template_string, request, send_file, redirect, url_for
from youtubesearchpython import VideosSearch

import time
import sys
import asyncio
from os import execle, getenv, environ

from pyrogram import Client, filters, idle
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from pyrogram.errors import FloodWait
import time
import multiprocessing
import tgcrypto

api_id = '5461760'
api_hash = '396b10bcf5e1ed5fcc71f1603800b7cf'
bot_token="7172656487:AAFGBHEWvjg-Z2ysgK5nYJ_eJ8o7zXVsQJk"






# Ping route to keep the app alive on Replit
import logging
from flask import Flask
# Configure logging
logging.basicConfig(level=logging.INFO)  # Set log level to INFO

import os
import yt_dlp
import tempfile
import threading  # Add threading for background tasks
from flask import Flask, render_template_string, request, send_file, redirect, url_for
from youtubesearchpython import VideosSearch


app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>YouTube Video Downloader and Search</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    background-color: black;
                    color: white;
                    text-align: center;
                }
                .tab-container {
                    display: flex;
                    justify-content: center;
                    margin: 20px 0;
                }
                .tab {
                    padding: 10px 20px;
                    margin: 0 10px;
                    cursor: pointer;
                    background-color: gray;
                    border-radius: 10px;
                    color: white;
                }
                .tab.active {
                    background-color: white;
                    color: black;
                }
                .content {
                    display: none;
                }
                .content.active {
                    display: block;
                }
                .form-container { 
                    margin: 20px auto; 
                    width: 60%; 
                    background-color: rgba(255, 255, 255, 0.1); 
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
                    text-align: center;
                }
                .input-box {
                    width: 80%;
                    padding: 10px;
                    margin: 10px auto;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    font-size: 16px;
                }
                .submit-button {
                    padding: 10px 20px;
                    font-size: 16px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                .submit-button:hover {
                    background-color: #45a049;
                }
                .video-item {
                    display: flex;
                    align-items: center;
                    margin: 10px 0;
                    padding: 10px;
                    background-color: rgba(255, 255, 255, 0.2);
                    border-radius: 10px;
                    transition: background-color 0.3s;
                    cursor: pointer;
                }
                .video-item:hover {
                    background-color: rgba(255, 255, 255, 0.3);
                }
                .video-thumbnail {
                    width: 160px;
                    height: 90px;
                    object-fit: cover;
                    border-radius: 5px;
                    margin-right: 20px;
                }
                .video-details {
                    flex-grow: 1;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    text-align: left;
                }
                .video-title {
                    font-size: 18px;
                    font-weight: bold;
                    color: white;
                }
                .video-title:hover {
                    text-decoration: underline;
                }
                .video-duration {
                    font-size: 14px;
                    color: #ccc;
                }
                .quality-tab-container {
                    display: flex;
                    justify-content: center;
                    margin: 20px 0;
                }
                .quality-tab {
                    padding: 10px 20px;
                    margin: 0 10px;
                    cursor: pointer;
                    background-color: gray;
                    border-radius: 10px;
                    color: white;
                }
                .quality-tab.active {
                    background-color: white;
                    color: black;
                }
                .quality-content {
                    display: none;
                }
                .quality-content.active {
                    display: block;
                }
            </style>
            <script>
                function showTab(tabId) {
                    const tabs = document.querySelectorAll('.tab');
                    const contents = document.querySelectorAll('.content');
                    tabs.forEach(tab => tab.classList.remove('active'));
                    contents.forEach(content => content.classList.remove('active'));
                    document.getElementById(tabId).classList.add('active');
                    document.getElementById(tabId + '-content').classList.add('active');
                }

                function showQualityTab(tabId) {
                    const tabs = document.querySelectorAll('.quality-tab');
                    const contents = document.querySelectorAll('.quality-content');
                    tabs.forEach(tab => tab.classList.remove('active'));
                    contents.forEach(content => content.classList.remove('active'));
                    document.getElementById(tabId).classList.add('active');
                    document.getElementById(tabId + '-content').classList.add('active');
                }
            </script>
        </head>
        <body onload="showTab('downloader')">
            <div class="tab-container">
                <div id="downloader" class="tab active" onclick="showTab('downloader')">YouTube Downloader</div>
                <div id="search" class="tab" onclick="showTab('search')">YouTube Search</div>
            </div>
            <div id="downloader-content" class="content active">
                <div class="form-container">
                    <form method="POST" action="/get_formats">
                        <input type="text" id="url" name="url" class="input-box" placeholder="Paste YouTube URL here" required>
                        <button type="submit" class="submit-button">Check and Download</button>
                    </form>
                </div>
            </div>
            <div id="search-content" class="content">
                <div class="form-container">
                    <form method="POST" action="/search_videos">
                        <input type="text" id="query" name="query" class="input-box" placeholder="Search for videos" required>
                        <button type="submit" class="submit-button">Search</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
    ''')
# Updated styles and templates for the get_formats route
@app.route('/get_formats', methods=['POST'])
def get_formats():
    url = request.form['url']
    audio_formats, video_formats = get_audio_and_video_formats(url)
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Select Format</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    background-color: black;
                    color: white;
                    text-align: center;
                }
                .quality-tab-container {
                    display: flex;
                    justify-content: center;
                    margin: 20px 0;
                }
                .quality-tab {
                    padding: 10px 20px;
                    margin: 0 10px;
                    cursor: pointer;
                    background-color: gray;
                    border-radius: 10px;
                    color: white;
                }
                .quality-tab.active {
                    background-color: white;
                    color: black;
                }
                .quality-content {
                    display: none;
                }
                .quality-content.active {
                    display: block;
                }
                .form-container {
                    margin: 20px auto; 
                    width: 60%; 
                    background-color: rgba(255, 255, 255, 0.1); 
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
                }
                .quality-options {
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                    gap: 10px;
                }
                .quality-option {
                    font-size: 19.2px; /* Increased by 20% from 16px */
                    padding: 10px;
                    background-color: rgba(255, 255, 255, 0.2);
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }
                .quality-option:hover {
                    background-color: rgba(255, 255, 255, 0.3);
                }
                .submit-button {
                    padding: 10px 20px;
                    font-size: 19.2px; /* Increased by 20% */
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                .submit-button:hover {
                    background-color: #45a049;
                }
            </style>
            <script>
                function showQualityTab(tabId) {
                    const tabs = document.querySelectorAll('.quality-tab');
                    const contents = document.querySelectorAll('.quality-content');
                    tabs.forEach(tab => tab.classList.remove('active'));
                    contents.forEach(content => content.classList.remove('active'));
                    document.getElementById(tabId).classList.add('active');
                    document.getElementById(tabId + '-content').classList.add('active');
                }
            </script>
        </head>
        <body onload="showQualityTab('audio')">
            <div class="quality-tab-container">
                <div id="audio" class="quality-tab active" onclick="showQualityTab('audio')">Audio Only</div>
                <div id="video" class="quality-tab" onclick="showQualityTab('video')">Video with Audio</div>
            </div>
            <div id="audio-content" class="quality-content active">
                <div class="form-container">
                    <form method="POST" action="/download">
                        <input type="hidden" name="url" value="{{ url }}">
                        <div class="quality-options">
                            {% for fmt in audio_formats %}
                            <div class="quality-option">
                                <input type="radio" id="{{ fmt['format_id'] }}" name="format_id" value="{{ fmt['format_id'] }}" required>
                                <label for="{{ fmt['format_id'] }}">{{ fmt['label'] }}</label>
                            </div>
                            {% endfor %}
                        </div>
                        <button type="submit" class="submit-button">Download</button>
                    </form>
                </div>
            </div>
            <div id="video-content" class="quality-content">
                <div class="form-container">
                    <form method="POST" action="/download">
                        <input type="hidden" name="url" value="{{ url }}">
                        <div class="quality-options">
                            {% for fmt in video_formats %}
                            <div class="quality-option">
                                <input type="radio" id="{{ fmt['format_id'] }}" name="format_id" value="{{ fmt['format_id'] }}" required>
                                <label for="{{ fmt['format_id'] }}">{{ fmt['label'] }}</label>
                            </div>
                            {% endfor %}
                        </div>
                        <button type="submit" class="submit-button">Download</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
    ''', url=url, audio_formats=audio_formats, video_formats=video_formats)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_id = request.form['format_id']
    file_path, filename = download_with_ytdlp(url, format_id)
    return send_file(file_path, as_attachment=True, download_name=filename)

@app.route('/search_videos', methods=['POST'])
def search_videos():
    query = request.form['query']
    search_results = search_youtube_videos(query)
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Search Results</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    background-color: black;
                    color: white;
                    text-align: center;
                }
                .video-item {
                    display: flex;
                    align-items: center;
                    margin: 10px 0;
                    padding: 10px;
                    background-color: rgba(255, 255, 255, 0.2);
                    border-radius: 10px;
                    transition: background-color 0.3s;
                    cursor: pointer;
                }
                .video-item:hover {
                    background-color: rgba(255, 255, 255, 0.3);
                }
                .video-thumbnail {
                    width: 160px;
                    height: 90px;
                    object-fit: cover;
                    border-radius: 5px;
                    margin-right: 20px;
                }
                .video-details {
                    flex-grow: 1;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    text-align: left;
                }
                .video-title {
                    font-size: 18px;
                    font-weight: bold;
                    color: white;
                }
                .video-title:hover {
                    text-decoration: underline;
                }
                .video-duration {
                    font-size: 14px;
                    color: #ccc;
                }
            </style>
        </head>
        <body>
            {% for video in search_results %}
            <div class="video-item" onclick="window.location.href='/select_format?url={{ video['url'] }}'">
                <img src="{{ video['thumbnail'] }}" class="video-thumbnail" alt="Thumbnail">
                <div class="video-details">
                    <div class="video-title">{{ video['title'] }}</div>
                    <div class="video-duration">{{ video['duration'] }}</div>
                </div>
            </div>
            {% endfor %}
        </body>
        </html>
    ''', search_results=search_results)

@app.route('/select_format', methods=['GET'])
def select_format():
    url = request.args.get('url')
    audio_formats, video_formats = get_audio_and_video_formats(url)
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Select Format</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    background-color: black;
                    color: white;
                    text-align: center;
                }
                .quality-tab-container {
                    display: flex;
                    justify-content: center;
                    margin: 20px 0;
                }
                .quality-tab {
                    padding: 10px 20px;
                    margin: 0 10px;
                    cursor: pointer;
                    background-color: gray;
                    border-radius: 10px;
                    color: white;
                }
                .quality-tab.active {
                    background-color: white;
                    color: black;
                }
                .quality-content {
                    display: none;
                }
                .quality-content.active {
                    display: block;
                }
                .form-container {
                    margin: 20px auto; 
                    width: 60%; 
                    background-color: rgba(255, 255, 255, 0.1); 
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
                }
                .submit-button {
                    padding: 10px 20px;
                    font-size: 16px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                .submit-button:hover {
                    background-color: #45a049;
                }
            </style>
            <script>
                function showQualityTab(tabId) {
                    const tabs = document.querySelectorAll('.quality-tab');
                    const contents = document.querySelectorAll('.quality-content');
                    tabs.forEach(tab => tab.classList.remove('active'));
                    contents.forEach(content => content.classList.remove('active'));
                    document.getElementById(tabId).classList.add('active');
                    document.getElementById(tabId + '-content').classList.add('active');
                }
            </script>
        </head>
        <body onload="showQualityTab('audio')">
            <div class="quality-tab-container">
                <div id="audio" class="quality-tab active" onclick="showQualityTab('audio')">Audio Only</div>
                <div id="video" class="quality-tab" onclick="showQualityTab('video')">Video with Audio</div>
            </div>
            <div id="audio-content" class="quality-content active">
                <div class="form-container">
                    <form method="POST" action="/download">
                        <input type="hidden" name="url" value="{{ url }}">
                        {% for fmt in audio_formats %}
                        <div>
                            <input type="radio" id="{{ fmt['format_id'] }}" name="format_id" value="{{ fmt['format_id'] }}" required>
                            <label for="{{ fmt['format_id'] }}">{{ fmt['label'] }}</label>
                        </div>
                        {% endfor %}
                        <button type="submit" class="submit-button">Download</button>
                    </form>
                </div>
            </div>
            <div id="video-content" class="quality-content">
                <div class="form-container">
                    <form method="POST" action="/download">
                        <input type="hidden" name="url" value="{{ url }}">
                        {% for fmt in video_formats %}
                        <div>
                            <input type="radio" id="{{ fmt['format_id'] }}" name="format_id" value="{{ fmt['format_id'] }}" required>
                            <label for="{{ fmt['format_id'] }}">{{ fmt['label'] }}</label>
                        </div>
                        {% endfor %}
                        <button type="submit" class="submit-button">Download</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
    ''', url=url, audio_formats=audio_formats, video_formats=video_formats)

def get_audio_and_video_formats(url):
    import yt_dlp  # Import yt_dlp module
    ydl_opts = {'listformats': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict['formats']
        audio_formats = []
        video_formats = []

        # Predefined labels for video quality
        labels = ['low', 'medium', 'high']

        # Dictionary to track available video qualities
        available_video_qualities = {
            'low': False,
            'medium': False,
            'high': False,
            'full_hd': False
        }

        # Dictionary to track available audio formats
        available_audio_formats = {}

        # Process each format
        for fmt in formats:
            if fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':
                if fmt['ext'] == 'webm':
                    label = labels[len(audio_formats) % len(labels)]  # Cycle through 'low', 'medium', 'high'
                    audio_formats.append({'format_id': fmt['format_id'], 'label': label})
                    available_audio_formats[label] = True

            elif fmt.get('acodec') != 'none' and fmt.get('vcodec') != 'none':
                if fmt['ext'] == 'mp4':
                    height = fmt.get('height', 0)

                    if 100 < height <= 280:
                        label = 'low'
                        available_video_qualities['low'] = True
                    elif 310 <= height <= 650:
                        label = 'medium'
                        available_video_qualities['medium'] = True
                    elif 660 <= height < 1000:
                        label = 'high'
                        available_video_qualities['high'] = True
                    elif height >= 1000:
                        label = 'full_hd'
                        available_video_qualities['full_hd'] = True
                    else:
                        label = f"{height}p"

                    video_formats.append({'format_id': fmt['format_id'], 'label': label})

        # Add 'not available' entries for missing video qualities
        for quality, available in available_video_qualities.items():
            if not available:
                video_formats.append({'format_id': 'not_available', 'label': f"{quality} (not available)"})

        # Add 'not available' entries for missing audio qualities
        for label in labels:
            if label not in available_audio_formats:
                audio_formats.append({'format_id': 'not_available', 'label': f"{label} (not available)"})

    # Sort video formats by quality level
    video_formats.sort(key=lambda x: labels.index(x['label']) if x['label'] in labels else len(labels))

    # Return audio and video formats
    return audio_formats, video_formats


def download_with_ytdlp(url, format_id):
    temp_dir = tempfile.gettempdir()
    ydl_opts = {
        'format': format_id,
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info_dict)

        # If downloading audio, rename the file extension to .mp3
        if info_dict['acodec'] != 'none' and info_dict['vcodec'] == 'none':
            new_file_path = os.path.splitext(file_path)[0] + '.mp3'
            os.rename(file_path, new_file_path)
            file_path = new_file_path

    return file_path, os.path.basename(file_path)

def search_youtube_videos(query):
    search = VideosSearch(query, limit=10)
    results = search.result()['result']
    videos = []
    for result in results:
        videos.append({
            'url': result['link'],
            'title': result['title'],
            'thumbnail': result['thumbnails'][0]['url'],
            'duration': result['duration'],
        })
    return videos




# Ping route to keep the app alive on Replit or similar platforms
@app.route('/ping')
def ping():
    app.logger.info('Ping request received')  # Log a message when /ping is accessed
    return 'Ping successful!'





def run_flask_app():
    app.run(host='0.0.0.0', port=8080, debug=True)

# Function to print numbers indefinitely
def print_numbers():
    i = 1
    while True:
        print(i)
        i += 1
        time.sleep(1)

# Main entry point
if __name__ == '__main__':
    # Start the Flask app in a separate process
    flask_process = multiprocessing.Process(target=run_flask_app)
    flask_process.start()

    # Give the Flask app some time to start up
    time.sleep(2)  # Adjust if necessary to ensure the server starts

    # Start printing numbers
    print_numbers()
