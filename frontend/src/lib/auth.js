import { goto } from "$app/navigation";
import { userState } from "$lib/state.svelte";
import { ACCESS_TOKEN_KEY, BASE_URL } from "./constant";

function save_access_token(data) {
    sessionStorage.setItem(ACCESS_TOKEN_KEY, data.access)
}

export async function _register(username, password) {
    const url = BASE_URL + 'auth/register/'
    const credentials = {
        username: username,
        password: password,
    }

    const response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify(credentials),
        headers: { 'Content-Type': 'application/json' },
    })

    return response
}

export async function _login(username, password) {
    const url = BASE_URL + 'auth/login/'
    const credentials = {
        username,
        password,
    }
    const response = await fetch(url, {
        credentials: "include",
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
    })

    if (response.ok) {
        const data = await response.json();
        save_access_token(data)
        console.log("Logged in successfully!");
        return response
    } else {
        console.error("Login failed:");
        return response
    }
}

export async function _refresh() {
    console.log("_refresh");
    
    const url = BASE_URL + 'auth/refresh/'
    const response = await fetch(url, {
        credentials: "include",
        method: 'GET',
    })
    
    if (response.ok) {
        const data = await response.json();
        save_access_token(data)
        console.log("Refreshed, stay logged in");
        return response
    } else {
        console.error("Login failed:");
        return response
    }
}

export function _remove_user() {
    sessionStorage.removeItem(ACCESS_TOKEN_KEY)
    Object.assign(userState, {})
}