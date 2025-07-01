export interface CircuitSummary {
  circuit_id: number;
  name: string;
  country: string;
  fastest_lap_ms: number;
  total_races: number;
}

export interface DriverSummary {
  driver_id: number;
  forename: string;
  surname: string;
  podiums: number;
  total_races: number;
}