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

// {
//     "id": 28,
//     "user_score": {
//         "fail": 3,
//         "success": 9,
//         "last_try": "2025-05-05"
//     },
//     "FR": "bibliothèque",
//     "KR": "두서관",
//     "EN": "",
//     "description": "",
//     "word_class": "n",
//     "create_at": "2025-04-24",
//     "user": 1
// }