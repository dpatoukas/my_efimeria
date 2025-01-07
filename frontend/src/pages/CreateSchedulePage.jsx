import React, { useState } from 'react';
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
  TextField,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

const CreateSchedulePage = () => {
  const navigate = useNavigate();

  const [month, setMonth] = useState('');
  const [year, setYear] = useState('');
  const [doctorCount, setDoctorCount] = useState(1);
  const [days, setDays] = useState([]);
  const [doctorNames, setDoctorNames] = useState([]);
  const [dayOff, setDayOff] = useState({});

  const handleConfirm = () => {
    const monthIndex = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December',
    ].indexOf(month);

    if (monthIndex !== -1) {
      const daysInMonth = new Date(year, monthIndex + 1, 0).getDate();
      setDays([...Array(daysInMonth).keys()].map(d => d + 1));
      const initialNames = [...Array(doctorCount)].map((_, i) => `Doctor ${String.fromCharCode(65 + i)}`);
      setDoctorNames(initialNames);
      const initialDaysOff = {};
      for (let i = 0; i < doctorCount; i++) initialDaysOff[i] = [];
      setDayOff(initialDaysOff);
    }
  };

  const toggleDayOff = (index, day) => {
    setDayOff(prev => {
      const updatedDaysOff = { ...prev };
      if (updatedDaysOff[index]?.includes(day)) {
        updatedDaysOff[index] = updatedDaysOff[index].filter(d => d !== day);
      } else {
        updatedDaysOff[index] = [...(updatedDaysOff[index] || []), day];
      }
      return updatedDaysOff;
    });
  };

  const handleDoctorNameChange = (index, value) => {
    const newDoctorNames = [...doctorNames];
    newDoctorNames[index] = value.substring(0, 20);
    setDoctorNames(newDoctorNames);
  };

  const handleSave = async () => {
    try {
      // Save doctors and preferences first
      for (let i = 0; i < doctorNames.length; i++) {
        const doctor = {
          name: doctorNames[i],
          days_off: dayOff[i].length > 0
            ? dayOff[i].map(d => `${year}-${String(month).padStart(2, '0')}-${String(d).padStart(2, '0')}`).join(',')
            : null,

        };

        const doctorResponse = await fetch('http://localhost:5000/api/doctors/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
          body: JSON.stringify(doctor),
        });

        if (!doctorResponse.ok) throw new Error('Failed to save doctor preferences');
      }

      // Then save the schedule
      const scheduleResponse = await fetch('http://localhost:5000/api/schedules/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({ month, year: parseInt(year) }),
      });

      if (!scheduleResponse.ok) throw new Error('Failed to create schedule');

      alert('Doctors and schedule saved successfully!');
      navigate('/dashboard');
    } catch (error) {
      console.error(error);
      alert('Failed to save doctors and schedule.');
    }
  };

  return (
    <Container>
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
      <FormControl fullWidth>
        <InputLabel>Year</InputLabel>
        <Select value={year} onChange={e => setYear(e.target.value)}>
          {[2024, 2025, 2026].map(y => (
            <MenuItem key={y} value={y}>{y}</MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl fullWidth>
        <InputLabel>Number of Doctors</InputLabel>
        <Select value={doctorCount} onChange={e => setDoctorCount(e.target.value)}>
          {[...Array(10).keys()].map(n => (
            <MenuItem key={n + 1} value={n + 1}>{n + 1}</MenuItem>
          ))}
        </Select>
      </FormControl>
      <Button onClick={handleConfirm}>Confirm</Button>

      {days.length > 0 && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Doctor</TableCell>
                {days.map(day => <TableCell key={day}>{day}</TableCell>)}
              </TableRow>
            </TableHead>
            <TableBody>
              {doctorNames.map((name, index) => (
                <TableRow key={index}>
                  <TableCell>
                    <TextField value={name} onChange={e => handleDoctorNameChange(index, e.target.value)} />
                  </TableCell>
                  {days.map(day => (
                    <TableCell key={day} onClick={() => toggleDayOff(index, day)}>
                      {dayOff[index]?.includes(day) ? 'X' : ''}
                    </TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      <Button onClick={handleSave} color="primary" variant="contained" style={{ marginTop: '1rem' }}>
        Confirm Schedule
      </Button>
    </Container>
  );
};

export default CreateSchedulePage;
