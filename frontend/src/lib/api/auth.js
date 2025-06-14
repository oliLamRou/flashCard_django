import { appState, learnState, userState } from "$lib/state.svelte";
import { ACCESS_TOKEN_KEY, APP_STATE, BASE_URL, LEARN_STATE, REFRESH_TOKEN_KEY, USER_STATE } from "$lib/constant";

async function save_access_token(data) {
    sessionStorage.setItem(ACCESS_TOKEN_KEY, data.access)
    localStorage.setItem(REFRESH_TOKEN_KEY, data.refresh)
}

export function _remove_user() {
    console.info("Clearing Session, Local, State Data")
    sessionStorage.removeItem(ACCESS_TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
    Object.assign(userState, USER_STATE)
    Object.assign(appState, APP_STATE)
    Object.assign(learnState, LEARN_STATE)
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
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
    })

    if (response.status === 200) {
        const data = await response.json();
        save_access_token(data)
        console.info("Logged in successfully!");
        return true
    } else {
        console.error("Login failed:");
        return false
    }
}

export async function _refresh() {
    console.log("FRONTEND -> _REFRESH");
    
    const url = BASE_URL + 'auth/refresh/'
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'refresh': localStorage.getItem(REFRESH_TOKEN_KEY)})
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