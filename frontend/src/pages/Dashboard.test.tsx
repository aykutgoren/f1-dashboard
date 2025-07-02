import React from 'react';
import { render, screen } from '@testing-library/react';
import Dashboard from '../pages/Dashboard';
import '@testing-library/jest-dom';

// Eğer CircuitSummaryCard ve DriverSummaryCard dışarıdan import ediliyorsa
// ve onların render’ları karmaşıksa, onları mock'lamak iyi olur:
jest.mock('../components/CircuitSummaryCard', () => () => <div data-testid="circuit-summary-card">CircuitSummaryCard</div>);
jest.mock('../components/DriverSummaryCard', () => () => <div data-testid="driver-summary-card">DriverSummaryCard</div>);

describe('Dashboard', () => {
  test('renders CircuitSummaryCard and DriverSummaryCard components', () => {
    render(<Dashboard />);

    expect(screen.getByTestId('circuit-summary-card')).toBeInTheDocument();
    expect(screen.getByTestId('driver-summary-card')).toBeInTheDocument();
  });
});
