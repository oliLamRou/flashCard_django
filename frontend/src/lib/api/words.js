import { api } from "./api"

export async function load_word_classes() {
    const response = await api('dictionary/word_classes/', {
        method: 'GET'
    })

    if (response.ok) {
        return await response.json()
        // Object.assign(word_classes, data.word_classes)
    }
}

export async function load_words() {
    const response = await api('dictionary/', {
        method: 'GET'
    })

    if (response.ok) {
        return await response.json()            
        // words = data.words
        // preferences = data.preference    
    }
}

const create = async() => {
    const data = {
        [preferences.languageA]: word_languageA,
        [preferences.languageB]: word_languageB,
        word_class: word_class,
        description: description,
    }

    if (word_id) { data['id'] = word_id }

    const method = (word_id) ? 'PATCH' : 'POST'

    const response = await api('dictionary/new/', {
        method: method,
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        },
    })

    //This is weak
    if (response.ok) {
        goto('/words')
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