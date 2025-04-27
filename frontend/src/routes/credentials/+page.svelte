<script>
    import { goto } from "$app/navigation";
	import { api } from "$lib";
    import { login } from "$lib";
    let username = ''
    let password = ''

    const ux_login = async () => {
        const data = await login(username, password)
        goto('/words')
    }

</script>

<fieldset class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
    <form on:submit|preventDefault={ux_login}>
        <legend class="fieldset-legend">Login</legend>
    
        <label class="label">Username</label>
        <input type="username" class="input validator" required placeholder="Email" bind:value={username}/>
    
        <label class="label">Password</label>
        <input type="password" class="input validator" required placeholder="Password" bind:value={password}/>
    
        <button class="btn btn-neutral mt-4" type="submit">Login</button>
    </form>    
</fieldset>