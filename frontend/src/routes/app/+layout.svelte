<script>
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import { _remove_user } from "$lib/api/auth";
	import { api } from "$lib/api/api";
	import { userState } from "$lib/state.svelte";
    
    let { children } = $props();

    // onMount(async() => {
    //     console.log("RELOAD");
    //     const response = await api('auth/info/', {
    //         method: 'GET',

    //     })
        
    //     const data = await response.json()
    //     Object.assign(userState, data)

    //     if (response.status === 200) {
    //         goto('/words')
    //     } else {
    //         goto('/credentials')
    //     }
    // })

    const logout = async() => {
        _remove_user()
        goto('auth/credentials')
    }

</script>

<div class="navbar bg-base-100 shadow-sm">
    <div class="flex-1">
        <a href="/app/words" class="btn btn-ghost text-xl">Words</a>
    </div>
    <div class="flex-1">
        <a href="/app/learn" class="btn btn-ghost text-xl">Learn</a>
    </div>
    <div class="flex-1">
        <a href="/app/preferences" class="btn btn-ghost text-xl">Preferences</a>
    </div>
    <div class="flex-1">
        <button onclick={logout} class="btn btn-ghost text-xl">Logout</button>
    </div>
</div>

{@render children()}