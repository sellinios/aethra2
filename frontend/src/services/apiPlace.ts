import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL;

export interface NearestPlace {
  id: number;
  name: string;
  longitude: number;
  latitude: number;
  elevation: number;
  category: {
    id: number;
    name: string;
  };
  admin_division: {
    id: number;
    name: string;
    slug: string;
    parent: number | null;
  };
  url: string;
  weather_url: string;
}

export const fetchNearestPlace = async (latitude: number, longitude: number): Promise<NearestPlace> => {
  try {
    const response = await axios.get<NearestPlace>(`${BASE_URL}/places/nearest/`, {
      params: { latitude, longitude }
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('Error fetching nearest place:', error.response ? error.response.data : error.message);
    } else {
      console.error('Unknown error:', error);
    }
    throw error;
  }
};