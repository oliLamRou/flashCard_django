<script>
    import "../app.css";
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import { appState, userState } from "$lib/state.svelte";
    
    let { children } = $props();

    onMount(() => {
        if (localStorage.getItem('REFRESH_TOKEN_KEY')) {
            console.info("User Return, Trying redirect to /learn")
            goto('/app/learn')
        } else {
            goto('/auth/credentials')
        }
    })

</script>

{@render children()}