import axios from 'axios';

// define it here for now
const baseUrl = "http://localhost:5000";

export const runExecutable = async (executablePath: string) => {
    return await axios.post(`${baseUrl}/run`, { path: executablePath });
}
