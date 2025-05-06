<script>
	import { load_word, update_word } from "$lib/api/learn.js";
	import { userState } from "$lib/state.svelte.js";

    let { data } = $props();
    let word = $state(data.word)

    let languageA = $state(userState.preferences.languageA)
    let languageB = $state(userState.preferences.languageB)
    
    let showAnswer = $state(false)

    const next_word = (async(score) => {
        update_word(word, score)
        const newWord = await load_word()

        word = newWord.word
        showAnswer = false
    })

</script>

<div class="card bg-secondary m-3">
    <div class="card-body flex flex-col flex-grow">
        <p>{languageA}</p>
        <p class="card-title font-sans text-4xl capitalize">
            {word[languageA]}
        </p>
        <p class="mt-2">{languageB}</p>
        <p class="font-sans text-3xl">
            {showAnswer ? word[languageB] : '--'}
        </p>
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
    </div>
</div>

<!-- <div class="min-h-screen flex items-center justify-center">
    <div class="card w-full bg-base-200 shadow-xl rounded-2xl max-w-md">
        <div class="card-body">
          <h2 class="card-title">Can you guess the word ?</h2>
          <card-body>
            <p>{languageA} - { word[languageA] }</p>
            <label class="swap">
                <input type="checkbox" bind:checked={showAnswer}/>
                <div class="swap-on">{ word[languageB] }</div>
                <div class="swap-off">click for answer</div>
            </label>
            </card-body>
            <p>{ word['description'] }</p>
            <div class="card-actions justify-end">
                <button onclick={() => next_word(1)} class="btn btn-primary">Good</button>
                <button onclick={() => next_word(-1)} class="btn btn-neutral">Bad</button>
            </div>
        </div>
    </div>
</div> -->