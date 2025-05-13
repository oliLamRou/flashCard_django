import { appState, userState } from "$lib/state.svelte.js";

export function load({url}) {
    const preferences = userState.preferences
    const wordParam = url.searchParams.get('word');
    const word = JSON.parse(wordParam)
    if (word){
        return {
            word_id: word.id || null,
            word_languageA: word[preferences.languageA] || '',
            word_languageB: word[preferences.languageB] || '',
            word_class: word['word_class'],
            description: word['description']
        }
    }
}