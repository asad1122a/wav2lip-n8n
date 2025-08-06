from flask import Flask, request, jsonify
import os
import subprocess
import uuid

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    script = data.get('script')
    bg_video_url = data.get('bg_video_url')

    if not script or not bg_video_url:
        return jsonify({'error': 'Missing script or background video URL'}), 400

    uid = str(uuid.uuid4())
    input_text = f"{uid}.txt"
    output_path = f"{uid}.mp4"

    # Save script to file
    with open(input_text, "w") as f:
        f.write(script)

    try:
        subprocess.run([
            "python3", "inference.py",
            "--checkpoint_path", "checkpoints/wav2lip_gan.pth",
            "--face", bg_video_url,
            "--outfile", output_path,
            "--audio", "audio.mp3",  # Replace if dynamic audio added later
            "--text", input_text
        ], check=True)

        # Upload to file.io (or similar) and return URL
        result = subprocess.check_output(["curl", "-F", f"file=@{output_path}", "https://file.io"]).decode()
        return jsonify({'video_url': eval(result)['link']})

    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if os.path.exists(input_text): os.remove(input_text)
        if os.path.exists(output_path): os.remove(output_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
