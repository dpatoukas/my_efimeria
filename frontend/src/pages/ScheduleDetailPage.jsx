import React, { useEffect, useState } from 'react';
import { Container, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Tooltip } from '@mui/material';
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
    const date = `${schedule.year}-${String(new Date(Date.parse(`${schedule.month} 1, ${schedule.year}`)).getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    const shift = shifts.find(s => s.doctor_id === doctorId && s.date === date);
    return shift ? (
      <Tooltip title={`Shift ID: ${shift.id}`} arrow>
        <span>✔️</span>
      </Tooltip>
    ) : '';
  };

  const exportToCSV = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`http://localhost:5000/api/schedules/export/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
        responseType: 'blob',
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `schedule_${id}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error exporting schedule:', error);
    }
  };

  const styles = {
    container: {
      width: '100vw',
      height: '100vh',
      overflow: 'auto',
    },
    tableContainer: {
      maxWidth: '100%',
      overflowX: 'auto',
    },
    table: {
      width: 'auto',
      borderCollapse: 'collapse',
    },
    headerCell: {
      minWidth: '40px',
      textAlign: 'center',
    },
    bodyCell: {
      minWidth: '40px',
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
          <Button onClick={exportToCSV} variant="contained" color="primary" style={{ marginBottom: '1rem' }}>
            Export to CSV
          </Button>
          <TableContainer component={Paper} style={styles.tableContainer}>
            <Table style={styles.table} size="small">
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
