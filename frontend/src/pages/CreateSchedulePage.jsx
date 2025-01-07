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
} from '@mui/material';
import axios from 'axios';

const CreateSchedulePage = () => {
  const [month, setMonth] = useState('');
  const [year, setYear] = useState('');
  const [days, setDays] = useState([]);
  const [doctors, setDoctors] = useState([]);

  useEffect(() => {
    if (month && year) {
      fetchDoctorsAndDays();
    }
  }, [month, year]);

  const fetchDoctorsAndDays = async () => {
    const monthIndex = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December',
    ].indexOf(month);

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
    const monthIndex = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December',
    ].indexOf(month);

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
    try {
      const token = localStorage.getItem('token');
      await Promise.all(doctors.map(async (doctor) => {
        await axios.put(`http://localhost:5000/api/doctors/${doctor.id}`, {
          days_off: doctor.days_off.join(',')
        }, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }));
      alert('Data updated successfully!');
    } catch (error) {
      console.error('Failed to update database:', error);
      alert('Failed to update data.');
    }
  };

  const generateSchedule = async () => {
    try {
      const token = localStorage.getItem('token');
      await axios.post('http://localhost:5000/api/schedules/generate', {
        month,
        year,
      }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      alert('Schedule generated successfully!');
    } catch (error) {
      console.error('Failed to generate schedule:', error);
      alert('Failed to generate schedule.');
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
      <FormControl fullWidth style={{ marginTop: '1rem' }}>
        <InputLabel>Year</InputLabel>
        <Select value={year} onChange={e => setYear(e.target.value)}>
          {[2024, 2025, 2026].map(y => (
            <MenuItem key={y} value={y}>{y}</MenuItem>
          ))}
        </Select>
      </FormControl>

      {days.length > 0 && (
        <TableContainer component={Paper} style={{ marginTop: '2rem', overflowX: 'auto' }}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell style={{ minWidth: '150px' }}>Doctor</TableCell>
                {days.map(day => <TableCell key={day} style={{ padding: '4px', minWidth: '30px' }}>{day}</TableCell>)}
              </TableRow>
            </TableHead>
            <TableBody>
              {doctors.map((doctor) => {
                return (
                  <TableRow key={doctor.id}>
                    <TableCell style={{ padding: '4px', minWidth: '150px' }}>{doctor.name}</TableCell>
                    {days.map(day => (
                      <TableCell
                        key={day}
                        style={{ padding: '4px', minWidth: '30px', cursor: 'pointer' }}
                        onClick={() => toggleDayOff(doctor.id, day)}
                      >
                        {doctor.days_off.includes(`${year}-${String([ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ].indexOf(month) + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`) ? 'X' : ''}
                      </TableCell>
                    ))}
                  </TableRow>
                );
              })}
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
