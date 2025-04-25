<script>
	import { onMount } from "svelte";
    import "../app.css";
	import { goto } from "$app/navigation";
	import { refreshToken, removeTokens } from "$lib";
    let { children } = $props();

    onMount(() => {
        goto('/words')
    })

    const logout = () => {
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