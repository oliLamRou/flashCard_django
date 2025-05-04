import { goto } from "$app/navigation";
import { userState } from "$lib/state.svelte";
import { _refresh } from "$lib/api/auth";
import { ACCESS_TOKEN_KEY, BASE_URL } from "$lib/constant";

export async function api(endpoint, options = {}) {
    const access_token = sessionStorage.getItem(ACCESS_TOKEN_KEY)
    const url = BASE_URL + endpoint
    const authOptions = {
        credentials: "include",
        ...options,
        headers: {
            ...options.headers,
            'Authorization': `Bearer ${ access_token }`,
          }
    };

    let response = await fetch(url, authOptions);

    if (response.status === 401) {
        response = await _refresh();
        if (response.status === 201) {
            access_token = sessionStorage.getItem(ACCESS_TOKEN_KEY)
            authOptions.headers['Authorization'] = `Bearer ${ access_token }`;
            response = await fetch(url, authOptions);
        } else {
            //destroy_user
            goto('/credentials')
            throw new Error("Session expired. Please log in again.");
        }
    }

    return response;
}