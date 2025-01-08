import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';

const ScheduleTable = ({ doctors, days, toggleDayOff, getShiftData, isReadOnly = false }) => {
  return (
    <TableContainer component={Paper} style={{ marginTop: '2rem', maxWidth: '100%' }}>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell style={{ minWidth: '100px' }}>Doctor</TableCell>
            {days.map(day => (
              <TableCell key={day} style={{ padding: '2px', minWidth: '20px' }}>
                {day}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {doctors.map((doctor) => (
            <TableRow key={doctor.id}>
              <TableCell style={{ padding: '2px', minWidth: '100px' }}>{doctor.name}</TableCell>
              {days.map(day => {
                const isDayOff = doctor.days_off.includes(
                  `${day}`
                );
                const shift = getShiftData ? getShiftData(doctor.id, day) : null;

                return (
                  <TableCell
                    key={day}
                    onClick={() =>
                      !isReadOnly && toggleDayOff && toggleDayOff(doctor.id, day)
                    }
                    style={{
                      padding: '2px',
                      cursor: isReadOnly ? 'default' : 'pointer',
                      backgroundColor: isDayOff ? 'red' : shift ? 'green' : 'white',
                    }}
                  >
                    {isDayOff ? 'X' : shift ? shift : ''}
                  </TableCell>
                );
              })}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default ScheduleTable;
