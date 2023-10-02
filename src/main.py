from flask import Flask, send_file, request
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from io import BytesIO
import time

app = Flask(__name__)

@app.route("/")
def index():
    return send_file("../public/index.html")

@app.route("/generate_gif")
def generate_gif():
    end_time_str = request.args.get('end_time')
    if not end_time_str:
        return "end_time parameter is missing", 400

    # Convert end_time_str to datetime object
    end_time = datetime.fromisoformat(end_time_str)

    # Calculate remaining time in seconds
    remaining_seconds = int((end_time - datetime.utcnow()).total_seconds())
    
    # Create GIF frames
    frames = []
    for i in range(52, 6, -1):
        frame = Image.new('RGBA', (100, 100), 'white')
        d = ImageDraw.Draw(frame)

        # Draw remaining time text on the frame
        d.text((10, 40), f"{remaining_seconds} s", fill=(0, 0, 0))

        frames.append(frame)

        # Update remaining_seconds for the next frame
        remaining_seconds -= 1

    # Save frames as a GIF
    gif_buffer = BytesIO()
    frames[0].save(gif_buffer, save_all=True, append_images=frames[1:], loop=0, duration=1000)

    gif_buffer.seek(0)
    return send_file(gif_buffer, mimetype='image/gif')

if __name__ == "__main__":
    app.run(debug=True)
