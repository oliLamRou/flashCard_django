<script>
	import { goto } from "$app/navigation";
	import { appState, userState } from "$lib/state.svelte";
	import { load_words, remove_word } from "$lib/api/words";
    import CircumIcon from "@klarr-agency/circum-icons-svelte";
	import { archive_word } from "$lib/api/learn";
	import { days_since } from "$lib/utils";
	import { load } from "../+layout.js";
	import { page } from "$app/state";

    const { data } = $props()

    let words = $state(data.words)
    const languageA_value = appState.languages[userState.preferences.languageA]
    const languageB_value = appState.languages[userState.preferences.languageB]
    
    let filters = $state({
        page_amount: data.page_amount,
        everyoneWords: false,
        archived: false,
        current_page: data.current_page,
        search: '',
        page: 0
    })

    const get_word_list = async(event) => {
        if (event.type == 'reset') {filters.search = ''}
        
        const attr = event.currentTarget.dataset
        filters.page = attr.page ? attr.page : 0

        const data = await load_words(filters)
        if (data) { 
            words = data.words
            filters.current_page = data.current_page
            filters.page_amount = data.page_amount
        }
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
            const data = await load_words(filters)
            words = data.words
            filters.current_page = data.current_page
            filters.page_amount = data.page_amount            
        }
    }

    const archive = async(word) => {
        const toArchive = word.user_score.archive ? false : true
        const response = await archive_word(word, toArchive)
        if (response.ok) {
            const data = await load_words(filters)
            words = data.words
            filters.current_page = data.current_page
            filters.page_amount = data.page_amount 
        }
    }

    const get_attemps = (word) => {
        const fail = word.user_score?.fail || 0
        const success = word.user_score?.success || 0
        return fail + success
    }
</script>

<div class="flex gap-x-2 m-2">
    <button onclick={create} class="btn btn-sm btn-primary">Add Words</button>
    <form onsubmit={get_word_list} onreset={get_word_list}>
        <div class="join">
            <input class="input input-sm" type="text" placeholder="Search in {languageA_value} and {languageB_value}" bind:value={filters.search}/>
            <button type="submit" class="btn btn-sm btn-secondary join-item" disabled={!filters.search}>Search</button>
            <button type="reset" onclick={get_word_list} data-action='clearSearch' class="btn btn-sm btn-neutral join-item" disabled={!filters.search}>clear</button>
        </div>
    </form>
    <label class="text-sm">
        <input onchange={get_word_list} class="toggle toggle-sm" type="checkbox" bind:checked={filters.everyoneWords}/>
        Everyones Words
    </label>
    <label class="text-sm">
        <input onchange={get_word_list} class="toggle toggle-sm" type="checkbox" bind:checked={filters.archived}/>
        Archived Words
    </label>    
</div>

<div class="overflow-x-auto rounded-box">
    <table class="table table-zebra table-sm">
        <thead>            
            <tr class="text-sm bg-base-300">
                <th>{languageA_value}</th>
                <th>{languageB_value}</th>
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
            {#each { length: filters.page_amount }, page}
                <button onclick={get_word_list} data-page={page} class="join-item btn btn-xs">{page + 1}</button>
            {/each}
        </div>
    </div>
</div>