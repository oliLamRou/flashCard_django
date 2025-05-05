import { load_preferences } from "$lib/api/global"
import { appState, userState } from "$lib/state.svelte";

export async function load() {
    return await load_preferences()
}