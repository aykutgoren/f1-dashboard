import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import DriverSummaryCard from './DriverSummaryCard';
import * as api from '../services/api';
import '@testing-library/jest-dom';

const mockData = [
  {
    driver_id: '1',
    forename: 'Lewis',
    surname: 'Hamilton',
    podiums: 100,
    total_races: 280,
  },
];

jest.mock('../services/api');

describe('DriverSummaryCard', () => {
  beforeEach(() => {
    (api.getDriverSummary as jest.Mock).mockResolvedValue(mockData);
  });

  test('renders table headers and data', async () => {
    render(<DriverSummaryCard />);

    expect(screen.getByText(/Driver Summary/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText(/Lewis Hamilton/)).toBeInTheDocument();
    });

    // Control table headers with role and name
    expect(screen.getByRole('columnheader', { name: /Driver/i })).toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: /Podiums/i })).toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: /Total Races/i })).toBeInTheDocument();
  });
});
