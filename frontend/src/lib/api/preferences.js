import { api } from "$lib/api/api"

export async function load_preferences() {
    const response = await api('auth/preference/', {})

    if (response.ok) {
        return await response.json()
    }
}

export async function save_prefererences(languageA, languageB, learnMode) {
    const data = {
        languageA: languageA,
        languageB: languageB,
        learnMode: learnMode,
    }

    const response = await api('auth/preference/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        },
    })

    return response
}