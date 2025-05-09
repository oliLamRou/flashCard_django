import { api } from "$lib/api/api"
import { userState } from "$lib/state.svelte"
import { load_preferences } from "./global"

export async function save_prefererences(data) {
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