import asyncio
import websockets
import json
import os

VIDEO_DIR = 'Videos'




async def handler(websocket, path):
    # Handle CORS preflight request
    if websocket.request_headers.get("Origin"):
        await websocket.send(
            "HTTP/1.1 101 Switching Protocols\r\n"
            "Connection: Upgrade\r\n"
            "Upgrade: websocket\r\n"
            f"Access-Control-Allow-Origin: {websocket.request_headers['Origin']}\r\n"
            "Access-Control-Allow-Credentials: true\r\n"
            "\r\n"
        )

    async for message in websocket:
        data = json.loads(message)
        if data['type'] == 'start_stream':
            video_name = data['video_name']
            video_path = os.path.join(VIDEO_DIR, video_name)
            await start_streaming(websocket, video_path)
        elif data['type'] == 'get_videos':
            videos = os.listdir(VIDEO_DIR)
            await websocket.send(json.dumps({'type': 'video_list', 'videos': videos}))

async def start_streaming(websocket, video_path):
    uri = "ws://localhost:8766"
    async with websockets.connect(uri) as simulator_ws:
        await simulator_ws.send(json.dumps({'type': 'start_stream', 'video_path': video_path}))
        async for stream_data in simulator_ws:
            await websocket.send(stream_data)

async def main():
    async with websockets.serve(handler, "localhost", 8765, extra_headers=cors_headers):
        print("WebSocket server started")
        await asyncio.Future()  # Run forever

def cors_headers(path, request_headers):
    headers = [
        ("Access-Control-Allow-Origin", "*"),
        ("Access-Control-Allow-Headers", "Content-Type"),
        ("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    ]
    return headers

if __name__ == "__main__":
    asyncio.run(main())
