import { render, screen, waitFor } from '@testing-library/react';
import CircuitSummaryCard from './CircuitSummaryCard';
import { getCircuitSummary } from '../services/api';
import { CircuitSummary } from '../types';
import '@testing-library/jest-dom';

jest.mock('../services/api');

const mockedData: CircuitSummary[] = [
  {
    circuit_id: 'monza',
    name: 'Monza',
    country: 'Italy',
    fastest_lap_ms: 74532,
    total_races: 30,
  },
  {
    circuit_id: 'silverstone',
    name: 'Silverstone',
    country: 'UK',
    fastest_lap_ms: 75500,
    total_races: 35,
  },
];

describe('CircuitSummaryCard', () => {
  beforeEach(() => {
    (getCircuitSummary as jest.Mock).mockResolvedValue(mockedData);
  });

  it('renders circuit summary header and table rows', async () => {
    render(<CircuitSummaryCard />);

    // Header appears
    expect(screen.getByText(/Circuit Summary/i)).toBeInTheDocument();

    // Wait for data to be rendered
    await waitFor(() => {
      expect(screen.getByText('Monza')).toBeInTheDocument();
      expect(screen.getByText('Silverstone')).toBeInTheDocument();
      expect(screen.getByText('🇮🇹 Italy')).toBeInTheDocument();
      expect(screen.getByText('🇬🇧 UK')).toBeInTheDocument();
    });
  });
});
