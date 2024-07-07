import asyncio
import base64
import websockets
import cv2
import json

async def handler(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        if data['type'] == 'start_stream':
            video_path = data['video_path']
            await stream_video(websocket, video_path)

async def stream_video(websocket, video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = base64.b64encode(buffer).decode('utf-8')
        await websocket.send(frame_data)
    cap.release()

async def main():
    async with websockets.serve(handler, "localhost", 8766, ping_interval=None, ping_timeout=None):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
