import { goto } from "$app/navigation";
import { userState } from "$lib/state.svelte";

const BASE_URL = import.meta.env.VITE_API_URL;

export async function api(endpoint, options = {}) {
    const url = BASE_URL + endpoint
    const authOptions = {
        ...options,
        headers: {
            ...options.headers,
            'Authorization': `Bearer ${ userState.accessToken }`,
          }
    };

    let response = await fetch(url, authOptions);

    if (response.status === 401) {
        refreshed = await refreshToken();
        if (refreshed) {
            authOptions.headers['Authorization'] = `Bearer ${ userState.accessToken }`;
            response = await fetch(url, authOptions);
        } else {
            goto('/credentials')
            throw new Error("Session expired. Please log in again.");
        }
    }

    return response;
}