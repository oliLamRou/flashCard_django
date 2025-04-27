import { goto } from "$app/navigation";

const BASE_URL = import.meta.env.VITE_API_URL;

async function getCSRF() {
    await fetch(BASE_URL + 'auth/csrf/', {
        method: 'GET',
        credentials: 'include'
    });
}

// Small helper to get the csrftoken from cookies
function getCookie(name) {
    let value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

export async function login(username, password) {
    await getCSRF(); // make sure CSRF is set

    const response = await api('auth/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })        
    })

    if (response.ok) {
        console.log('Logged in!');
    } else {
        const data = await response.json();
        throw new Error(data.detail || 'Login failed');
    }
    
    return await response.json();
}

export async function api(endpoint, options = {}) {
    const url = BASE_URL + endpoint
    console.log("requesting: ", url)

    const authOptions = {
        credentials: 'include',
        ...options,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            ...options.headers,
        }
    };

    let response = await fetch(url, authOptions);

    return response;
}