<script>
	import { load_word, update_word } from "$lib/api/learn.js";
	import { appState, userState } from "$lib/state.svelte.js";
	import { onMount } from "svelte";
	import flattenColorPalette from "tailwindcss/lib/util/flattenColorPalette";

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

    const word_classes = appState.word_classes

    let showAnswer = $state(false)

    const next_word = async(score) => {
        update_word(word, score)
        const newWord = await load_word()

        words = newWord?.words || null
        showAnswer = false
    }

    //THIS IN IS COMPONENT LATER
	import { goto } from "$app/navigation";
    import { archive_word } from "$lib/api/learn";
	import { fade } from "svelte/transition";

    let showToast = $state(false);

	function triggerToast() {
		showToast = true;
		setTimeout(() => {
			showToast = false;
		}, 3000);
	}

    const create = () => {
        goto('/app/words/edit')
    }

    const archive = async() => {
        const response = await archive_word(word)
        if (true) {
            triggerToast()
        }
        next_word(0)
    }    
    
</script>

{#if words}
<div class="card card-border m-2">
    <div class="card-body">
        <p class="card-title">LIST NAME</p>
        <div class="flex justify-between font-thin mt-2">
            <div>{word_classes[word.word_class]}</div>
             <div>{last_try}</div>
        </div>
        <div class="card bg-base-200">
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
        <div class="flex mt-4">
            {#if showAnswer}
            <button onclick={() => next_word(-1)} class="btn btn-error btn-lg grow mx-1">Incorrect</button>
            <button onclick={() => next_word(1)} class="btn btn-success btn-lg grow mr-1">Correct</button>
            {:else}    
            <button onclick={() => showAnswer = !showAnswer} class="btn btn-accent btn-lg grow">
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
        <p>No words is matching your filter. Edit settings to see more flashcards.</p>
    </div>
</div>
{/if}
<div class="card card-border bg-base-100 m-2">
    <div class="card-body">
        <p class="card-title">Options</p>
        <div class="card-actions">
            <button onclick={create} class="btn btn-xs btn-primary">New Word</button>
            <button disabled class="btn btn-xs btn-primary">New List</button>
            <div class="tooltip" data-tip="Archive it and you can choose in setting to see or not">
                <button onclick={archive} class="btn btn-xs btn-warning">Archive</button>
            </div>
        </div>
    </div>
</div>

{#if showToast}
<div class="toast toast-center">
    <div class="alert alert-success">
        <span>Word Archived</span>
    </div>
</div>
{/if}