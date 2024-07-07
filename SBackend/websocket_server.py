import asyncio
import websockets
import json
import os

VIDEO_DIR = 'Videos'

async def handler(websocket, path):
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            data = json.loads(message)
            if data['type'] == 'start_stream':
                video_name = data['video_name']
                print(f"Starting stream for: {video_name}")
                video_path = os.path.join(VIDEO_DIR, video_name)
                await start_streaming(websocket, video_path)
            elif data['type'] == 'get_videos':
                print("Sending video list")
                videos = os.listdir(VIDEO_DIR)
                await websocket.send(json.dumps({'type': 'video_list', 'videos': videos}))
    except Exception as e:
        print(f"Error in handler: {e}")

        
async def start_streaming(websocket, video_path):
    uri = "ws://localhost:8766"
    async with websockets.connect(uri) as simulator_ws:
        await simulator_ws.send(json.dumps({'type': 'start_stream', 'video_path': video_path}))
        async for stream_data in simulator_ws:
            await websocket.send(stream_data)

async def main():
    async with websockets.serve(handler, "localhost", 8765, process_request=process_cors, ping_interval=None, ping_timeout=None):
        print("WebSocket server started")
        await asyncio.Future()  # Run forever

async def process_cors(path, request_headers):
    allowed_origins = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://your-frontend-domain.com"
    ]
    if "Origin" in request_headers and request_headers["Origin"] in allowed_origins:
        return {
            "Access-Control-Allow-Origin": request_headers["Origin"],
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    return None  # Origin not allowed

if __name__ == "__main__":
    asyncio.run(main())
