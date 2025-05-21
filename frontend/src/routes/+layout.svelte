<script>
    import "../app.css";
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import { appState } from "$lib/state.svelte";
    
    let { children } = $props();

    onMount(() => {
        goto('/app/learn')
    })

</script>

{@render children()}