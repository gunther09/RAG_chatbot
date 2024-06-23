import React from 'react';

function ChatMessage({ username, message }) {
  return (
    <div className="chat-message">
      <strong>{username}: </strong> {message}
    </div>
  );
}

export default ChatMessage;
