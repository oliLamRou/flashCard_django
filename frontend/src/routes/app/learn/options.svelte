<script>
	import { goto } from "$app/navigation";
    import { archive_word, load_word } from "$lib/api/learn";
	import { save_prefererences } from "$lib/api/preferences";
	import { appState, currentWords, userState } from "$lib/state.svelte";

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
        const word = currentWords[0]
        const response = await archive_word(word)

        if (response.ok) {
            triggerToast()
        }
        load_word()
    }

    $effect(() => {
        const data = {
            learnDeck: userChoice
        }
        save_prefererences(data)
    })

</script>

<div class="card card-border bg-base-100 m-2">
    <div class="card-body">
        <p class="card-title">Options</p>
        <div class="card-actions">
            <button onclick={create} class="btn btn-xs btn-primary">New Word</button>
            <div class="tooltip" data-tip="Archive it and you can choose in setting to see or not">
                <button onclick={archive} class="btn btn-xs btn-warning">Archive</button>
            </div>
        </div>  
        {#each Object.entries(appState.deck) as [k, v]}
            <label class="label" id="userWords"> 
                <input type="radio" name="userChoice" value={k} class="radio" bind:group={userChoice} />
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