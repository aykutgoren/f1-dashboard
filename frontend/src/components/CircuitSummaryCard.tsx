import { useEffect, useState } from 'react';
import { getCircuitSummary } from '../services/api';
import { CircuitSummary } from '../types';
import styles from './SummaryCard.module.css';

const countryFlags: Record<string, string> = {
    Afghanistan: '🇦🇫',
    Albania: '🇦🇱',
    Algeria: '🇩🇿',
    Andorra: '🇦🇩',
    Angola: '🇦🇴',
    AntiguaandBarbuda: '🇦🇬',
    Argentina: '🇦🇷',
    Armenia: '🇦🇲',
    Australia: '🇦🇺',
    Austria: '🇦🇹',
    Azerbaijan: '🇦🇿',
    Bahamas: '🇧🇸',
    Bahrain: '🇧🇭',
    Bangladesh: '🇧🇩',
    Barbados: '🇧🇧',
    Belarus: '🇧🇾',
    Belgium: '🇧🇪',
    Belize: '🇧🇿',
    Benin: '🇧🇯',
    Bhutan: '🇧🇹',
    Bolivia: '🇧🇴',
    BosniaandHerzegovina: '🇧🇦',
    Botswana: '🇧🇼',
    Brazil: '🇧🇷',
    Brunei: '🇧🇳',
    Bulgaria: '🇧🇬',
    BurkinaFaso: '🇧🇫',
    Burundi: '🇧🇮',
    CaboVerde: '🇨🇻',
    Cambodia: '🇰🇭',
    Cameroon: '🇨🇲',
    Canada: '🇨🇦',
    CentralAfricanRepublic: '🇨🇫',
    Chad: '🇹🇩',
    Chile: '🇨🇱',
    China: '🇨🇳',
    Colombia: '🇨🇴',
    Comoros: '🇰🇲',
    CostaRica: '🇨🇷',
    Croatia: '🇭🇷',
    Cuba: '🇨🇺',
    Cyprus: '🇨🇾',
    CzechRepublic: '🇨🇿',
    DRCongo: '🇨🇩',
    Denmark: '🇩🇰',
    Djibouti: '🇩🇯',
    Dominica: '🇩🇲',
    DominicanRepublic: '🇩🇴',
    EastTimor: '🇹🇱',
    Ecuador: '🇪🇨',
    Egypt: '🇪🇬',
    ElSalvador: '🇸🇻',
    EquatorialGuinea: '🇬🇶',
    Eritrea: '🇪🇷',
    Estonia: '🇪🇪',
    Eswatini: '🇸🇿',
    Ethiopia: '🇪🇹',
    Fiji: '🇫🇯',
    Finland: '🇫🇮',
    France: '🇫🇷',
    Gabon: '🇬🇦',
    Gambia: '🇬🇲',
    Georgia: '🇬🇪',
    Germany: '🇩🇪',
    Ghana: '🇬🇭',
    Greece: '🇬🇷',
    Grenada: '🇬🇩',
    Guatemala: '🇬🇹',
    Guinea: '🇬🇳',
    GuineaBissau: '🇬🇼',
    Guyana: '🇬🇾',
    Haiti: '🇭🇹',
    Honduras: '🇭🇳',
    Hungary: '🇭🇺',
    Iceland: '🇮🇸',
    India: '🇮🇳',
    Indonesia: '🇮🇩',
    Iran: '🇮🇷',
    Iraq: '🇮🇶',
    Ireland: '🇮🇪',
    Israel: '🇮🇱',
    Italy: '🇮🇹',
    Jamaica: '🇯🇲',
    Japan: '🇯🇵',
    Jordan: '🇯🇴',
    Kazakhstan: '🇰🇿',
    Kenya: '🇰🇪',
    Kiribati: '🇰🇮',
    KoreaNorth: '🇰🇵',
    Korea: '🇰🇷',
    Kuwait: '🇰🇼',
    Kyrgyzstan: '🇰🇬',
    Laos: '🇱🇦',
    Latvia: '🇱🇻',
    Lebanon: '🇱🇧',
    Lesotho: '🇱🇸',
    Liberia: '🇱🇸',
    Libya: '🇱🇾',
    Liechtenstein: '🇱🇮',
    Lithuania: '🇱🇹',
    Luxembourg: '🇱🇺',
    Madagascar: '🇲🇬',
    Malawi: '🇲🇼',
    Malaysia: '🇲🇾',
    Maldives: '🇲🇻',
    Mali: '🇲🇱',
    Malta: '🇲🇹',
    MarshallIslands: '🇲🇭',
    Mauritania: '🇲🇷',
    Mauritius: '🇲🇺',
    Mexico: '🇲🇽',
    Micronesia: '🇫🇲',
    Moldova: '🇲🇩',
    Monaco: '🇲🇨',
    Mongolia: '🇲🇳',
    Montenegro: '🇲🇪',
    Morocco: '🇲🇦',
    Mozambique: '🇲🇿',
    Myanmar: '🇲🇲',
    Namibia: '🇳🇦',
    Nauru: '🇳🇷',
    Nepal: '🇳🇵',
    Netherlands: '🇳🇱',
    NewZealand: '🇳🇿',
    Nicaragua: '🇳🇮',
    Niger: '🇳🇪',
    Nigeria: '🇳🇬',
    NorthMacedonia: '🇲🇰',
    Norway: '🇳🇴',
    Oman: '🇴🇲',
    Pakistan: '🇵🇰',
    Palau: '🇵🇼',
    Panama: '🇵🇦',
    PapuaNewGuinea: '🇵🇬',
    Paraguay: '🇵🇾',
    Peru: '🇵🇪',
    Philippines: '🇵🇭',
    Poland: '🇵🇱',
    Portugal: '🇵🇹',
    Qatar: '🇶🇦',
    Romania: '🇷🇴',
    Russia: '🇷🇺',
    Rwanda: '🇷🇼',
    SaintKittsandNevis: '🇰🇳',
    SaintLucia: '🇱🇨',
    SainVincentandtheGrenadines: '🇻🇨',
    Samoa: '🇼🇸',
    SanMarino: '🇸🇲',
    SaoTomeandPrincipe: '🇸🇹',
    "Saudi Arabia": '🇸🇦',
    Senegal: '🇸🇳',
    Serbia: '🇷🇸',
    Seychelles: '🇸🇨',
    SierraLeone: '🇸🇱',
    Singapore: '🇸🇬',
    Slovakia: '🇸🇰',
    Slovenia: '🇸🇮',
    SolomonIslands: '🇸🇧',
    Somalia: '🇸🇴',
    SouthAfrica: '🇿🇦',
    SouthSudan: '🇸🇸',
    Spain: '🇪🇸',
    SriLanka: '🇱🇰',
    Sudan: '🇸🇩',
    Suriname: '🇸🇷',
    Sweden: '🇸🇪',
    Switzerland: '🇨🇭',
    Syria: '🇸🇾',
    Taiwan: '🇹🇼',
    Tajikistan: '🇹🇯',
    Tanzania: '🇹🇿',
    Thailand: '🇹🇭',
    Togo: '🇹🇬',
    Tonga: '🇹🇴',
    TrinidadanTobago: '🇹🇹',
    Tunisia: '🇹🇳',
    Turkey: '🇹🇷',
    Turkmenistan: '🇹🇲',
    Tuvalu: '🇹🇻',
    Uganda: '🇺🇬',
    Ukraine: '🇺🇦',
    UAE: '🇦🇪',
    UK: '🇬🇧',
    "United States": '🇺🇸',
    USA: '🇺🇸',
    Uruguay: '🇺🇾',
    Uzbekistan: '🇺🇿',
    Vanuatu: '🇻🇺',
    VaticanCity: '🇻🇦',
    Venezuela: '🇻🇪',
    Vietnam: '🇻🇳',
    Yemen: '🇾🇪',
    Zambia: '🇿🇲',
    Zimbabwe: '🇿🇼',
    };

