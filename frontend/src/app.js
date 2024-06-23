import React, { useState, useRef } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState("");
  const [disableInput, setDisableInput] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const inputReference = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    setDisableInput(true);
    setChatInput("");
    setChatMessages([...chatMessages, { username: "Du", message: chatInput }]);
    setIsLoading(true);

    fetch("http://127.0.0.1:5000/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question: chatInput })
    })
    .then(response => response.json())
    .then(response => {
      setIsLoading(false);
      setChatMessages([...chatMessages, { username: "Chatbot", message: response }]);
      setDisableInput(false);
    });
  };

  return (
    <div className="App container mt-5">
      <div className="chat">
        {chatMessages.map((msg, index) => (
          <div key={index} className="mb-3">
            <strong>{msg.username}: </strong> {msg.message}
          </div>
        ))}
        {isLoading && <div>Loading...</div>}
      </div>
      <form onSubmit={handleSubmit} className="mt-4">
        <div className="input-group">
          <input
            type="text"
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            disabled={disableInput}
            placeholder="Stelle eine Frage..."
            className="form-control"
          />
          <button type="submit" className="btn btn-primary" disabled={disableInput}>Senden</button>
        </div>
      </form>
    </div>
  );
}

export default App;
