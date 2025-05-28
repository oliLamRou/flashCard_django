import { api } from "$lib/api/api"

export async function load_words(page=0, all=false) {
    const param = new URLSearchParams({
        page: page,
        all: all,
    }).toString()
    
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