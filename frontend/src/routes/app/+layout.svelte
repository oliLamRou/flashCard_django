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

<div class="navbar shadow-sm flex justify-between min-h-0 h-10">
    <div>
        <a href="/app/learn" class="btn btn-ghost">
            <CircumIcon name="memo_pad" size=25px/>
        </a>
    </div>
    <div>
        <a href="/app/words" class="btn btn-ghost">
            <CircumIcon name="database" size=25px/>
        </a>
    </div>
    <div>
        <a href="/app/preferences" class="btn btn-ghost">
            <CircumIcon name="settings" size=25px/>
        </a>
    </div>
    <div>
        <button onclick={logout} class="btn btn-ghost">
            <CircumIcon name="logout" size=25px/>
        </button>
    </div>
</div>

{@render children()}