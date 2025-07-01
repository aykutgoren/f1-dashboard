import axios from 'axios';
import { CircuitSummary, DriverSummary } from '../types';

const BASE_URL = 'http://localhost:8000/api';

export const getCircuitSummary = async (): Promise<CircuitSummary[]> => {
  const res = await axios.get(`${BASE_URL}/circuits/summary`);
  return res.data;
};

export const getDriverSummary = async (): Promise<DriverSummary[]> => {
  const res = await axios.get(`${BASE_URL}/drivers/summary`);
  return res.data;
};