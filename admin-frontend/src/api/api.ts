import axios from "axios";

export interface TVTStatus {
    name: string;
    status: "active" | "inactive";
}


// TODO: temporary solution, will call real api in the future
const base = (import.meta.env.VITE_BASE_PATH ?? "");
function url(path: string) {
    return `${base}${path}`;
}

export async function getVTStatuses(): Promise<TVTStatus[]> {
    const response = await axios.get(url("/api/vtstatuses.json"));
    return response.data.message;
}