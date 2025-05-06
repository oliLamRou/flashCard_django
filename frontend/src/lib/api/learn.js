import { api } from "$lib/api/api"

export async function load_word() {
    const response = await api('learn/guess/', {
        method: 'GET'
    })

    if (response.ok) {
        return await response.json()
    }
}

export async function update_word(word, score) {
    const data = {
        id: word.id,
        score: score
    }
    
    const response = await api('learn/score/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        },
    })

    return response
}