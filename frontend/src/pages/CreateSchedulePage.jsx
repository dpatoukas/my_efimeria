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

  // State variables
  const [month, setMonth] = useState('');
  const [year, setYear] = useState('');
  const [doctorCount, setDoctorCount] = useState(1);
  const [days, setDays] = useState([]);
  const [tableVisible, setTableVisible] = useState(false);
  const [doctorNames, setDoctorNames] = useState([]); // Doctor names
  const [dayOff, setDayOff] = useState({}); // Tracks selected days off for each doctor

  // List of months
  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
  ];

  // List of years
  const years = Array.from({ length: 8 }, (_, i) => 2023 + i);

  // Handle confirmation
  const handleConfirm = () => {
    if (!month || !year || doctorCount < 1 || doctorCount > 10) {
      alert('Please fill all fields correctly!');
      return;
    }

    // Calculate number of days in the selected month and year
    const monthIndex = months.indexOf(month);
    const daysInMonth = new Date(year, monthIndex + 1, 0).getDate();
    setDays([...Array(daysInMonth).keys()].map(d => d + 1));

    // Initialize doctor names with placeholders
    const initialDoctorNames = [...Array(doctorCount)].map((_, i) => `Doctor ${String.fromCharCode(65 + i)}`);
    setDoctorNames(initialDoctorNames);

    // Initialize day-off tracking for each doctor
    const initialDaysOff = {};
    for (let i = 0; i < doctorCount; i++) {
      initialDaysOff[i] = [];
    }
    setDayOff(initialDaysOff);

    // Show the table
    setTableVisible(true);
  };

  // Toggle day off for a doctor
  const toggleDayOff = (doctorIndex, day) => {
    setDayOff((prev) => {
      const updatedDaysOff = { ...prev };
      if (updatedDaysOff[doctorIndex]?.includes(day)) {
        updatedDaysOff[doctorIndex] = updatedDaysOff[doctorIndex].filter((d) => d !== day);
      } else {
        updatedDaysOff[doctorIndex] = [...(updatedDaysOff[doctorIndex] || []), day];
      }
      return updatedDaysOff;
    });
  };

  // Handle doctor name changes
  const handleDoctorNameChange = (index, value) => {
    const newDoctorNames = [...doctorNames];
    newDoctorNames[index] = value.substring(0, 20); // Limit input to 20 characters
    setDoctorNames(newDoctorNames);
  };

  // Final confirm and navigate to the next page
  const handleFinalConfirm = () => {
    const scheduleData = {
      month,
      year,
      doctorCount,
      doctorNames,
      dayOff,
    };
    localStorage.setItem('scheduleData', JSON.stringify(scheduleData));
    navigate('/shift-resources');
  };

  // Styles
  const styles = {
    container: {
      padding: '2rem',
      backgroundColor: '#f9f9f9',
    },
    tableContainer: {
      marginTop: '2rem',
      maxWidth: '100%',
      overflowX: 'auto',
    },
    headerCell: {
      padding: '6px',
      fontSize: '12px',
      textAlign: 'center',
    },
    cell: {
      padding: '6px',
      fontSize: '12px',
      textAlign: 'center',
      cursor: 'pointer',
    },
    nameInput: {
      width: '120px',
      fontSize: '12px',
    },
    dayOffMark: {
      color: 'red',
      fontWeight: 'bold',
      fontSize: '12px',
    },
  };

  return (
    <Container style={styles.container}>
      <Typography variant="h5" gutterBottom>
        Create Schedule
      </Typography>

      <FormControl fullWidth>
        <InputLabel shrink>Month</InputLabel>
        <Select value={month} onChange={(e) => setMonth(e.target.value)}>
          {months.map((m, index) => (
            <MenuItem key={index} value={m}>{m}</MenuItem>
          ))}
        </Select>
      </FormControl>

      <FormControl fullWidth>
        <InputLabel shrink>Year</InputLabel>
        <Select value={year} onChange={(e) => setYear(e.target.value)}>
          {years.map((y) => (
            <MenuItem key={y} value={y}>{y}</MenuItem>
          ))}
        </Select>
      </FormControl>

      <FormControl fullWidth>
        <InputLabel shrink>Number of Doctors</InputLabel>
        <Select value={doctorCount} onChange={(e) => setDoctorCount(e.target.value)}>
          {[...Array(10).keys()].map((n) => (
            <MenuItem key={n + 1} value={n + 1}>{n + 1}</MenuItem>
          ))}
        </Select>
      </FormControl>

      <Button variant="contained" color="primary" onClick={handleConfirm}>
        Confirm
      </Button>

      {tableVisible && (
        <div style={styles.tableContainer}>
          <Typography variant="h6" gutterBottom>
            {`${month} ${year}`}
          </Typography>
          <TableContainer component={Paper}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell style={styles.headerCell}>Doctor Name</TableCell>
                  {days.map((day) => (
                    <TableCell key={day} style={styles.headerCell}>{day}</TableCell>
                  ))}
                  <TableCell style={styles.headerCell}>Days Off</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {doctorNames.map((name, index) => (
                  <TableRow key={`doctor-${index}`}>
                    <TableCell style={styles.cell}>
                      <TextField
                        value={name}
                        onChange={(e) => handleDoctorNameChange(index, e.target.value)}
                        style={styles.nameInput}
                      />
                    </TableCell>
                    {days.map((day) => (
                      <TableCell
                        key={day}
                        onClick={() => toggleDayOff(index, day)}
                        style={styles.cell}
                      >
                        {dayOff[index]?.includes(day) ? <span style={styles.dayOffMark}>X</span> : ''}
                      </TableCell>
                    ))}
                    <TableCell style={styles.cell}>{dayOff[index]?.length || 0}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
          <Button variant="contained" color="secondary" onClick={handleFinalConfirm} style={{ marginTop: '1rem' }}>
            Confirm Schedule
          </Button>
        </div>
      )}
    </Container>
  );
};

export default CreateSchedulePage;
