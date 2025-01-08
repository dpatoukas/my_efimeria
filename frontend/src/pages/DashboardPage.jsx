import React, { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Button,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from '@mui/material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const DashboardPage = () => {
  const [schedules, setSchedules] = useState([]); // Store fetched schedules
  const [loading, setLoading] = useState(true);  // Loading state
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false); // Dialog state
  const [scheduleToDelete, setScheduleToDelete] = useState(null);  // Schedule ID to delete
  const navigate = useNavigate();               // Navigation hook

  // Fetch schedules from API
  useEffect(() => {
    const fetchSchedules = async () => {
      try {
        const token = localStorage.getItem('token'); // Get JWT token
        const response = await axios.get('http://localhost:5000/api/schedules/history', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setSchedules(response.data); // Store fetched schedules
      } catch (error) {
        console.error('Error fetching schedules:', error);
      } finally {
        setLoading(false); // Stop loading
      }
    };
    fetchSchedules();
  }, []);

  // Navigate to Create Schedule Page
  const handleCreateSchedule = () => {
    navigate('/create-schedule');
  };

  // Navigate to Schedule Detail Page
  const handleScheduleClick = (id) => {
    navigate(`/schedule/${id}`);
  };

  // Open Delete Confirmation Dialog
  const handleDeleteClick = (id) => {
    setScheduleToDelete(id);
    setDeleteDialogOpen(true);
  };

  // Confirm Delete Schedule
  const handleConfirmDelete = async () => {
    try {
      const token = localStorage.getItem('token'); // Get JWT token
      await axios.delete(`http://localhost:5000/api/schedules/${scheduleToDelete}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      // Update the schedule list after deletion
      setSchedules((prevSchedules) => prevSchedules.filter(schedule => schedule.id !== scheduleToDelete));
      console.log(`Schedule ID ${scheduleToDelete} deleted successfully.`);
    } catch (error) {
      console.error(`Error deleting schedule ID ${scheduleToDelete}:`, error.response?.data || error.message);
    } finally {
      setDeleteDialogOpen(false);
      setScheduleToDelete(null);
    }
  };

  return (
    <Container>
      <Typography variant="h2" gutterBottom>
        Dashboard
      </Typography>

      {loading ? (
        <CircularProgress /> // Show spinner when loading
      ) : schedules.length === 0 ? (
        // Show only the button when no schedules exist
        <>
          <Typography>No schedules found. Click below to create one.</Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={handleCreateSchedule}
            style={{ marginTop: '1rem' }}
          >
            Create New Schedule
          </Button>
        </>
      ) : (
        // Show schedules and button when schedules exist
        <>
          {/* Add a Title for the Schedule List */}
          <Typography variant="h4" gutterBottom>
            Schedules
          </Typography>

          <List>
            {schedules.map((schedule) => (
              <ListItem key={schedule.id}>
                <ListItemText
                  primary={`${schedule.month} ${schedule.year}`}
                  secondary={`Status: ${schedule.status}`}
                />
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => handleScheduleClick(schedule.id)}
                  style={{ marginRight: '0.5rem' }}
                >
                  View
                </Button>
                <Button
                  variant="contained"
                  color="secondary"
                  onClick={() => handleDeleteClick(schedule.id)}
                >
                  Delete
                </Button>
              </ListItem>
            ))}
          </List>

          <Button
            variant="contained"
            color="primary"
            onClick={handleCreateSchedule}
            style={{ marginTop: '1rem' }}
          >
            Create New Schedule
          </Button>
        </>
      )}

      {/* Always show Manage Doctors button */}
      <Button
        variant="contained"
        color="secondary"
        onClick={() => navigate('/doctor-management')}
        style={{ marginTop: '1rem', marginLeft: '1rem' }}
      >
        Manage Doctors
      </Button>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
      >
        <DialogTitle>Confirm Deletion</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete this schedule? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)} color="primary">
            Cancel
          </Button>
          <Button onClick={handleConfirmDelete} color="secondary">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default DashboardPage;
