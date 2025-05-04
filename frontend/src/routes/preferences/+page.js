import { load_preferences } from "$lib/api/preferences"

export async function load() {
    return await load_preferences()
}