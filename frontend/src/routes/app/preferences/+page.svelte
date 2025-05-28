<script>
	import { goto } from "$app/navigation";
	import { save_prefererences } from "$lib/api/preferences.js";
	import { appState, userState } from "$lib/state.svelte.js";

    let languages = $state(appState.languages)
    let modes = $state(appState.modes)

    let languageA = $state(userState.preferences.languageA)
    let languageB = $state(userState.preferences.languageB)
    let learnMode = $state(userState.preferences.learnMode)

    const save = async() => {
        const data = {
            languageA: languageA,
            languageB: languageB,
            learnMode: learnMode,
        }

        const response = await save_prefererences(data)
        if (response) {
            goto('/app/learn')
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

        <button onclick={save} class="btn btn-primary">Save</button>
    </fieldset>
</div>