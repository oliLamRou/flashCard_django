const BASE_URL = import.meta.env.VITE_API_URL;

export async function api(endpoint, options = {}) {
    const authToken = localStorage.getItem('access')
    const url = BASE_URL + endpoint
    const authOptions = {
        ...options,
        headers: {
            ...options.headers,
            'Authorization': `Bearer ${authToken}`,
          }
    };

    let response = await fetch(url, authOptions);

    if (response.status === 401) {
        refreshed = await refreshToken();
        if (refreshed) {
            // Retry original request
            authToken = localStorage.getItem('access');
            authOptions.headers['Authorization'] = `Bearer ${authToken}`;
            response = await fetch(url, authOptions);
        } else {
            throw new Error("Session expired. Please log in again.");
        }        
    }

    return response;
}