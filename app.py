import os
import time
import threading
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory
from downloader import download_youtube_video
from processor import process_video

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'data/uploads'
OUTPUT_FOLDER = 'data/output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Job store (in-memory for this personal tool)
jobs = {}

def run_job(job_id, url, thickness, brightness, jitter, is_preview):
    try:
        jobs[job_id]['status'] = 'downloading'
        video_path = download_youtube_video(url, UPLOAD_FOLDER)

        jobs[job_id]['status'] = 'processing'
        output_filename = f"{job_id}.mp4"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        duration = 5 if is_preview else None
        process_video(video_path, output_path, thickness, brightness, jitter, duration)

        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['output_file'] = output_filename
    except Exception as e:
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['error'] = str(e)
        print(f"Job {job_id} failed: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    url = data.get('url')
    thickness = int(data.get('thickness', 1))
    brightness = float(data.get('brightness', 1.0))
    jitter = int(data.get('jitter', 0))
    is_preview = data.get('preview', True)

    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        'status': 'queued',
        'url': url,
        'is_preview': is_preview,
        'created_at': time.time()
    }

    thread = threading.Thread(target=run_job, args=(job_id, url, thickness, brightness, jitter, is_preview))
    thread.start()

    return jsonify({'job_id': job_id})

@app.route('/status/<job_id>')
def status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    return jsonify(job)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

@app.route('/job/<job_id>')
def job_page(job_id):
    return render_template('job.html', job_id=job_id)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5005, debug=True)
