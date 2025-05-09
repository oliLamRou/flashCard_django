<script>
	import { goto } from "$app/navigation";
	import { save_prefererences } from "$lib/api/preferences.js";
	import { appState, userState } from "$lib/state.svelte.js";
	import { onMount } from "svelte";

    let languages = $state(appState.languages)
    let modes = $state(appState.modes)

    let languageA = $state(userState.preferences.languageA)
    let languageB = $state(userState.preferences.languageB)
    let learnMode = $state(userState.preferences.learnMode)
    let userWordsPerc = $state(userState.preferences.learnUserWordsPerc)
    let favoriteWordsPerc = $state(userState.preferences.learnFavoriteWordsPerc)
    let newWordsPerc = $state(userState.preferences.learnNewWordsPerc)
    let failWordsPerc = $state(userState.preferences.learnFailWordsPerc)
    let successWordsPerc = $state(userState.preferences.learnSuccessWordsPerc)

    const save = async() => {
        const data = {
            languageA: languageA,
            languageB: languageB,
            learnMode: learnMode,
            learnUserWordsPerc: userWordsPerc,
            learnFavoriteWordsPerc: favoriteWordsPerc,
            learnNewWordsPerc: newWordsPerc,
            learnFailWordsPerc: failWordsPerc,
            learnSuccessWordsPerc: successWordsPerc,
        }

        const response = await save_prefererences(data)
        if (response.ok) {
            goto('/app/words')
        }
    }
    
</script>

<div class="min-h-screen flex items-center justify-center">
    <fieldset class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
        <legend class="fieldset-legend">Set your preferences</legend>
    
        <label for="id" class="label">Main Language</label>
        <select class="select" bind:value={languageA}>
            {#each Object.entries(languages) as [k, v]}
                <option value={k}>{v}</option>
            {/each}
        </select>  

        <label for="id" class="label">Language you want to learn</label>
        <select class="select" bind:value={languageB}>
            {#each Object.entries(languages) as [k, v]}
                <option value={k}>{v}</option>
            {/each}
        </select>  

        <label for="id" class="label">Learning Mode</label>
        <select class="select" bind:value={learnMode}>
            {#each Object.entries(modes) as [k, v]}
                <option value={k}>{v}</option>
            {/each}
        </select>
        
        <div class="divider"></div>

        <label for="id" class="label">Others Words</label>
        <input type="range" min="0" max="1" bind:value={userWordsPerc} class="range" step="1"/>
        <label for="id" class="label">New Words</label>
        <input type="range" min="0" max="1" bind:value={newWordsPerc} class="range" step="0.01"/>
        <label for="id" class="label">Favorite Words</label>
        <input type="range" min="0" max="1" bind:value={favoriteWordsPerc} class="range" step="0.01"/>
        <label for="id" class="label">Fail Words</label>
        <input type="range" min="0" max="1" bind:value={failWordsPerc} class="range" step="0.01"/>
        <label for="id" class="label">Success Words</label>
        <input type="range" min="0" max="1" bind:value={successWordsPerc} class="range" step="0.01"/>

        <div class="flex justify-between px-2.5 mt-2 text-xs">
            <span>0%</span>
            <span>50%</span>
            <span>100%</span>
        </div>

        <div class="divider"></div>

        <button onclick={save} class="btn btn-neutral">Save</button>
    </fieldset>
</div>