import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Typography, Box, Container, CircularProgress } from '@mui/material';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = async () => {
    if (input.trim() === '') return;

    const userMessage = { sender: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);
    setIsTyping(true);

    try {
      const response = await axios.post(process.env.REACT_APP_API_URL, {
        prompt: input,
        session_id: sessionId,
      });

      const message = response.data?.response;
      const session_id = response.data?.session_id;

      if (session_id && !sessionId) {
        setSessionId(session_id);
      }

      const botMessage = { sender: 'bot', text: message };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages((prev) => [...prev, { sender: 'bot', text: 'An error occurred. Please try again.' }]);
    } finally {
      setIsTyping(false);
    }

    setInput('');
  };

  return (
    <Container maxWidth={false} disableGutters sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', backgroundColor: '#f5f5f5', py: 4 }}>
      <Box sx={{ width: '80%', backgroundColor: '#fff', boxShadow: 3, borderRadius: 2, display: 'flex', flexDirection: 'column', minHeight: '80vh' }}>
        <Box sx={{ flex: 1, overflowY: 'auto', borderBottom: '1px solid #ccc', p: 2 }}>
          {messages.map((msg, index) => (
            <Typography
              key={index}
              align={msg.sender === 'user' ? 'right' : 'left'}
              sx={{ backgroundColor: msg.sender === 'user' ? '#e3f2fd' : '#f0f0f0', p: 1, borderRadius: 1, mb: 1 }}
            >
              {msg.text}
            </Typography>
          ))}
          {isTyping && (
            <Typography align="left" sx={{ fontStyle: 'italic', color: 'gray', mt: 1 }}>
              <CircularProgress size={16} sx={{ mr: 1 }} /> Typing...
            </Typography>
          )}
        </Box>
        <Box sx={{ display: 'flex', p: 2, backgroundColor: '#fff' }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          />
          <Button variant="contained" color="primary" onClick={handleSend} sx={{ ml: 1 }} disabled={isTyping}>
            Send
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default Chatbot;
