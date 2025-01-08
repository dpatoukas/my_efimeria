import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Button,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  CircularProgress,
  Backdrop,
  Snackbar,
  Alert
} from '@mui/material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const CreateSchedulePage = () => {
  const [month, setMonth] = useState('');
  const [year, setYear] = useState('');
  const [days, setDays] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(false);
  const [alert, setAlert] = useState({ open: false, message: '', severity: 'success' });
  const navigate = useNavigate();

  // Global monthIndex for reuse
  const monthIndex = React.useMemo(() => [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
  ].indexOf(month), [month]);

  useEffect(() => {
    if (month && year) {
      fetchDoctorsAndDays();
    }
  }, [month, year]);

  const fetchDoctorsAndDays = async () => {
    if (monthIndex !== -1) {
      const daysInMonth = new Date(year, monthIndex + 1, 0).getDate();
      setDays([...Array(daysInMonth).keys()].map(d => d + 1));

      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:5000/api/doctors/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        const updatedDoctors = response.data.map(doctor => ({
          ...doctor,
          days_off: doctor.days_off.split(',')
        }));
        setDoctors(updatedDoctors);
      } catch (error) {
        console.error('Failed to fetch doctors:', error);
      }
    }
  };

  const toggleDayOff = (doctorId, day) => {
    const formattedDate = `${year}-${String(monthIndex + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    setDoctors(prevDoctors =>
      prevDoctors.map(doctor => {
        if (doctor.id === doctorId) {
          const updatedDaysOff = doctor.days_off.includes(formattedDate)
            ? doctor.days_off.filter(date => date !== formattedDate)
            : [...doctor.days_off, formattedDate];
          return { ...doctor, days_off: updatedDaysOff };
        }
        return doctor;
      })
    );
  };

  const updateDatabase = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      await Promise.all(doctors.map(async (doctor) => {
        await axios.put(`http://localhost:5000/api/doctors/${doctor.id}`, {
          days_off: doctor.days_off.join(',')
        }, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }));
      setAlert({ open: true, message: 'Data updated successfully!', severity: 'success' });
    } catch (error) {
      console.error('Failed to update database:', error);
      setAlert({ open: true, message: 'Failed to update data.', severity: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const generateSchedule = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      await axios.post('http://localhost:5000/api/schedules/generate', {
        month,
        year,
      }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setAlert({ open: true, message: 'Schedule generated successfully!', severity: 'success' });
      setTimeout(() => navigate('/dashboard'), 2000); // Redirect to dashboard after 2 seconds
    } catch (error) {
      console.error('Failed to generate schedule:', error);
      setAlert({ open: true, message: 'Failed to generate schedule.', severity: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Backdrop open={loading} style={{ zIndex: 1201 }}>
        <CircularProgress color="inherit" />
      </Backdrop>

      <Snackbar open={alert.open} autoHideDuration={6000} onClose={() => setAlert({ ...alert, open: false })}>
        <Alert severity={alert.severity} onClose={() => setAlert({ ...alert, open: false })}>
          {alert.message}
        </Alert>
      </Snackbar>

      <Typography variant="h2" gutterBottom>
        Create Schedule
      </Typography>

      <FormControl fullWidth>
        <InputLabel>Month</InputLabel>
        <Select value={month} onChange={e => setMonth(e.target.value)}>
          {[
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December',
          ].map(m => (
            <MenuItem key={m} value={m}>{m}</MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl fullWidth style={{ marginTop: '1rem' }}>
        <InputLabel>Year</InputLabel>
        <Select value={year} onChange={e => setYear(e.target.value)}>
          {[2024, 2025, 2026].map(y => (
            <MenuItem key={y} value={y}>{y}</MenuItem>
          ))}
        </Select>
      </FormControl>

      {days.length > 0 && (
        <TableContainer component={Paper} style={{ marginTop: '2rem', maxWidth: '100%' }}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell style={{ minWidth: '100px' }}>Doctor</TableCell>
                {days.map(day => <TableCell key={day} style={{ padding: '2px', minWidth: '20px' }}>{day}</TableCell>)}
              </TableRow>
            </TableHead>
            <TableBody>
              {doctors.map((doctor) => (
                <TableRow key={doctor.id}>
                  <TableCell style={{ padding: '2px', minWidth: '100px' }}>{doctor.name}</TableCell>
                  {days.map(day => (
                    <TableCell
                      key={day}
                      onClick={() => toggleDayOff(doctor.id, day)}
                      style={{ padding: '2px', cursor: 'pointer', backgroundColor: doctor.days_off.includes(`${year}-${String(monthIndex + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`) ? 'red' : 'white' }}>
                      {doctor.days_off.includes(`${year}-${String(monthIndex + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`) ? 'X' : ''}
                    </TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      <Button variant="contained" color="primary" onClick={updateDatabase} style={{ marginTop: '1rem' }}>
        Update Database
      </Button>
      <Button variant="contained" color="secondary" onClick={generateSchedule} style={{ marginTop: '1rem', marginLeft: '1rem' }}>
        Generate Schedule
      </Button>
    </Container>
  );
};

export default CreateSchedulePage;
