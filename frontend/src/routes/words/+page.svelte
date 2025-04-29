<script>
    import { onMount } from "svelte";
    import { api } from "$lib/api";
	import { goto } from "$app/navigation";
	import stat from "daisyui/components/stat";

    let words = $state([])
    let preference = $state({})
    let word_classes = $state({})

    let searchValue = $state()

    let filtered_words = $derived.by(() => {
        if (!searchValue || searchValue === '') {return words}
        const result = words.filter((word) => {
            const word_a = word[preference.languageA]?.toLowerCase()
            const word_b = word[preference.languageB]?.toLowerCase()
            if (word_a && word_a.includes(searchValue)) {
                return word
            } else if (word_b && word_b.includes(searchValue)) {
                return word
            }
        })
        return result
    })

    onMount(async() => {
        load_word_classes()
        load()
    })

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

    const load = async() => {
        const response = await api('dictionary/', {
            method: 'GET'
        })

        if (response.ok) {
            const data = await response.json()
            Object.assign(words, data.words)
            Object.assign(preference, data.preference)
        }
    }

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
        const response = await api('dictionary/delete/', {
            method: 'POST',
            body: JSON.stringify({'id': id}),
            headers: {
                'Content-Type': 'application/json'
            },
        })

        if (response.ok) {
            load()
        }
    }

</script>

<button onclick={create} class="btn btn-secondary btn-sm">New</button>
<button onclick={batch_import} class="btn btn-secondary btn-sm">Import</button>
<input type="text" placeholder="Search" class="input" bind:value={searchValue}/>
<div class="overflow-x-auto">
    <table class="table table-zebra">
        <thead>            
            <tr>
                <th>User</th>
                <th>{ preference?.languageA}</th>
                <th>{ preference?.languageB }</th>
                <th>Description</th>
                <th>Word Class</th>
                <th>Fail</th>
                <th>Success</th>
                <th>Options</th>
            </tr>
        </thead>
        <tbody>
            {#each filtered_words as word}
            <tr>
                <td>{ word.user }</td>
                <td>{ word[preference.languageA] }</td>
                <td>{ word[preference.languageB] }</td>
                <td>{ word.description }</td>
                <td>{ word_classes[word.word_class] }</td>
                <td>{ word.user_score?.fail }</td>
                <td>{ word.user_score?.success }</td>
                <td>
                    <button onclick={() => edit(word)} class="btn btn-xs btn-outline btn-secondary">Edit</button>
                    <button onclick={() => remove(word.id)} class="btn btn-xs btn-outline btn-warning">Delete</button>
                </td>
            </tr>
            {/each}
        </tbody>
    </table>
</div>