type SortKey = keyof CircuitSummary;

export default function CircuitSummaryCard() {
  const [data, setData] = useState<CircuitSummary[]>([]);
  const [search, setSearch] = useState('');
  const [sortKey, setSortKey] = useState<SortKey>('total_races');
  const [sortAsc, setSortAsc] = useState(false);

  useEffect(() => {
    getCircuitSummary().then(setData);
  }, []);

  const filtered = data.filter(c =>
    c.name.toLowerCase().includes(search.toLowerCase()) ||
    c.country.toLowerCase().includes(search.toLowerCase())
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
      <h2 className={styles.title}> Circuit Summary 🏁</h2>
      <div className={styles.searchContainer}>
        <input
          type="text"
          placeholder="Search by name or country"
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
                <th className={`${styles.sortable}`} onClick={() => handleSort('name')}>
                  <span className={styles.iconHeader}>
                    Circuit
                    {sortKey === 'name' && <span className={styles.sortArrow}>{sortAsc ? '↑' : '↓'}</span>}
                  </span>
                </th>
                <th className={styles.sortable} onClick={() => handleSort('country')}>
                  Country
                  {sortKey === 'country' && <span className={styles.sortArrow}>{sortAsc ? '↑' : '↓'}</span>}
                </th>
                <th className={styles.sortable} onClick={() => handleSort('fastest_lap_ms')}>
                  Fastest Lap (ms)
                  {sortKey === 'fastest_lap_ms' && <span className={styles.sortArrow}>{sortAsc ? '↑' : '↓'}</span>}
                </th>
                <th className={styles.sortable} onClick={() => handleSort('total_races')}>
                  Total Races
                  {sortKey === 'total_races' && <span className={styles.sortArrow}>{sortAsc ? '↑' : '↓'}</span>}
                </th>
              </tr>
            </thead>
            <tbody>
              {sorted.map((item) => (
                <tr key={item.circuit_id}>
                  <td>{item.name}</td>
                  <td>{countryFlags[item.country] || '🏁'} {item.country}</td>
                  <td>{item.fastest_lap_ms}</td>
                  <td>{item.total_races}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
