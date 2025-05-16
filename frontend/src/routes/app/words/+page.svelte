<script>
    import { onMount } from "svelte";
	import { goto } from "$app/navigation";
    import { api } from "$lib/api/api";
	import { appState, userState } from "$lib/state.svelte";
	import { load_words, remove_word } from "$lib/api/words";
    import CircumIcon from "@klarr-agency/circum-icons-svelte";
	import { archive_word } from "$lib/api/learn";

    const { data } = $props()
    let words = $state(data.words)

    let word_classes = $state(appState.word_classes)
    let languageA = $state(userState.preferences.languageA)
    let languageB = $state(userState.preferences.languageB)

    let username = $state(userState.user_info.username)
    let user_id = $state(userState.user_info.id)

    let searchValue = $state()
    let userWords = $state(true)

    let bookmarked = $state(false)

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

    const archive = async(word) => {
        const toArchive = word.user_score.archive ? false : true
        const response = await archive_word(word, toArchive)
        if (response.ok) {
            const data = await load_words()
            words = data.words
        }
    }
</script>

<div class="flex m-3">
    <button onclick={create} class="btn btn-sm btn-primary mr-2">New</button>
    <button onclick={batch_import} disabled class="btn btn-sm btn-primary">Import</button>
    <label class="label mx-2">
    <input type="text" placeholder="Search" class="input input-sm grow" bind:value={searchValue}/>
    <input type="checkbox" class="toggle toggle-sm" bind:checked={userWords}/>
        Your Words
    </label>
</div>

<div class="overflow-x-auto">
    <table class="table table-zebra table-sm">
        <thead>            
            <tr class="text-xs bg-base-300">
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
                        {languageA}: { word[languageA] }
                        <br/>
                        {languageB}: { word[languageB] }
                    </td>                    
                    <td>{word_classes[word.word_class]}</td>
                    <td class="text-right">{get_score(word)}</td>
                    <td>
                        <!-- <button 
                            onclick={() => bookmarked = !bookmarked}
                            disabled={'disabled' ? word.user !== user_id : 'enable'}
                            class="btn btn-xs btn-circle btn-warning {bookmarked ? 'btn-soft' : ''}">
                            <CircumIcon name="bookmark" size=15px/>
                        </button>                         -->
                        <button 
                            onclick={() => archive(word)}
                            disabled={'disabled' ? word.user !== user_id : 'enable'}
                            class="btn btn-xs btn-circle btn-info {word?.user_score?.archive ? 'btn-soft' : ''}">
                            <CircumIcon name={word?.user_score?.archive ? 'unread' : 'read'} size=15px/>
                        </button>
                        <button 
                            onclick={() => edit(word)}
                            disabled={'disabled' ? word.user !== user_id : 'enable'}
                            class="btn btn-xs btn-circle btn-secondary">
                            <CircumIcon name="edit" size=15px/>
                        </button>                        
                        <button 
                            onclick={() => remove(word.id)} 
                            disabled={'disabled' ? word.user !== user_id : 'enable'}
                            class="btn btn-circle btn-xs btn-error">
                            <CircumIcon name="trash" size=15px/>
                        </button>                                                
                        <!-- <label>
                            <input type="checkbox" disabled class="toggle" checked={"checked" ? word?.user_score?.archive : ""}/>
                            archived
                        </label> -->
                    </td>
                </tr>
            {/each}
        </tbody>
    </table>
</div>

<style>

</style>