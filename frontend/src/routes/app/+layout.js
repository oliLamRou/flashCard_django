import { load_word_classes, load_preferences, load_user_info } from "$lib/api/global";
import { appState, userState } from "$lib/state.svelte";

export async function load() {
    const preferences = await load_preferences()
    const word_classes = await load_word_classes()
    const user_info = await load_user_info()
    
    userState['preferences'] = preferences.preferences
    userState['user_info'] = user_info

    appState['word_classes'] = word_classes.word_classes
    appState['languages'] = preferences.languages
    appState['modes'] = preferences.modes
}