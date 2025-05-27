import { APP_STATE, LEARN_STATE, USER_STATE } from "./constant";

//preferences, 
export const userState = $state(USER_STATE);

//word_classes, languages, selected word
export const appState = $state(APP_STATE);

//Current Flashcard
export const learnState = $state(LEARN_STATE);