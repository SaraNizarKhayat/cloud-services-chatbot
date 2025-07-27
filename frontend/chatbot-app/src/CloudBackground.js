// frontend/src/CloudBackground.js

import React, { useState, useEffect } from 'react';
// Note: Chat.css already contains the .cloud-container and .cloud-item styles
// We'll rely on App.js to import Chat.css or a dedicated global CSS if preferred.

function CloudBackground({ onCloudClick }) {
  const [suggestedQuestions, setSuggestedQuestions] = useState([]);

  // Function to fetch random questions from the backend
  const fetchRandomQuestions = async () => {
    try {
      // Significantly increased count to 50 for very dense coverage
      const response = await fetch('http://127.0.0.1:8000/random_questions?count=50');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setSuggestedQuestions(data.questions);
    } catch (error) {
      console.error("Error fetching random questions for clouds:", error);
      // Optionally, you might want to display a subtle message to the user
      // that suggested questions couldn't load, but not critical for background.
    }
  };

  // Fetch random questions on component mount and whenever a message is sent (via onCloudClick prop change)
  useEffect(() => {
    fetchRandomQuestions();
  }, [onCloudClick]); // Re-fetch when onCloudClick changes, which happens after a message is sent

  return (
    <div className="cloud-container">
      {suggestedQuestions.map((q, index) => {
        // Generate a random size for the cloud (e.g., 100px to 160px)
        const minSize = 70;
        const maxSize = 70;
        const sizePx = Math.random() * (maxSize - minSize) + minSize;

        // AGGRESSIVE POSITIONING: Allow clouds to spawn far off-screen
        // This range (-100% to 200%) means clouds can start and end completely off-screen,
        // ensuring they float across the entire visible area.
        const randomTop = Math.random() * 20; // Range from -100 to 200
        const randomLeft = Math.random() * 100; // Range from -100 to 200

        const animationDelay = `${Math.random() * 15}s`; // Longer random delay for less synchronized movement
        const animationDuration = `${30 + Math.random() * 20}s`; // Even longer, more varied duration (30-50s) for very slow, natural float

        return (
          <div
            key={index}
            className="cloud" /* Changed class name to "cloud" */
            style={{
              top: `${randomTop}vh`,
              left: `${randomLeft}vw`,
              animationDelay,
              // Removed width and height here, as they are now defined in CSS
              animation: `float ${animationDuration} ease-in-out infinite ${animationDelay}`,
              zIndex: Math.floor(Math.random() * 5) + 1 // Random z-index for layering
            }}
            onClick={() => onCloudClick(q)} // Call the prop function on click
          ><div className="cloud-text"> 
              {q}
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default CloudBackground;
