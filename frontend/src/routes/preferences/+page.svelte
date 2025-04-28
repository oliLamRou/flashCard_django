<script>
	import { onMount } from "svelte";
    import { api } from "$lib/api";
	import { goto } from "$app/navigation";

    let preferences = $state({
        'languages': {},
        'modes': {},
        'preferences': {}
    })

    let languageA = $state('')
    let languageB = $state('')
    let learnMode = $state('')

    onMount(async() => {
        load()
    })

    const load = async() => {
        const response = await api('auth/preference/', {})

        if (response.ok) {
            const data = await response.json()
            Object.assign(preferences, data)

            languageA = data.preferences.languageA
            languageB = data.preferences.languageB
            learnMode = data.preferences.learnMode
        }
    }

    const save = async() => {
        const data = {
            languageA: languageA,
            languageB: languageB,
            learnMode: learnMode,
        }

        const response = await api('auth/preference/', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json'
            },
        })
        goto('/words')
    }
    
</script>

<fieldset class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
    <legend class="fieldset-legend">Set your preferences</legend>
  
    <!-- <label class="label">Main Language</label> -->
    <select class="select" bind:value={languageA}>
        {#each Object.entries(preferences.languages) as [k, v]}
            <option value={k}>{v}</option>
        {/each}
    </select>  

    <!-- <label class="label">Language you want to learn</label> -->
    <select class="select" bind:value={languageB}>
        {#each Object.entries(preferences.languages) as [k, v]}
            <option value={k}>{v}</option>
        {/each}
    </select>  

    <!-- <label class="label">Learning Mode</label> -->
    <select class="select" bind:value={learnMode}>
        {#each Object.entries(preferences.modes) as [k, v]}
            <option value={k}>{v}</option>
        {/each}
    </select>
    <div class="divider"></div>
    <button onclick={save} class="btn btn-neutral">Save</button>
</fieldset>