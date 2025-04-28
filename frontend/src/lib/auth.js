import { goto } from "$app/navigation";

const BASE_URL = import.meta.env.VITE_API_URL;

export async function register(username, password) {
    const url = BASE_URL + 'auth/register/'    
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password,
        })
    })

    return response
}


export function removeTokens() {
    console.log("Removing Tokens")
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
}

export async function refreshToken() {
    const refresh = localStorage.getItem('refresh');
    const response = await fetch(BASE_URL + 'token/refresh/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh })
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access', data.access);
        return true;
    } else {
        // Refresh token failed (maybe expired)
        removeTokens()
        return false;
    }
}

export async function getTokens(username, password) {
    const url = BASE_URL + 'token/'    
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username,
            password,
        })
    })
    
    const data = await response.json();

    if (response.ok) {
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
        console.log("Logged in successfully!");
        goto('/words')
    } else {
        console.error("Login failed:", data);
    }
}