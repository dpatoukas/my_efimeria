import React, { useEffect, useState } from 'react';
import { Container, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
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

  const getShiftForDoctorAndDay = (doctorId, day) => {
    // Generate date in 'YYYY-MM-DD' format
    const date = `${schedule.year}-${String(new Date(Date.parse(`${schedule.month} 1, ${schedule.year}`)).getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
  
    // Find matching shift
    const shift = shifts.find(s => s.doctor_id === doctorId && s.date === date);
  
    console.log(`Doctor: ${doctorId}, Day: ${day}, Date: ${date}, Shift: ${shift}`); // Debugging
    return shift ? '✔️' : ''; // Show checkmark for assigned shifts
  };

  const styles = {
    container: {
      width: '100vw',       // Full width of the viewport
      height: '100vh',      // Full height of the viewport
      overflow: 'auto',     // Add scrollbars if necessary
    },
    table: {
      width: '100%',        // Make table take full width
      borderCollapse: 'collapse', // Prevent gaps between cells
    },
    headerCell: {
      minWidth: '50px',     // Adjust cell width for better spacing
      textAlign: 'center',  // Center-align headers
    },
    bodyCell: {
      minWidth: '50px',     // Adjust cell width
      textAlign: 'center',  // Center-align content
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
          <TableContainer component={Paper}>
            <Table style={styles.table}>
              <TableHead>
                <TableRow>
                  <TableCell style={styles.headerCell}>Doctor</TableCell>
                  {days.map(day => (
                    <TableCell key={day} style={styles.headerCell}>{day}</TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {doctors.map(doctor => (
                  <TableRow key={doctor.id}>
                    <TableCell style={styles.bodyCell}>{doctor.name}</TableCell>
                    {days.map(day => (
                      <TableCell key={day} style={styles.bodyCell}>
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
