import { userState } from "$lib/state.svelte"
import { api } from "$lib/api/api"

export async function create(word) {
    const preferences = userState.preferences
    const data = {
        [preferences.languageA]: word.word_languageA,
        [preferences.languageB]: word.word_languageB,
        word_class: word.word_class,
        description: word.description,
    }

    if (word.word_id) { data['id'] = word.word_id }

    const method = (word.word_id) ? 'PATCH' : 'POST'

    const response = await api('dictionary/new/', {
        method: method,
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        },
    })

    return response
}