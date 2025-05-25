<script>
	import { goto } from "$app/navigation";
    import { archive_word, load_word } from "$lib/api/learn";
	import { save_prefererences } from "$lib/api/preferences";
	import { appState, learnState, userState } from "$lib/state.svelte";

    let showToast = $state(false);
    let userChoice = $state(userState.preferences.learnDeck)

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
        const word = learnState.currentWord[0]
        const response = await archive_word(word)

        if (response.ok) {
            triggerToast()
        }
        load_word()
    }

    const update = async() => {
        const data = {
            learnDeck: userChoice
        }
        const saved = await save_prefererences(data)
        if (!saved) return
        
        const loaded = await load_word()
        if (!loaded) return
        
        learnState.showAnswer = false
    }

</script>

<div class="card card-border bg-base-100 m-2">
    <div class="card-body">
        <!-- <p class="card-title">Options</p> -->
        <div class="card-actions">
            <button onclick={create} class="btn btn-xs btn-primary">New Word</button>
            <button onclick={archive} class="btn btn-xs btn-warning">Archive</button>
        </div>  
        <p>Flashcard:</p>
        {#each Object.entries(appState.deck) as [k, v]}
            <label class="label" id="userWords"> 
                <input onchange={update} type="radio" name="userChoice" value={k} class="radio radio-sm" bind:group={userChoice} />
                {v}
            </label>            
        {/each}
    </div>
</div>

{#if showToast}
<div class="toast toast-center">
    <div class="alert alert-success">
        <span>Word Archived</span>
    </div>
</div>
{/if}