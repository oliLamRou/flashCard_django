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
        if (response.ok) {
            goto('/app/learn')
        }
    }

    const signIn = () => {
        goto('/auth/credentials')
    }

</script>

<div class="min-h-screen flex items-center justify-center">
    <fieldset class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
        <form on:submit|preventDefault={register}>
            <legend class="fieldset-legend">Create An Account</legend>
        
            <label class="label">Username</label>
            <input type="username" class="input validator" required bind:value={username}/>
        
            <label class="label">Password</label>
            <input type="password" class="input validator" required bind:value={password}/>
        
            <button class="btn btn-block btn-primary mt-4" type="submit">Sign Up</button>
        </form>    
        <a class="link justify-center" on:click={signIn}>Already Having An Account?</a>
    </fieldset>
</div>