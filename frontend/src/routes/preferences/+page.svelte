<script>
	import { goto } from "$app/navigation";
	import { save_prefererences } from "$lib/api/preferences.js";

    let { data } = $props()

    let preferences = $state(data.preferences)
    let languages = $state(data.languages)
    let modes = $state(data.modes)
    let languageA = $state(preferences.languageA)
    let languageB = $derived(preferences.languageB)
    let learnMode = $state(preferences.learnMode)

    const save = async() => {
        const response = await save_prefererences(languageA, languageB, learnMode)
        if (response.ok) {
            goto('/words')
        }
    }
    
</script>

<div class="min-h-screen flex items-center justify-center">
    <!-- <div class="card w-full bg-base-200 shadow-xl rounded-2xl max-w-md"> -->
        <fieldset class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
            <legend class="fieldset-legend">Set your preferences</legend>
        
            <!-- <label class="label">Main Language</label> -->
            <select class="select" bind:value={languageA}>
                {#each Object.entries(languages) as [k, v]}
                    <option value={k}>{v}</option>
                {/each}
            </select>  

            <!-- <label class="label">Language you want to learn</label> -->
            <select class="select" bind:value={languageB}>
                {#each Object.entries(languages) as [k, v]}
                    <option value={k}>{v}</option>
                {/each}
            </select>  

            <!-- <label class="label">Learning Mode</label> -->
            <select class="select" bind:value={learnMode}>
                {#each Object.entries(modes) as [k, v]}
                    <option value={k}>{v}</option>
                {/each}
            </select>
            <div class="divider"></div>
            <button onclick={save} class="btn btn-neutral">Save</button>
        </fieldset>
    <!-- </div> -->
</div>