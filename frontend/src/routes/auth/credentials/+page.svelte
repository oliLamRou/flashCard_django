<script>
    import { goto } from "$app/navigation";
	import { api } from "$lib/api/api";
	import { _login, _refresh } from "$lib/api/auth";
	import { userState } from "$lib/state.svelte";
    let username = $state('')
    let password = $state('')
    let authType = $state(true)

    const login = async() => {        
        const response = await _login(username, password)        
        if (response.ok) {
            goto('/app/learn')
        }
    }

    const signUp = () => {
        goto('/auth/register')
    }
</script>

<div class="min-h-screen flex items-center justify-center">
    <fieldset class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
        <form on:submit|preventDefault={login}>
            <legend class="fieldset-legend">Welcome Back!</legend>
        
            <label class="label">Username</label>
            <input type="username" class="input validator" required bind:value={username}/>
        
            <label class="label">Password</label>
            <input type="password" class="input validator" required bind:value={password}/>
        
            <button class="btn btn-block btn-primary mt-4" type="submit">Login</button>
        </form>    
        <a class="link justify-center" on:click={signUp}>Create New Account here!</a>
    </fieldset>
</div>