import React, { useState, useEffect } from 'react';
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
  TextField,
  Button,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

const ShiftResourcesPage = () => {
  const navigate = useNavigate();

  // Retrieve schedule data from local storage
  const scheduleData = JSON.parse(localStorage.getItem('scheduleData'));
  const maxDoctors = scheduleData.doctorCount || 1; // Max doctors from schedule
  const [minShifts, setMinShifts] = useState([]);
  const [maxShifts, setMaxShifts] = useState([]);

  // Initialize data based on days of the month
  useEffect(() => {
    if (scheduleData && minShifts.length === 0 && maxShifts.length === 0) {
      const monthIndex = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December',
      ].indexOf(scheduleData.month);

      if (monthIndex !== -1) {
        const daysInMonth = new Date(scheduleData.year, monthIndex + 1, 0).getDate();

        // Set default values based on constraints
        setMinShifts(new Array(daysInMonth).fill(1)); // Default Min = 1
        setMaxShifts(new Array(daysInMonth).fill(Math.min(2, maxDoctors))); // Default Max = 2 or maxDoctors
      }
    }
  }, [scheduleData]);

  // Handle changes in minimum shifts
  const handleMinChange = (index, value) => {
    const updatedMinShifts = [...minShifts];
    let min = parseInt(value) || 0;

    // Enforce constraints
    if (min < 1) min = 1;
    if (min > maxShifts[index]) min = maxShifts[index];

    updatedMinShifts[index] = min;
    setMinShifts(updatedMinShifts);
  };

  // Handle changes in maximum shifts
  const handleMaxChange = (index, value) => {
    const updatedMaxShifts = [...maxShifts];
    let max = parseInt(value) || 0;

    // Enforce constraints
    if (max < minShifts[index]) max = minShifts[index];
    if (max > maxDoctors) max = maxDoctors;

    updatedMaxShifts[index] = max;
    setMaxShifts(updatedMaxShifts);
  };

  // Save and navigate to the next page
  const handleSave = () => {
    const data = {
      ...scheduleData,
      minShifts,
      maxShifts,
    };
    localStorage.setItem('shiftResources', JSON.stringify(data));
    navigate('/summary'); // Update this route as needed
  };

  // Styles
  const styles = {
    container: {
      padding: '1rem',
      backgroundColor: '#f9f9f9',
    },
    tableContainer: {
      marginTop: '1rem',
      width: '100%',
      overflowX: 'auto',
    },
    headerCell: {
      padding: '2px',
      fontSize: '10px',
      textAlign: 'center',
    },
    cell: {
      padding: '2px',
      fontSize: '10px',
      textAlign: 'center',
    },
    input: {
      width: '35px',
      textAlign: 'center',
    },
  };

  return (
    <Container style={styles.container}>
      <Typography variant="h6" gutterBottom>
        Shift Resources for {scheduleData.month} {scheduleData.year}
      </Typography>
      <TableContainer component={Paper} style={styles.tableContainer}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell style={styles.headerCell}>Day</TableCell>
              {minShifts.map((_, index) => (
                <TableCell key={index + 1} style={styles.headerCell}>{index + 1}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell style={styles.cell}>Min Shifts</TableCell>
              {minShifts.map((value, index) => (
                <TableCell key={index} style={styles.cell}>
                  <TextField
                    value={value}
                    onChange={(e) => handleMinChange(index, e.target.value)}
                    style={styles.input}
                  />
                </TableCell>
              ))}
            </TableRow>
            <TableRow>
              <TableCell style={styles.cell}>Max Shifts</TableCell>
              {maxShifts.map((value, index) => (
                <TableCell key={index} style={styles.cell}>
                  <TextField
                    value={value}
                    onChange={(e) => handleMaxChange(index, e.target.value)}
                    style={styles.input}
                  />
                </TableCell>
              ))}
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
      <Button
        variant="contained"
        color="primary"
        onClick={handleSave}
        style={{ marginTop: '1rem' }}
      >
        Save and Continue
      </Button>
    </Container>
  );
};

export default ShiftResourcesPage;
