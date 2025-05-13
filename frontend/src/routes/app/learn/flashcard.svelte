<script>
	import { load_word, update_word } from "$lib/api/learn.js";
	import { appState, userState } from "$lib/state.svelte.js";
	import { onMount } from "svelte";

    let { words } = $props();
    let word = $derived(words ? words[0] : null)
    let last_try = $derived(word?.user_score?.last_try || 'Never Seen')

    let score_count = $derived.by(() => {
        const fail = word?.user_score?.fail
        const success = word?.user_score?.success        
        if (fail === null || fail === undefined || success === null || success === undefined ){
            return 0
        }
        return success - fail
    })

    let languageA = $state(userState.preferences.languageA)
    let languageB = $state(userState.preferences.languageB)
    let learnMode = $state(userState.preferences.learnMode)

    let lang_from = $state(learnMode === 'NORMAL' ? languageA : languageB)
    let lang_to = $state(learnMode === 'NORMAL' ? languageB : languageA)

    let archiveIt = $state(false)
    
    const word_classes = appState.word_classes

    let showAnswer = $state(false)

    const next_word = async(score) => {
        console.log(word?.user_score?.success);
        
        update_word(word, score, archiveIt)
        const newWord = await load_word()

        words = newWord?.words || null
        showAnswer = false
    }

    const archive = async() => {
        next_word(word, 0)
    }
    
</script>

{#if words}
<div class="card card-border bg-base-200 m-2">
    <div class="card-body">
        <p class="card-title">LIST NAME</p>
        <div class="flex justify-between font-thin mt-5">
            <div>{word_classes[word.word_class]}</div>
             <div>{last_try}</div>
        </div>
        <div class="card bg-base-100">
            <div class="card-body text-center card-title">
                <p class="font-sans text-4xl capitalize">{word[lang_from]}</p>
                <div class="divider text-xs font-thin">{lang_from} / {lang_to}</div>
                {#each words as word_}
                <p class="font-sans text-4xl capitalize">
                    {showAnswer ? word_[lang_to] : '--'}
                </p>            
                {/each}
            </div>
        </div>
        <div class="flex justify-end">
            <div class="badge badge-soft font-medium badge-info">
                Score: {score_count}
            </div>
        </div>
        <div class="mt-8">
            <label id="archiveIt" class="font-medium">
                <input class="checkbox checkbox-neutral checkbox-warning" type="checkbox" bind:checked={archiveIt}/>
                Archive It
            </label>
            <div class="flex mt-2">
                {#if showAnswer}
                <button onclick={() => next_word(1)} class="btn btn-primary btn-xl grow mr-1">Good</button>
                <button onclick={() => next_word(-1)} class="btn btn-secondary btn-xl grow ml-1">Bad</button>
                {:else}    
                <button onclick={() => showAnswer = !showAnswer} class="btn btn-primary btn-xl grow ml-1">
                    Show Answer
                </button>
                {/if}
            </div>

            <div class="card-actions mt-8">
            </div>            
        </div>
    </div>
</div>
{:else}
<div class="card card-border bg-base-200 m-2">
    <div class="card-body">
        <p class="card-title">Empty Stack</p>
        <p>No words is matching your filter. Edit settings to see more flashcards.</p>
    </div>
</div>
{/if}