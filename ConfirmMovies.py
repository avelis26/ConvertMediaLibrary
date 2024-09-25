# pip install opencv-python-headless imagehash requests Pillow

import os
import requests
import cv2
import imagehash
from PIL import Image
from io import BytesIO
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
success_log = "success_log.txt"
failure_log = "failure_log.txt"

# TMDb API configuration
API_KEY = "your_tmdb_api_key"
BASE_URL = "https://api.themoviedb.org/3/movie/"

# Directory to search for movies
SEARCH_DIR = "/mnt/data/Media/Movies"

# Function to fetch backdrops from TMDb
def fetch_backdrops(tmdb_id):
    url = f"{BASE_URL}{tmdb_id}/images"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        images = response.json().get('backdrops', [])
        return images
    else:
        logging.error(f"Failed to fetch backdrops for TMDb ID: {tmdb_id}")
        return []

# Function to calculate image hash
def calculate_image_hash(image_data):
    image = Image.open(BytesIO(image_data))
    return imagehash.average_hash(image)

# Function to extract frames from video using OpenCV
def extract_frames(video_file, interval=10):
    cap = cv2.VideoCapture(video_file)
    frames = []
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % interval == 0:  # Extract every Nth frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_frame = Image.fromarray(frame_rgb)
            frames.append(pil_frame)
        frame_count += 1
    cap.release()
    return frames

# Function to compare frame with backdrops
def compare_frames_with_backdrops(frames, backdrop_hashes, threshold=5):
    for frame in frames:
        frame_hash = imagehash.average_hash(frame)
        for backdrop_hash in backdrop_hashes:
            if frame_hash - backdrop_hash <= threshold:  # Hash difference <= threshold
                return True
    return False

# Main function to process movie directories
def process_movie_dirs():
    for movie_dir in os.listdir(SEARCH_DIR):
        movie_path = os.path.join(SEARCH_DIR, movie_dir)
        if os.path.isdir(movie_path):
            try:
                movie_name, release_year, tmdb_id = movie_dir.split('_')
                tmdb_id = tmdb_id.strip('[]')

                # Fetch backdrops
                backdrops = fetch_backdrops(tmdb_id)
                backdrop_hashes = []
                for backdrop in backdrops:
                    image_url = f"https://image.tmdb.org/t/p/original{backdrop['file_path']}"
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        backdrop_hash = calculate_image_hash(image_response.content)
                        backdrop_hashes.append(backdrop_hash)

                # Find the movie file in the directory
                movie_files = [f for f in os.listdir(movie_path) if f.endswith(('.mp4', '.mkv', '.avi'))]
                for movie_file in movie_files:
                    movie_file_path = os.path.join(movie_path, movie_file)

                    # Extract frames from the movie file
                    frames = extract_frames(movie_file_path)

                    # Compare the movie frames with backdrops
                    if compare_frames_with_backdrops(frames, backdrop_hashes):
                        logging.info(f"Success: {movie_name}, {movie_file_path}")
                        with open(success_log, 'a') as f:
                            f.write(f"{movie_name}, {movie_file_path}, Success\n")
                    else:
                        logging.info(f"Failure: {movie_name}, {movie_file_path}")
                        with open(failure_log, 'a') as f:
                            f.write(f"{movie_name}, {movie_file_path}, Failure\n")

            except Exception as e:
                logging.error(f"Error processing directory {movie_dir}: {e}")

if __name__ == "__main__":
    process_movie_dirs()
