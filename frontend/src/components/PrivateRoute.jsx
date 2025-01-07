import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

// Check if the user is authenticated
const PrivateRoute = () => {
  const token = localStorage.getItem('token');
  return token ? <Outlet /> : <Navigate to="/" />;
};

export default PrivateRoute;
