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

export async function startElection() {
    const response = await axios.post(url("/../voting-process-manager-api/start"))
        .then( function (response){
            let message = '';
            if(response.status == 200) {
                message += 'Úspešne spustené terminály. (' + response.data.success_terminals_count + ')\n';
                message += 'Neúspešne spustené terminály. (' + response.data.error_terminals_count + ')';
                alert(message);
            } else {
                alert(response.status)
            }
        })
        .catch(function (error) {
            alert(error)
        });
}


export async function stopElection() {
    const response = await axios.post(url("/../voting-process-manager-api/end"))
        .then( function (response){
            let message = '';
            if(response.status == 200) {
                message += 'Úspešne zastavené terminály. (' + response.data.success_terminals_count + ')\n';
                message += 'Neúspešne zastavené terminály. (' + response.data.error_terminals_count + ')';
                alert(message);
            } else {
                alert(response.status)
            }
        })
        .catch(function (error) {
            alert(error)
        });
}
