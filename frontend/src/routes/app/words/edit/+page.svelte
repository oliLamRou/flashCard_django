<script>
	import { goto } from "$app/navigation";
	import { appState, userState } from "$lib/state.svelte";
	import { create } from "$lib/api/word.js";
	import { fade } from "svelte/transition";
	import { update_word } from "$lib/api/learn.js";

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
    let formEl

    const save = async() => {
        const response = await create(word)
        if (response && word.word_id) {
            goto('/app/words')
        }
        
        triggerToast()
        formEl.reset()
    }

</script>
<div class="min-h-screen flex items-center justify-center">
    <fieldset class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
    <form onsubmit={save} bind:this={formEl}>
        <legend class="fieldset-legend">{word.word_id ? 'Edit Word' : 'New Word'}</legend>
    
        <label for='id' class="label">{languages[languageA]}</label>
        <input bind:value={word.word_languageA} type="text" class="input validator" required minlength="1"/>
        <p class="validator-hint">Minimum 1 character</p>

        <label for='id' class="label">{languages[languageB]}</label>
        <input bind:value={word.word_languageB} type="text" class="input validator" required minlength="1"/>
        <p class="validator-hint">Minimum 1 character</p>

        <label for='id' class="label">Word Class</label>
        <select class='select' bind:value={word.word_class}>
            {#each Object.entries(word_classes) as [k, v]}
                <option value={k}>{v}</option>
            {/each}
        </select>

        <div class="divider"></div>
        
        <button type="submit" class="btn btn-primary">Save</button>
    </form>
</fieldset>
</div>

{#if showToast}
<div transition:fade class="toast toast-center">
    <div class="alert alert-success">
        <span>Word Created</span>
    </div>
</div>
{/if}