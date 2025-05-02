<script>
    import { goto } from "$app/navigation";
	import { api } from "$lib/api";
	import { _login, _refresh } from "$lib/auth";
	import { userState } from "$lib/state.svelte";
    let username = $state('')
    let password = $state('')
    let authType = $state(true)

    const login = async() => {        
        const response = await _login(username, password)        
        if (response.ok) {
            userState.username = username
            goto('/words')
        }
    }
    const refresh = async() => {
        _refresh()
    }

    const signUp = () => {
        goto('/register')
    }
</script>

<fieldset class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
    <form on:submit|preventDefault={login}>
        <legend class="fieldset-legend">Login</legend>
    
        <label class="label">Username</label>
        <input type="username" class="input validator" required placeholder="Email" bind:value={username}/>
    
        <label class="label">Password</label>
        <input type="password" class="input validator" required placeholder="Password" bind:value={password}/>
    
        <button class="btn btn-neutral mt-4" type="submit">Login</button>
    </form>    
    <button class="btn btn-neutral mt-4" on:click={signUp}>sign up</button>
</fieldset>

<button on:click={refresh}>Refresh</button>