<script>
    import { goto } from "$app/navigation";
    let username = ''
    let password = ''

    const login = async () => {
        const response = await fetch("http://localhost:8000/api/token/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
                password,
            })
        })
        
        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("access", data.access);
            localStorage.setItem("refresh", data.refresh);
            console.log("Logged in successfully!");
            await goto('/words')
        } else {
            console.error("Login failed:", data);
        }
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
</fieldset>