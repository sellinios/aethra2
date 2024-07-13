// src/utils/axiosError.ts
import { AxiosError } from 'axios';

export function isAxiosError(error: unknown): error is AxiosError {
    return (error as AxiosError).isAxiosError !== undefined;
}

export function getAxiosErrorMessage(error: AxiosError): string {
    if (error.response) {
        // The request was made and the server responded with a status code that falls out of the range of 2xx
        return (error.response.data as { error?: string }).error || error.response.statusText || 'Unknown error';
    } else if (error.request) {
        // The request was made but no response was received
        return 'No response received from server';
    } else {
        // Something happened in setting up the request that triggered an Error
        return error.message;
    }
}