<script>
	import { goto } from "$app/navigation";
	import { appState, userState } from "$lib/state.svelte";
	import { load_words, remove_word } from "$lib/api/words";
    import CircumIcon from "@klarr-agency/circum-icons-svelte";
	import { archive_word } from "$lib/api/learn";
	import { days_since } from "$lib/utils";
	import { load } from "../+layout.js";

    const { data } = $props()
    let words = $state(data.words)
    let page_amount = $state(data.page_amount)
    let current_page = $state(data.current_page)
    let allWords = $state(false)

    const reload_words = (data) => {
        words = data.words
        page_amount = data.page_amount
        current_page = data.current_page
    }

    const create = (id) => {
        goto('words/edit/')
    }

    const edit = (word) => {
        goto(`/app/words/edit?word=${encodeURIComponent(JSON.stringify(word))}`);
    }

    const remove = async(id) => {
        const response = await remove_word(id)
        if (response.ok) {
            const data = await load_words()
            words = data.words
        }
    }

    const archive = async(word) => {
        const toArchive = word.user_score.archive ? false : true
        const response = await archive_word(word, toArchive)
        if (response.ok) {
            const data = await load_words()
            words = data.words
        }
    }

    const get_user_words = async() => {
        const data = await load_words(current_page, allWords)
        if (data) { reload_words(data) }
    }

    const get_new_page = async(page) => {
        const data = await load_words(page, allWords)
        if (data) { reload_words(data) }
    }

    const get_attemps = (word) => {
        const fail = word.user_score?.fail || 0
        const success = word.user_score?.success || 0
        return fail + success
    }
</script>

<div class="flex m-3">
    <button onclick={create} class="btn btn-sm btn-primary mr-2">Add Words</button>
    <label>
        <input onchange={get_user_words} class="toggle" type="checkbox" bind:checked={allWords}/>
        Everyones words
    </label>
</div>

<div class="overflow-x-auto rounded-box">
    <table class="table table-zebra table-sm">
        <thead>            
            <tr class="text-sm bg-base-300">
                <th>{userState.preferences.languageA}</th>
                <th>{userState.preferences.languageB}</th>
                <!-- <th>Word Class</th> -->
                <th>Created</th>
                <!-- <th>By</th> -->
                <th class="text-right">Last Attempt</th>
                <th class="text-right">Attempts</th>
                <th class="text-right">Streak</th>
                <th>Options</th>
            </tr>
        </thead>
        <tbody>
            {#each words as word}
                <tr>
                    <td>{ word[userState.preferences.languageA] }</td>
                    <td>{ word[userState.preferences.languageB] }</td>
                    <!-- <td>{ appState.word_classes[word.word_class]}</td> -->
                    <td>{ word.create_at}</td>
                    <!-- <td>{ word.user}</td> -->
                    <td class="text-right">{days_since(word.user_score)}</td>
                    <td class="text-right">{get_attemps(word)}</td>
                    <td class="text-right">{word.user_score?.score || 0}</td>
                    <td>
                        <button 
                            onclick={() => archive(word)}
                            class="btn btn-xs btn-circle btn-info {word?.user_score?.archive ? 'btn-soft' : ''}">
                            <CircumIcon name={word?.user_score?.archive ? 'unread' : 'read'} size=15px/>
                        </button>
                        <button 
                            onclick={() => edit(word)}
                            disabled={'disabled' ? word.user !== userState.user_info.id : 'enable'}
                            class="btn btn-xs btn-circle btn-secondary">
                            <CircumIcon name="edit" size=15px/>
                        </button>                        
                        <button 
                            onclick={() => remove(word.id)} 
                            disabled={'disabled' ? word.user !== userState.user_info.id : 'enable'}
                            class="btn btn-circle btn-xs btn-error">
                            <CircumIcon name="trash" size=15px/>
                        </button>
                    </td>
                </tr>
            {/each}
        </tbody>
    </table>
    <div class="mt-2 flex justify-center">
        <div class="join">
            {#each { length: page_amount }, page}
                <button onclick={() => get_new_page(page)} class="join-item btn btn-xs">{page + 1}</button>
            {/each}
        </div>
    </div>
</div>