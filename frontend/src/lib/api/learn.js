import { api } from "$lib/api/api"

export async function load_word() {
    const response = await api('learn/guess/', {
        method: 'GET'
    })

    if (response.ok) {
        const data = await response.json()
        return data
    }
}

export async function update_word(word, score) {
    const data = {
        id: word.id,
        score: score,
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

export async function archive_word(word, archive=true) {
    const data = {
        id: word.id,
        archive: archive
    }

    const response = await api('learn/archive/', {
        method: 'POST', 
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    
    return response
}