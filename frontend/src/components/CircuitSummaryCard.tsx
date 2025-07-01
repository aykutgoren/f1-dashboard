import { useEffect, useState } from 'react';
import { getCircuitSummary } from '../services/api';
import { CircuitSummary } from '../types';

export default function CircuitSummaryCard() {
  const [data, setData] = useState<CircuitSummary[]>([]);
  const [search, setSearch] = useState('');

  useEffect(() => {
    getCircuitSummary().then(setData);
  }, []);

  const filtered = data.filter(c =>
    c.name.toLowerCase().includes(search.toLowerCase()) ||
    c.country.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-6 shadow-xl rounded-2xl border bg-white">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Circuit Summary</h2>
      <input
        type="text"
        placeholder="Search by name or country"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="mb-4 p-2 w-full border rounded-md focus:outline-none focus:ring focus:border-blue-300"
      />
      <div className="overflow-x-auto">
        <table className="table-auto w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-100 text-gray-600 uppercase text-sm leading-normal">
              <th className="py-2 px-4">Name</th>
              <th className="py-2 px-4">Country</th>
              <th className="py-2 px-4">Fastest Lap (ms)</th>
              <th className="py-2 px-4">Total Races</th>
            </tr>
          </thead>
          <tbody className="text-gray-700">
            {filtered.map((item) => (
              <tr key={item.circuitId} className="border-b hover:bg-gray-50">
                <td className="py-2 px-4 font-medium">{item.name}</td>
                <td className="py-2 px-4">{item.country}</td>
                <td className="py-2 px-4">{item.fastest_lap_ms}</td>
                <td className="py-2 px-4">{item.total_races}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
