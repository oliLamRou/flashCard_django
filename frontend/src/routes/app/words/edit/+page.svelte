<script>
    //load_word should be a load function in .js
    //create should be in /api/word
    
	import { api } from "$lib/api/api";
	import { onMount } from "svelte";
    import { page } from "$app/stores";
	import { goto } from "$app/navigation";
	import { appState, userState } from "$lib/state.svelte";

    let languageA = $state(userState.preferences.languageA)
    let languageB = $state(userState.preferences.languageB)
    let languages = $state(appState.languages)
    let word_classes = $state(appState.word_classes)

    //Form Data
    let word_id = $state()
    let word_languageA = $state('')
    let word_languageB = $state('')
    let word_class = $state('undef')
    let description = $state('')

    const load_word = async() => {
        const word = $page.state.word
        if (word) {
            word_id = word['id']
            word_languageA = word[languageA]
            word_languageB = word[languageB]
            word_class = word['word_class']
            description = word['description']
        }
    }

    const create = async() => {
        const data = {
            [languageA]: word_languageA,
            [languageB]: word_languageB,
            word_class: word_class,
            description: description,
        }

        if (word_id) { data['id'] = word_id }

        const method = (word_id) ? 'PATCH' : 'POST'

        const response = await api('dictionary/new/', {
            method: method,
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json'
            },
        })

        //This is weak
        if (response.ok) {
            goto('app/words')
        }
    }

</script>

<fieldset class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
    <form onsubmit={create}>
        <legend class="fieldset-legend">Write a word and it's translation</legend>
    
        <label for='id' class="label">{languages[languageA]}</label>
        <input bind:value={word_languageA} type="text" class="input validator" required minlength="2"/>
        <p class="validator-hint">Must be 2 characters at least</p>

        <label for='id' class="label">{languages[languageB]}</label>
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