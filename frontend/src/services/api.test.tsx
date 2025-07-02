// __tests__/api.test.ts
import axios from 'axios';
import { getCircuitSummary, getDriverSummary } from '../services/api';
import { CircuitSummary, DriverSummary } from '../types';

// Mock axios module
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('API service functions', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  test('getCircuitSummary fetches and returns circuit summary data', async () => {
    // Arrange: mock axios.get to resolve with sample data
    const mockData: CircuitSummary[] = [
      { circuit_id: '1', name: 'Silverstone', location: 'UK' },
      { circuit_id: '2', name: 'Monaco', location: 'Monaco' },
    ];
    mockedAxios.get.mockResolvedValueOnce({ data: mockData });

    // Act
    const result = await getCircuitSummary();

    // Assert
    expect(mockedAxios.get).toHaveBeenCalledWith('http://localhost:8000/api/circuits/summary');
    expect(result).toEqual(mockData);
  });

  test('getDriverSummary fetches and returns driver summary data', async () => {
    // Arrange: mock axios.get to resolve with sample data
    const mockData: DriverSummary[] = [
      { driver_id: 'hamilton', forename: 'Lewis', surname: 'Hamilton', podiums: 100, total_races: 280 },
      { driver_id: 'verstappen', forename: 'Max', surname: 'Verstappen', podiums: 50, total_races: 120 },
    ];
    mockedAxios.get.mockResolvedValueOnce({ data: mockData });

    // Act
    const result = await getDriverSummary();

    // Assert
    expect(mockedAxios.get).toHaveBeenCalledWith('http://localhost:8000/api/drivers/summary');
    expect(result).toEqual(mockData);
  });
});
