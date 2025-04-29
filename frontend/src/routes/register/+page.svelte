<script>
    import { goto } from "$app/navigation";
	import { api } from "$lib/api";
	import { getTokens } from "$lib/auth";
    import { register } from "$lib/auth";
    let username = $state('')
    let password = $state('')
    let authType = $state(true)

    let languages = $state([])

    const sign_up = async() => {
        const res_register = await register(username, password)
        if (res_register.status !== 201) { return }

        const response = await getTokens(username, password)
    }

</script>

<h1>Sign Up</h1>
<fieldset class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
    <form on:submit|preventDefault={sign_up}>
        <legend class="fieldset-legend">Login</legend>
    
        <label class="label">Username</label>
        <input type="username" class="input validator" required placeholder="Username" bind:value={username}/>
    
        <label class="label">Password</label>
        <input type="password" class="input validator" required placeholder="Password" bind:value={password}/>
    
        <button class="btn btn-neutral mt-4" type="submit">Sign Up</button>
    </form>    
</fieldset>