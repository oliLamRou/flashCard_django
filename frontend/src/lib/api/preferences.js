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

    if (response.status === 201) {
        const data = await load_preferences()
        userState['preferences'] = data.preferences
        return true
    }

    return false
}