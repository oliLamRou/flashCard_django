<script>
	import { load_word, update_word } from "$lib/api/learn.js";
	import { userState } from "$lib/state.svelte.js";
	import { onMount } from "svelte";

    let { data } = $props();
    let words = $state(data.words)
    let word = $derived.by(() => {
        if (!words) {
            return null
        }
        return words[0]
    })

    let languageA = $state(userState.preferences.languageA)
    let languageB = $state(userState.preferences.languageB)
    let learnMode = $state(userState.preferences.learnMode)

    let lang_from = $state(learnMode === 'NORMAL' ? languageA : languageB)
    let lang_to = $state(learnMode === 'NORMAL' ? languageB : languageA)
    
    let showAnswer = $state(false)

    const next_word = (async(score) => {
        update_word(word, score)
        const newWord = await load_word()
        words = newWord.words
        showAnswer = false
    })
    
</script>

<div class="card bg-secondary m-3">
    <div class="card-body flex flex-col flex-grow">
        {#if words}
            <p>{lang_from}</p>
            <p class="card-title font-sans text-4xl capitalize">
                {word[lang_from]}
            </p>
            <p class="mt-2">{lang_to}</p>
            {#each words as word_}
            <p class="font-sans text-3xl">
                {showAnswer ? word_[lang_to] : '--'}
            </p>            
            {/each}
            <p class="mt-2">Description</p>
            <p class="font-sans text-lg">{word.description || '--'}</p>
            <div class="card-actions mt-8">
                {#if showAnswer}
                <button onclick={() => next_word(1)} class="btn-xl btn btn-success">Good</button>
                <button onclick={() => next_word(-1)} class="btn-xl btn btn-error">Bad</button>
                {:else}    
                <button onclick={() => showAnswer = !showAnswer} class="btn-xl btn btn-block btn-neutral">Show Answer</button>
                {/if}
            </div>
        {:else}
            <p>No words found</p>
            <p>change your preferences</p>
        {/if}
    </div>
</div>