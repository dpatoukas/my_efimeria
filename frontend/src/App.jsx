import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import NotFoundPage from './pages/NotFoundPage';
import ScheduleDetailPage from './pages/ScheduleDetailPage';
import CreateSchedulePage from './pages/CreateSchedulePage';
import ShiftResourcesPage from './pages/ShiftResourcesPage';
import PrivateRoute from './components/PrivateRoute';
import DoctorManagementPage from './pages/DoctorManagementPage.jsx';
import { Container } from '@mui/material';

/**
 * App Component - Entry point for the application.
 * Sets up routing and layout for the Clinic Scheduling System.
 *
 * Routes:
 * - "/" - Login Page (Public)
 * - "/dashboard" - Dashboard Page (Protected)
 * - "/schedule/:id" - Schedule Detail Page (Protected)
 * - "/create-schedule" - Create Schedule Page (Protected)
 * - "/shift-resources" - Shift Resources Page (Protected)
 * - "*" - Not Found Page (Fallback)
 */
const App = () => {
  return (
    <Router>
      <Container>
        <Routes>
          {/* Public Route: Login Page */}
          <Route path="/" element={<LoginPage />} />

          {/* Protected Routes */}
          <Route element={<PrivateRoute />}>
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/schedule/:id" element={<ScheduleDetailPage />} />
            <Route path="/create-schedule" element={<CreateSchedulePage />} />
            <Route path="/shift-resources" element={<ShiftResourcesPage />} />
            <Route path="/doctor-management" element={<DoctorManagementPage />} />
          </Route>

          {/* Catch-all Route for 404 Page */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Container>
    </Router>
  );
};

export default App;
