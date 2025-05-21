<script>
	import { load_word, update_word } from "$lib/api/learn.js";
	import { appState, learnState, userState } from "$lib/state.svelte.js";

    //App State
    const word_classes = appState.word_classes

    //User State
    let languageA = $state(userState.preferences.languageA)
    let languageB = $state(userState.preferences.languageB)
    let learnMode = $state(userState.preferences.learnMode)

    let lang_from = $state(learnMode === 'NORMAL' ? languageA : languageB)
    let lang_to = $state(learnMode === 'NORMAL' ? languageB : languageA)
    
    //Current Word
    let word = $derived(learnState.currentWord ? learnState.currentWord[0] : null)
    let last_try = $derived(word?.user_score?.last_try || 'Never Seen')

    let score_count = $derived.by(() => {
        const fail = word?.user_score?.fail
        const success = word?.user_score?.success        
        if (fail === null || fail === undefined || success === null || success === undefined ){
            return 0
        }
        return success - fail
    })

    //Functions
    const answer = async(score) => {
        update_word(word, score)
        const response = await load_word()
        if (response.ok) {
            learnState.showAnswer = false
        }
    }

    const learnDeck = $state(appState.deck[userState.preferences.learnDeck])
</script>

{#if learnState.currentWord.length > 0}
<div class="card card-border m-2">
    <div class="card-body">
        <p class="card-title">{learnDeck}</p>
        <!-- <div class="flex justify-between font-thin mt-2">
            <div>{word_classes[word.word_class]}</div>
             <div>{last_try}</div>
        </div> -->
        <div class="card bg-base-200">
            <div class="card-body text-center card-title">
                <p class="font-sans text-4xl capitalize">{word[lang_from]}</p>
                <div class="divider text-xs font-thin">{word_classes[word.word_class]}</div>
                {#each learnState.currentWord as word_answer}
                <p class="font-sans text-4xl capitalize">
                    {learnState.showAnswer ? word_answer[lang_to] : '--'}
                </p>            
                {/each}
            </div>
        </div>
        <!-- <div class="flex justify-end">
            <div class="badge badge-soft font-medium badge-info">
                Score: {score_count}
            </div>
        </div> -->
        <div class="flex gap-x-2">
            {#if learnState.showAnswer}
            <button onclick={() => answer(-1)} class="btn btn-lg btn-error grow">Incorrect</button>
            <button onclick={() => answer(1)} class="btn btn-lg btn-success grow">Correct</button>
            {:else}    
            <button onclick={() => learnState.showAnswer = !learnState.showAnswer} class="btn btn-lg btn-accent grow">
                Reveal
            </button>
            {/if}
        </div>
    </div>
</div>
{:else}
<div class="card card-border bg-base-200 m-2">
    <div class="card-body">
        <p class="card-title">Empty Stack</p>
        <p>No more words in this list.</p>
    </div>
</div>
{/if}