import React from 'react';
import { render, screen } from '@testing-library/react';
import Dashboard from '../pages/Dashboard';
import '@testing-library/jest-dom';

/// If CircuitSummaryCard and DriverSummaryCard are imported externally
// and their renders are complex, it would be good to mock them:
jest.mock('../components/CircuitSummaryCard', () => () => <div data-testid="circuit-summary-card">CircuitSummaryCard</div>);
jest.mock('../components/DriverSummaryCard', () => () => <div data-testid="driver-summary-card">DriverSummaryCard</div>);

describe('Dashboard', () => {
  test('renders CircuitSummaryCard and DriverSummaryCard components', () => {
    render(<Dashboard />);

    expect(screen.getByTestId('circuit-summary-card')).toBeInTheDocument();
    expect(screen.getByTestId('driver-summary-card')).toBeInTheDocument();
  });
});
