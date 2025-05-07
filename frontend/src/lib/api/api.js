import { goto } from "$app/navigation";
import { userState } from "$lib/state.svelte";
import { _refresh } from "$lib/api/auth";
import { ACCESS_TOKEN_KEY, BASE_URL, REFRESH_TOKEN_KEY } from "$lib/constant";

export async function api(endpoint, options = {}) {
    if (typeof window === 'undefined') {
        console.log("NO WINDOW");
        return {}
    }
    
    const url = BASE_URL + endpoint
    let authOptions = {
        ...options,
        headers: {
            ...options.headers,
            'Authorization': `Bearer ${ sessionStorage.getItem(ACCESS_TOKEN_KEY) }`,
            }
    };

    let response = await fetch(url, authOptions);

    if (response.status === 401) {
        response = await _refresh();
        if (response.status === 200) {
            authOptions.headers['Authorization'] = `Bearer ${ sessionStorage.getItem(ACCESS_TOKEN_KEY) }`;
            response = await fetch(url, authOptions);
        } else {
            //destroy_user
            goto('/auth/credentials')
            throw new Error("Session expired. Please log in again.");
        }
    }

    return response;
}