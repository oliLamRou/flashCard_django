<script>
    import { goto } from "$app/navigation";
	import { api } from "$lib/api/api";
	import { _login } from "$lib/api/auth";
    import { _register } from "$lib/api/auth";
    let username = $state('')
    let password = $state('')
    let authType = $state(true)

    let languages = $state([])

    const register = async() => {
        const res_register = await _register(username, password)
        if (res_register.status !== 201) { return }

        const response = await _login(username, password)
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