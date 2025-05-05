import { api } from "$lib/api/api"
import { userState } from "$lib/state.svelte"
import { load_preferences } from "./global"

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

    if (response.ok) {
        const data = await load_preferences()
        userState['preferences'] = data.preferences
    }

    return response
}