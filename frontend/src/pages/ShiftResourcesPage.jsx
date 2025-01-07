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
  const [minShifts, setMinShifts] = useState([]);
  const [maxShifts, setMaxShifts] = useState([]);

  // Initialize data based on days of the month
  useEffect(() => {
    if (scheduleData) {
      const daysInMonth = new Date(scheduleData.year, scheduleData.month - 1 + 1, 0).getDate();
      setMinShifts(new Array(daysInMonth).fill(0));
      setMaxShifts(new Array(daysInMonth).fill(0));
    }
  }, [scheduleData]);

  // Handle changes in minimum shifts
  const handleMinChange = (index, value) => {
    const updatedMinShifts = [...minShifts];
    updatedMinShifts[index] = parseInt(value) || 0;
    setMinShifts(updatedMinShifts);
  };

  // Handle changes in maximum shifts
  const handleMaxChange = (index, value) => {
    const updatedMaxShifts = [...maxShifts];
    updatedMaxShifts[index] = parseInt(value) || 0;
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
    },
    input: {
      width: '50px',
      textAlign: 'center',
    },
  };

  return (
    <Container style={styles.container}>
      <Typography variant="h5" gutterBottom>
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
