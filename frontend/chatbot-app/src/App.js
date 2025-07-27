// frontend/src/App.js

import React, { useState, useCallback, useRef } from 'react';
import './App.css';
import './Chat.css';

import Chat from './Chat';
import CloudBackground from './CloudBackground';

function App() {
  // const [cloudQuestionToSend, setCloudQuestionToSend] = useState(null); // Remove this line
  const chatRef = useRef(null);

  const handleCloudClick = useCallback((question) => {
    if (chatRef.current) {
      chatRef.current.sendSpecificMessage(question);
    }
  }, []);

  const handleMessageSent = useCallback(() => {
    // This will trigger CloudBackground to re-fetch questions
    // by changing the key or a state prop if needed.
    // For now, we'll just rely on CloudBackground's internal useEffect [onCloudClick]
    // which will be triggered by CloudBackground's fetchRandomQuestions being called.
    // A simpler way is to just pass a counter or a specific trigger to CloudBackground.
    // Let's pass a simple state update to CloudBackground to trigger re-fetch.
    // setCloudQuestionToSend(null); // Remove or comment out this line as well
  }, []);

  return (
    <div className="App">
      <CloudBackground onCloudClick={handleCloudClick} />
      <Chat ref={chatRef} onSendMessage={handleMessageSent} />
    </div>
  );
}

export default App;
