import { load_word_classes, load_words } from "$lib/api/words";

export async function load() {
    const words_preferences = await load_words()
    const wordClasses = await load_word_classes()

    return {...words_preferences, ...wordClasses}
}