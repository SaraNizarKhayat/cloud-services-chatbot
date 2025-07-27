// frontend/src/App.js

import React, { useState, useCallback, useRef } from 'react'; // Added useRef here
import './App.css'; // For global body styles
import './Chat.css'; // For all chat and cloud specific styles

import Chat from './Chat'; // Import our Chat component
import CloudBackground from './CloudBackground'; // Import the new CloudBackground component

function App() {
  const [cloudQuestionToSend, setCloudQuestionToSend] = useState(null);
  const chatRef = useRef(null); // Ref to access methods of the Chat component

  // Callback to handle clicks from clouds
  const handleCloudClick = useCallback((question) => {
    // This function will directly send the message to the backend
    // and then update the Chat component's messages state.
    if (chatRef.current) {
      chatRef.current.sendSpecificMessage(question);
    }
  }, []);

  // Callback for when a message is sent from the Chat component
  const handleMessageSent = useCallback(() => {
    // This will trigger CloudBackground to re-fetch questions
    // by changing the key or a state prop if needed.
    // For now, we'll just rely on CloudBackground's internal useEffect [onCloudClick]
    // which will be triggered by CloudBackground's fetchRandomQuestions being called.
    // A simpler way is to just pass a counter or a specific trigger to CloudBackground.
    // Let's pass a simple state update to CloudBackground to trigger re-fetch.
    setCloudQuestionToSend(null); // Clear the question after it's processed
  }, []);

  return (
    <div className="App">
      {/* CloudBackground is a sibling to Chat, so it positions relative to body */}
      <CloudBackground onCloudClick={handleCloudClick} /> {/* Pass the function to CloudBackground */}
      <Chat ref={chatRef} onSendMessage={handleMessageSent} /> {/* Pass ref to Chat */}
    </div>
  );
}

export default App;
