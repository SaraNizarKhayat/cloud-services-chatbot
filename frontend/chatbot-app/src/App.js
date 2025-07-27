// frontend/src/App.js

import React, { useState, useCallback, useRef } from 'react';
import './App.css';
import './Chat.css';

import Chat from './Chat';
import CloudBackground from './CloudBackground';

function App() {
  const [cloudQuestionToSend, setCloudQuestionToSend] = useState(null); // Keep this
  const [refreshCloudBackground, setRefreshCloudBackground] = useState(0); // New state for trigger
  const chatRef = useRef(null);

  const handleCloudClick = useCallback((question) => {
    if (chatRef.current) {
      chatRef.current.sendSpecificMessage(question);
    }
  }, []);

  const handleMessageSent = useCallback(() => {
    // Increment a counter to trigger re-fetch in CloudBackground
    setRefreshCloudBackground(prev => prev + 1);
    setCloudQuestionToSend(null); // Still clear this if it was a temporary state
  }, []);

  return (
    <div className="App">
      {/* Pass the new state as a prop to trigger CloudBackground's useEffect */}
      <CloudBackground onCloudClick={handleCloudClick} refreshTrigger={refreshCloudBackground} />
      <Chat ref={chatRef} onSendMessage={handleMessageSent} />
    </div>
  );
}

export default App;