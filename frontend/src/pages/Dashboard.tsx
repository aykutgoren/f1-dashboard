import CircuitSummaryCard from '../components/CircuitSummaryCard';
import DriverSummaryCard from '../components/DriverSummaryCard';

export default function Dashboard() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6 bg-gray-100 min-h-screen">
      <CircuitSummaryCard />
      <DriverSummaryCard />
    </div>
  );
}