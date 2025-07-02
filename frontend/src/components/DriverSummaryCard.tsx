import { useEffect, useState } from 'react';
import { getDriverSummary } from '../services/api';
import { DriverSummary } from '../types';
import styles from './SummaryCard.module.css';

type SortKey = keyof DriverSummary;

export default function DriverSummaryCard() {
  const [data, setData] = useState<DriverSummary[]>([]);
  const [search, setSearch] = useState('');
  const [sortKey, setSortKey] = useState<SortKey>('podiums');
  const [sortAsc, setSortAsc] = useState(false);

  useEffect(() => {
    getDriverSummary().then(setData);
  }, []);

  const filtered = data.filter(driver =>
    `${driver.forename} ${driver.surname}`.toLowerCase().includes(search.toLowerCase())
  );

  const sorted = [...filtered].sort((a, b) => {
    const valA = a[sortKey];
    const valB = b[sortKey];
    return sortAsc
      ? valA > valB ? 1 : -1
      : valA < valB ? 1 : -1;
  });

  const handleSort = (key: SortKey) => {
    if (key === sortKey) {
      setSortAsc(!sortAsc);
    } else {
      setSortKey(key);
      setSortAsc(true);
    }
  };

  return (
    <div className={styles.card}>
      <h2 className={styles.title}>️ Driver Summary 🏆</h2>
      <div className={styles.searchContainer}>
        <input
          type="text"
          placeholder="Search by driver name"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className={styles.searchInput}
        />
      </div>
      <div className={styles.tableWrapper}>
        {sorted.length === 0 ? (
          <div className={styles.emptyMessage}>No results found.</div>
        ) : (
          <table className={styles.table}>
            <thead>
              <tr>
                <th className={styles.sortable} onClick={() => handleSort('surname')}>
                  Driver
                  {sortKey === 'surname' && <span className={styles.sortArrow}>{sortAsc ? '↑' : '↓'}</span>}
                </th>
                <th className={styles.sortable} onClick={() => handleSort('podiums')}>
                  Podiums
                  {sortKey === 'podiums' && <span className={styles.sortArrow}>{sortAsc ? '↑' : '↓'}</span>}
                </th>
                <th className={styles.sortable} onClick={() => handleSort('total_races')}>
                  Total Races
                  {sortKey === 'total_races' && <span className={styles.sortArrow}>{sortAsc ? '↑' : '↓'}</span>}
                </th>
              </tr>
            </thead>
            <tbody>
              {sorted.map((driver) => (
                <tr key={driver.driver_id}>
                  <td> {driver.forename} {driver.surname}</td>
                  <td>{driver.podiums}</td>
                  <td>{driver.total_races}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
