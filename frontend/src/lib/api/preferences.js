import { api } from "$lib/api/api"

export async function load_preferences() {
    const response = await api('auth/preference/', {})

    if (response.ok) {
        return await response.json()
        // Object.assign(preferences, data)

        // languageA = data.preferences.languageA
        // languageB = data.preferences.languageB
        // learnMode = data.preferences.learnMode
    }
}

// const save = async() => {
//     const data = {
//         languageA: languageA,
//         languageB: languageB,
//         learnMode: learnMode,
//     }

//     const response = await api('auth/preference/', {
//         method: 'POST',
//         body: JSON.stringify(data),
//         headers: {
//             'Content-Type': 'application/json'
//         },
//     })
//     goto('/words')
// }