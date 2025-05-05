import { load_words } from "$lib/api/words";

export async function load() {
    const words_preferences = await load_words()
    return {
        words: words_preferences.words,
    }
}