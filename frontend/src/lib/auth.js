import { goto } from "$app/navigation";
import { userState } from "$lib/state.svelte";

const BASE_URL = import.meta.env.VITE_API_URL;

export async function register(username, password) {
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

export function resetUserState() {
    userState.username = null
    userState.accessToken = null
    userState.refreshToken = null    
}

export function removeTokens() {
    console.log("Removing Tokens")
    userState.accessToken = null
    userState.refreshToken = null
}

export async function refreshToken() {
    const refresh = userState.refreshToken
    const response = await fetch(BASE_URL + 'token/refresh/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refreshToken })
    });

    if (response.ok) {
        const data = await response.json();
        userState.accessToken = data.access
        userState.refreshToken = data.refresh
        return true;
    } else {
        removeTokens()
        return false;
    }
}

export async function getTokens(username, password) {
    const url = BASE_URL + 'token/'
    const credentials = {
        username,
        password,
    }
    const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
    })
    
    const data = await response.json();

    if (response.ok) {
        userState.accessToken = data.access
        userState.refreshToken = data.refresh
        console.log("Logged in successfully!");
        return response
    } else {
        console.error("Login failed:", data);
        return response
    }
}