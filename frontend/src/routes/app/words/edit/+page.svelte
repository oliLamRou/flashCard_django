<script>
	import { goto } from "$app/navigation";
	import { appState, userState } from "$lib/state.svelte";
	import { create } from "$lib/api/word.js";
	import { fade } from "svelte/transition";

    let showToast = $state(false);

	function triggerToast() {
		showToast = true;
		setTimeout(() => {
			showToast = false;
		}, 3000);
	}

    let languageA = $state(userState.preferences.languageA)
    let languageB = $state(userState.preferences.languageB)
    let languages = $state(appState.languages)
    let word_classes = $state(appState.word_classes)
    
    let { data } = $props()
    let word = $state(data)

    const save = async() => {
        const response = await create(word)
        if (response.ok) {
            triggerToast()
            word.word_languageA = null
            word.word_languageB = null
            word.description = null
            word.word_class = word_classes.undef
        }
    }

</script>

<fieldset class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
    <form onsubmit={save}>
        <legend class="fieldset-legend">Write a word and it's translation</legend>
    
        <label for='id' class="label">{languages[languageA]}</label>
        <input bind:value={word.word_languageA} type="text" class="input validator" required minlength="2"/>
        <p class="validator-hint">Must be 2 characters at least</p>

        <label for='id' class="label">{languages[languageB]}</label>
        <input bind:value={word.word_languageB} type="text" class="input validator" required minlength="2"/>
        <p class="validator-hint">Must be 2 characters at least</p>

        <label for='id' class="label">Word Class</label>
        <select class='select' bind:value={word.word_class}>
            {#each Object.entries(word_classes) as [k, v]}
                <option value={k}>{v}</option>
            {/each}
        </select>

        <label for='id' class="label">Description</label>
        <input bind:value={word.description} type="text" class="input"/>

        <div class="divider"></div>
        
        <button type="submit" class="btn btn-neutral">Save</button>
    </form>
</fieldset>

{#if showToast}
<div transition:fade class="toast toast-center">
    <div class="alert alert-success">
        <span>Word Created</span>
    </div>
</div>
{/if}