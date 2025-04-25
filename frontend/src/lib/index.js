const BASE_URL = import.meta.env.VITE_API_URL;

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
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        return false;
    }
}

export async function api(endpoint, options = {}) {
    const url = BASE_URL + endpoint
    console.log("requesting: ", url)
    
    let access = localStorage.getItem('access');

    const authOptions = {
        ...options,
        headers: {
            ...options.headers,
            'Authorization': `Bearer ${access}`,
            // 'Content-Type': 'application/json',
        }
    };

    let response = await fetch(url, authOptions);

    // If access token is expired
    if (response.status === 401) {
        const refreshed = await refreshToken();
        if (refreshed) {
            // Retry original request
            access = localStorage.getItem('access');
            authOptions.headers['Authorization'] = `Bearer ${access}`;
            response = await fetch(url, authOptions);
        } else {
            throw new Error("Session expired. Please log in again.");
        }
    }

    return response;
}