import { api } from "$lib/api/api"
import { learnState } from "$lib/state.svelte"

export async function load_word() {
    console.log("LOAD_WORD");
    
    const response = await api('learn/guess/', {
        method: 'GET'
    })

    learnState.currentWord.length = 0
    
    if (response.status === 200) {
        const data = await response.json()        
        learnState.currentWord.push(...data.words);
    }

    return response
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