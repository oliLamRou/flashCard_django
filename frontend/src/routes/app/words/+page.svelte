<script>
    import { onMount } from "svelte";
	import { goto } from "$app/navigation";
    import { api } from "$lib/api/api";
	import { appState, userState } from "$lib/state.svelte";
	import { load_words, remove_word } from "$lib/api/words";

    const { data } = $props()
    let words = $state(data.words)

    let word_classes = $state(appState.word_classes)
    let languageA = $state(userState.preferences.languageA)
    let languageB = $state(userState.preferences.languageB)

    let username = $state(userState.user_info.username)
    let user_id = $state(userState.user_info.id)

    let searchValue = $state()
    let userWords = $state(true)

    let filtered_words = $derived.by(() => {
        let result = words
        if (searchValue) {            
            result = words.filter((word) => {
                const word_a = word[languageA]?.toLowerCase()
                const word_b = word[languageB]?.toLowerCase()
                if (word_a && word_a.includes(searchValue.toLowerCase())) {
                    return word
                } else if (word_b && word_b.includes(searchValue.toLowerCase())) {
                    return word
                }
            })
        }
        if (userWords) {
            result = result.filter((word) => word.user == user_id)
        }

        return result
    })

    const create = (id) => {
        goto('words/edit/')
    }

    const edit = (word) => {
        goto(`/app/words/edit?word=${encodeURIComponent(JSON.stringify(word))}`);
    }

    const batch_import = () => {
        console.log('csv import')
    }

    const remove = async(id) => {
        const response = await remove_word(id)
        if (response.ok) {
            const data = await load_words()
            words = data.words
        }
    }

    const get_score = (word) => {
        if (!word?.user_score) {
            return '--'
        }
        return word.user_score.fail - word.user_score.success
    }
</script>

<div>
    <button onclick={create} class="btn btn-secondary btn-sm">New</button>
    <button onclick={batch_import} disabled class="btn btn-secondary btn-sm">Import</button>
</div>
<div class="flex">
    <label class="label mx-2">
        <input type="checkbox" class="toggle" bind:checked={userWords}/>
        Filter Your Words
    </label>
    <input type="text" placeholder="Search" class="input grow" bind:value={searchValue}/>
</div>    
<div class="overflow-x-auto">
    <table class="table table-zebra table-sm">
        <thead>            
            <tr>
                <th>Archived</th>
                <th>Translation</th>
                <th class="min-w-3">Word Class</th>
                <th class="min-w-1 text-right">Score</th>
                <th>Options</th>
            </tr>
        </thead>
        <tbody>
            {#each filtered_words as word}
                <tr>
                    <td>
                        <input type="checkbox" class="checkbox" checked={"checked" ? word?.user_score?.archive : ""} disabled/>
                    </td>
                    <td>
                        {languageA}: { word[languageA] }
                        <br/>
                        {languageB}: { word[languageB] }
                    </td>                    
                    <td>{word_classes[word.word_class]}</td>
                    <td class="text-right">{get_score(word)}</td>
                    <td>
                        <button 
                            onclick={() => edit(word)}
                            disabled={'disabled' ? word.user !== user_id : 'enable'}
                            class="btn btn-xs btn-outline btn-secondary">Edit</button>
                        <button 
                            onclick={() => remove(word.id)} 
                            disabled={'disabled' ? word.user !== user_id : 'enable'}
                            class="btn btn-xs btn-outline btn-error">Delete</button>
                    </td>
                </tr>
            {/each}
        </tbody>
    </table>
</div>