// import { WORD_CLASSES } from "$lib/state.svelte"
// import { api } from "./api"

// export async function word_classes() {
//     if (Object.keys(WORD_CLASSES) < 1) {
//         const response = await api('dictionary/word_classes/', {
//             method: 'GET'
//         })
    
//         if (response.ok) {
//             const data = await response.json()
//             WORD_CLASSES.set(data)
//         }
//     }
//     console.log(WORD_CLASSES);
//     return WORD_CLASSES
// };