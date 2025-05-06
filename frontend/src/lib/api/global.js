//user list ?

import { api } from "$lib/api/api"

export async function load_word_classes() {
    const response = await api('dictionary/word_classes/', {
        method: 'GET'
    })

    if (response.ok) {
        return await response.json()
    }
}

export async function load_preferences() {
    const response = await api('auth/preference/', {})

    if (response.ok) {
        return await response.json()
    }
}

export async function load_user_info() {
    const response = await api('auth/info/', {
        method: 'GET'
    })

    if (response.ok) {
        return await response.json()
    }
}