<script>
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import { _remove_user } from "$lib/api/auth";
	import { api } from "$lib/api/api";
	import { userState } from "$lib/state.svelte";

    import CircumIcon from "@klarr-agency/circum-icons-svelte";
    
    let { children } = $props();

    const logout = async() => {
        _remove_user()
        goto('auth/credentials')
    }

</script>

<div class="navbar bg-base-100 shadow-sm flex justify-between">
    <div>
        <a href="/app/learn" class="btn btn-ghost text-xl">
            <CircumIcon name="credit_card_2"/>
        </a>
    </div>
    <div>
        <a href="/app/words" class="btn btn-ghost text-xl">
            <CircumIcon name="edit"/>
        </a>
    </div>
    <div>
        <a href="/app/preferences" class="btn btn-ghost text-xl">
            <CircumIcon name="settings"/>
        </a>
    </div>
    <div>
        <button onclick={logout} class="btn btn-ghost text-xl">
            <CircumIcon name="logout"/>
        </button>
    </div>
</div>

{@render children()}