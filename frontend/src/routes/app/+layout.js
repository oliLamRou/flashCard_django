import { load_word_classes, load_preferences } from "$lib/api/global";
import { appState, userState } from "$lib/state.svelte";

export async function load() {
    const preferences = await load_preferences()
    const word_classes = await load_word_classes()
    
    userState['preferences'] = preferences.preferences
    
    appState['word_classes'] = word_classes.word_classes
    appState['languages'] = preferences.languages
    appState['modes'] = preferences.modes
}