import { useEffect, useState } from 'react';
import { getDriverSummary } from '../services/api';
import { DriverSummary } from '../types';

export default function DriverSummaryCard() {
  const [data, setData] = useState<DriverSummary[]>([]);
  const [search, setSearch] = useState('');

  useEffect(() => {
    getDriverSummary().then(setData);
  }, []);

  const filtered = data.filter(driver =>
    `${driver.forename} ${driver.surname}`.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-6 shadow-xl rounded-2xl border bg-white">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Driver Summary</h2>
      <input
        type="text"
        placeholder="Search by driver name"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="mb-4 p-2 w-full border rounded-md focus:outline-none focus:ring focus:border-blue-300"
      />
      <div className="overflow-x-auto">
        <table className="table-auto w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-100 text-gray-600 uppercase text-sm leading-normal">
              <th className="py-2 px-4">Name</th>
              <th className="py-2 px-4">Podiums</th>
              <th className="py-2 px-4">Total Races</th>
            </tr>
          </thead>
          <tbody className="text-gray-700">
            {filtered.map((driver) => (
              <tr key={driver.driver_id} className="border-b hover:bg-gray-50">
                <td className="py-2 px-4 font-medium">
                  {driver.forename} {driver.surname}
                </td>
                <td className="py-2 px-4">{driver.podiums}</td>
                <td className="py-2 px-4">{driver.total_races}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
