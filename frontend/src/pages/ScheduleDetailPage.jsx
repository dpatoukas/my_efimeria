import React, { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Tooltip,
} from '@mui/material';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const ScheduleDetailPage = () => {
  const { id } = useParams(); // Get schedule ID from URL
  const [schedule, setSchedule] = useState({});
  const [shifts, setShifts] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [days, setDays] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch schedule details
  useEffect(() => {
    const fetchScheduleDetails = async () => {
      try {
        const token = localStorage.getItem('token');

        // Fetch schedule
        const scheduleResponse = await axios.get(`http://localhost:5000/api/schedules/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        const { month, year } = scheduleResponse.data;
        setSchedule(scheduleResponse.data);

        // Generate days of the month
        const date = new Date(year, new Date(Date.parse(`${month} 1, ${year}`)).getMonth() + 1, 0);
        setDays([...Array(date.getDate()).keys()].map(d => d + 1));

        // Fetch shifts
        const shiftsResponse = await axios.get(`http://localhost:5000/api/shifts?schedule_id=${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setShifts(shiftsResponse.data);

        // Fetch doctors
        const doctorsResponse = await axios.get('http://localhost:5000/api/doctors', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setDoctors(doctorsResponse.data);

      } catch (error) {
        console.error('Error fetching schedule details:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchScheduleDetails();
  }, [id]);

  // Function to check shift for a doctor and day
  const getShiftForDoctorAndDay = (doctorId, day) => {
    const date = `${schedule.year}-${String(new Date(Date.parse(`${schedule.month} 1, ${schedule.year}`)).getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    const shift = shifts.find(s => s.doctor_id === doctorId && s.date === date);
    return shift ? (
      <Tooltip title={`Shift ID: ${shift.id}`} arrow>
        <span style={{ color: 'green' }}>✔️</span>
      </Tooltip>
    ) : '';
  };

  // Print functionality
  const printSchedule = () => {
    window.print(); // Triggers the browser's print dialog
  };

  // Styles to fit the table and align properly
  const styles = {
    container: {
      maxWidth: 'md',
    },
    tableContainer: {
      marginTop: '2rem',
      overflowX: 'auto',
      maxWidth: '100%',
    },
    tableCell: {
      padding: '2px',
      minWidth: '30px',
      height: '30px',
      textAlign: 'center',
      fontSize: '0.8rem',
    },
    headerCell: {
      padding: '2px',
      minWidth: '30px',
      fontWeight: 'bold',
      textAlign: 'center',
    },
  };

  return (
    <Container style={styles.container}>
      {loading ? (
        <Typography>Loading...</Typography>
      ) : (
        <>
          <Typography variant="h2" gutterBottom>
            {schedule.month} {schedule.year}
          </Typography>
          <Button
            onClick={printSchedule}
            variant="contained"
            color="primary"
            style={{ marginBottom: '1rem' }}
          >
            Print Schedule
          </Button>
          <TableContainer component={Paper} style={styles.tableContainer}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell style={styles.headerCell}>Doctor</TableCell>
                  {days.map(day => (
                    <TableCell key={day} style={styles.headerCell}>
                      {day}
                    </TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {doctors.map(doctor => (
                  <TableRow key={doctor.id}>
                    <TableCell style={styles.tableCell}>{doctor.name}</TableCell>
                    {days.map(day => (
                      <TableCell key={day} style={styles.tableCell}>
                        {getShiftForDoctorAndDay(doctor.id, day)}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </>
      )}
    </Container>
  );
};

export default ScheduleDetailPage;
