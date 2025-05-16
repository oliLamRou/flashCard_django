import { load_words } from "$lib/api/words";

export async function load() {
    return await load_words()
}