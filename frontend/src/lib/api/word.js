
const create = async() => {
    const data = {
        [languageA]: word_languageA,
        [languageB]: word_languageB,
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
        goto('app/words')
    }
}