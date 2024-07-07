// import { useState } from 'react'
import './App.css'

import React, { useEffect, useState, useRef } from 'react';

function App() {
  const [videos, setVideos] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState('');
  const videoRef = useRef(null);
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket('ws://localhost:8765');

    ws.current.onopen = () => {
      ws.current.send(JSON.stringify({ type: 'get_videos' }));
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'video_list') {
        setVideos(data.videos);
      } else {
        const blob = new Blob([event.data], { type: 'video/mp4' });
        videoRef.current.src = URL.createObjectURL(blob);
      }
    };

    return () => {
      ws.current.close();
    };
  }, []);

  const startStreaming = () => {
    ws.current.send(JSON.stringify({ type: 'start_stream', video_name: selectedVideo }));
  };

  return (
    <div>
      <h1>Video Streaming Dashboard</h1>
      <div>
        <label htmlFor="videos">Choose a video:</label>
        <select id="videos" onChange={(e) => setSelectedVideo(e.target.value)} value={selectedVideo}>
          {videos.map((video, index) => (
            <option key={index} value={video}>
              {video}
            </option>
          ))}
        </select>
        <button onClick={startStreaming}>Start Streaming</button>
      </div>
      <video ref={videoRef} width="600" controls autoPlay></video>
    </div>
  );
}

export default App;
