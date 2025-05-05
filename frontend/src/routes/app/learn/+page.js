import { load_word } from "$lib/api/learn"

export async function load() {
    return await load_word()
}