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

    let searchValue = $state()
    let userWords = $state(false)

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
            result = result.filter((word) => word.user == userState.id)
        }

        return result
    })

    const create = (id) => {
        goto('words/edit/')
    }

    const edit = (word) => {
        const wordCopy = JSON.parse(JSON.stringify(word));
        goto('words/edit/', {
            state: {word: wordCopy}
        })
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

</script>

<h1>Hi {userState.username} - {userState.id}!</h1>
<button onclick={create} class="btn btn-secondary btn-sm">New</button>
<button onclick={batch_import} class="btn btn-secondary btn-sm">Import</button>
<input type="text" placeholder="Search" class="input" bind:value={searchValue}/>
<label class="label">
    <input type="checkbox" class="toggle" bind:checked={userWords}/>
    Your Word Only
  </label>
<div class="overflow-x-auto">
    <table class="table table-zebra">
        <thead>            
            <tr>
                <th>ID</th>
                <th>Word Class</th>
                <th>{languageA}</th>
                <th>{languageB }</th>
                <th>Description</th>
                <th>Fail</th>
                <th>Success</th>
                <th>Options</th>
            </tr>
        </thead>
        <tbody>
            {#each filtered_words as word}
                <tr>
                    <td>{ word.user }</td>
                    <td class="capitalize">{ word_classes[word.word_class] }</td>
                    <td class="capitalize">{ word[languageA] }</td>
                    <td class="capitalize">{ word[languageB] }</td>
                    <td>{ word.description }</td>
                    <td>{ word.user_score?.fail }</td>
                    <td>{ word.user_score?.success }</td>
                    <td>
                        <button 
                            onclick={() => edit(word)}
                            disabled={'disabled' ? word.user !== userState.id : 'enable'}
                            class="btn btn-xs btn-outline btn-secondary">Edit</button>
                        <button onclick={() => remove(word.id)} class="btn btn-xs btn-outline btn-warning">Delete</button>
                    </td>
                </tr>
            {/each}
        </tbody>
    </table>
</div>