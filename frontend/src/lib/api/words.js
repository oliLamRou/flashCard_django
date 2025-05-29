import { api } from "$lib/api/api"

export async function load_words(filters) {
    const param = new URLSearchParams(filters).toString()
    const response = await api('dictionary/?' + param, {
        method: 'GET',
    })

    if (response.ok) {
        return await response.json()
    }
}

export async function remove_word(id) {
    const response = await api('dictionary/delete/', {
        method: 'POST',
        body: JSON.stringify({'id': id}),
        headers: {
            'Content-Type': 'application/json'
        },
    })
    return response
}