import { api } from "$lib/api/api"

export async function load_words() {
    const response = await api('dictionary/', {
        method: 'GET'
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