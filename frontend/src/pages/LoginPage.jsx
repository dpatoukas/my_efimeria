import React, { useState } from 'react';
import { Container, Typography, Button, TextField, Alert } from '@mui/material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/auth/login', {
        username,
        password,
      });

      // Store the token
      localStorage.setItem('token', response.data.access_token);

      // Redirect to Dashboard
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid username or password!');
    }
  };

  return (
    <Container>
      <Typography variant="h2" gutterBottom>
        Login
      </Typography>
      {error && <Alert severity="error">{error}</Alert>}
      <TextField
        label="Username"
        fullWidth
        margin="normal"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <TextField
        label="Password"
        type="password"
        fullWidth
        margin="normal"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <Button
        variant="contained"
        color="primary"
        style={{ marginTop: '1rem' }}
        onClick={handleLogin}
      >
        Login
      </Button>
    </Container>
  );
};

export default LoginPage;
