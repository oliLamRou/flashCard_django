<script>
	import { api } from "$lib/api";
	import { onMount } from "svelte";
    import { page } from "$app/stores";
	import { goto } from "$app/navigation";

    let word_modal = $state()

    //Enum
    let word_classes = $state([])
    let languages = $state({})

    //User
    let preferences = $state({})
    
    //Form Data
    let word_languageA = $state('')
    let word_languageB = $state('')
    let word_class = $state('undef')
    let description = $state('')

    onMount(async() => {
        await load_preference()
        await load_word_classes()
        load_word()
    })

    const load_preference = async() => {
        const response = await api('auth/preference/', {
            method: 'GET'
        })

        if (response.ok) {
            const data = await response.json()
            Object.assign(languages, data.languages)
            Object.assign(preferences, data.preferences)
        }

        return response
    }

    const load_word_classes = async() => {
        const response = await api('dictionary/word_classes/', {
            method: 'GET'
        })

        if (response.ok) {
            const data = await response.json()
            Object.assign(word_classes, data.word_classes)
        }

        return response
    }

    const load_word = async() => {
        const word = $page.state.word
        if (word) {
            word_languageA = word[preferences.languageA]
            word_languageB = word[preferences.languageB]
            word_class = word['word_class']
            description = word['description']
        }
    }

    const create = async() => {
        const data = {
            [preferences.languageA]: word_languageA,
            [preferences.languageB]: word_languageB,
            word_class: word_class,
            description: description,
        }
        const response = await api('dictionary/new/', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json'
            },
        })

        if (response.ok) {
            goto('/words')
        }
    }

</script>

<fieldset class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
    <form onsubmit={create}>
        <legend class="fieldset-legend">Write a word and it's translation</legend>
    
        <label for='id' class="label">{languages[preferences.languageA]}</label>
        <input bind:value={word_languageA} type="text" class="input validator" required minlength="2"/>
        <p class="validator-hint">Must be 2 characters at least</p>

        <label for='id' class="label">{languages[preferences.languageB]}</label>
        <input bind:value={word_languageB} type="text" class="input validator" required minlength="2"/>
        <p class="validator-hint">Must be 2 characters at least</p>

        <label for='id' class="label">Word Class</label>
        <select class='select' bind:value={word_class}>
            {#each Object.entries(word_classes) as [k, v]}
                <option value={k}>{v}</option>
            {/each}
        </select>

        <label for='id' class="label">Description</label>
        <input bind:value={description} type="text" class="input"/>

        <div class="divider"></div>
        
        <button type="submit" class="btn btn-neutral">Save</button>
    </form>
</fieldset>