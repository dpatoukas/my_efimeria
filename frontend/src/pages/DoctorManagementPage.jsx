import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Button,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  TextField,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  IconButton,
  Chip,
  Stack
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs from 'dayjs';
import axios from 'axios';

const DoctorManagementPage = () => {
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [newDoctorName, setNewDoctorName] = useState('');
  const [newDaysOff, setNewDaysOff] = useState([]);
  const [selectedDate, setSelectedDate] = useState(null);

  useEffect(() => {
    fetchDoctors();
  }, []);

  const fetchDoctors = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:5000/api/doctors/', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setDoctors(response.data);
    } catch (error) {
      console.error('Error fetching doctors:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddDoctor = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('http://localhost:5000/api/doctors/', {
        name: newDoctorName,
        days_off: newDaysOff.join(','),
      }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setDoctors([...doctors, response.data]);
      setOpen(false);
      setNewDoctorName('');
      setNewDaysOff([]);
    } catch (error) {
      console.error('Error adding doctor:', error);
    }
  };

  const handleDeleteDoctor = async (id) => {
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`http://localhost:5000/api/doctors/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setDoctors(doctors.filter((doctor) => doctor.id !== id));
    } catch (error) {
      console.error('Error deleting doctor:', error);
    }
  };

  const handleAddDayOff = () => {
    if (selectedDate) {
      const formattedDate = dayjs(selectedDate).format('YYYY-MM-DD');
      if (!newDaysOff.includes(formattedDate)) {
        setNewDaysOff([...newDaysOff, formattedDate]);
      }
    }
  };

  const handleRemoveDayOff = (date) => {
    setNewDaysOff(newDaysOff.filter((d) => d !== date));
  };

  return (
    <Container>
      <Typography variant="h2" gutterBottom>
        Doctor Management
      </Typography>
      {loading ? (
        <CircularProgress />
      ) : (
        <>
          <List>
            {doctors.map((doctor) => (
              <ListItem key={doctor.id}>
                <ListItemText
                  primary={doctor.name}
                  secondary={`Days Off: ${doctor.days_off}`}
                />
                <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteDoctor(doctor.id)}>
                  <DeleteIcon />
                </IconButton>
              </ListItem>
            ))}
          </List>
          <Button
            variant="contained"
            color="primary"
            onClick={() => setOpen(true)}
            style={{ marginTop: '1rem' }}
          >
            Add Doctor
          </Button>
        </>
      )}

      {/* Add Doctor Dialog */}
      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>Add New Doctor</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Doctor Name"
            fullWidth
            value={newDoctorName}
            onChange={(e) => setNewDoctorName(e.target.value)}
          />
          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DatePicker
              label="Select Day Off"
              value={selectedDate}
              onChange={(date) => setSelectedDate(date)}
            />
          </LocalizationProvider>
          <Button onClick={handleAddDayOff} style={{ marginTop: '1rem' }}>
            Add Day Off
          </Button>
          <Stack direction="row" spacing={1} style={{ marginTop: '1rem', flexWrap: 'wrap' }}>
            {newDaysOff.map((date) => (
              <Chip key={date} label={date} onDelete={() => handleRemoveDayOff(date)} />
            ))}
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button onClick={handleAddDoctor} color="primary">Add</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default DoctorManagementPage;
