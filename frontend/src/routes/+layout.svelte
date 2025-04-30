<script>
    import "../app.css";
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import { refreshToken, removeTokens } from "$lib/auth";
    
    let { children } = $props();

    onMount(async() => {
        goto('/credentials')
        if (await refreshToken()){
            goto('/words')
        }
    })

    const logout = async() => {
        removeTokens()    
        goto('/credentials')
    }

</script>

<div class="navbar bg-base-100 shadow-sm">
    <div class="flex-1">
        <a href="/words" class="btn btn-ghost text-xl">Words</a>
    </div>
    <div class="flex-1">
        <a href="/learn" class="btn btn-ghost text-xl">Learn</a>
    </div>
    <div class="flex-1">
        <a href="/preferences" class="btn btn-ghost text-xl">Preferences</a>
    </div>
    <div class="flex-1">
        <button onclick={logout} class="btn btn-ghost text-xl">Logout</button>
    </div>
</div>

{@render children()}