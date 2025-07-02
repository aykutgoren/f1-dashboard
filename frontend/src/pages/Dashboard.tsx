import CircuitSummaryCard from '../components/CircuitSummaryCard';
import DriverSummaryCard from '../components/DriverSummaryCard';

export default function Dashboard() {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: '24px',
      padding: '24px',
      background: '#f4f6f8',
      minHeight: '100vh',
      maxWidth: '1200px',
      margin: '0 auto',
    }}>
      <CircuitSummaryCard />
      <DriverSummaryCard />
    </div>
  );
}
