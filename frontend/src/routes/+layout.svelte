<script>
    import "../app.css";
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
    
    let { children } = $props();

    onMount(async() => {
        goto('/auth/credentials')
        // const response = await api('auth/info/', {
        //     method: 'GET',

        // })
        
        // const data = await response.json()
        // Object.assign(userState, data)

        // if (response.status === 200) {
        //     goto('/words')
        // } else {
        //     goto('/credentials')
        // }
    })

</script>

{@render children()}