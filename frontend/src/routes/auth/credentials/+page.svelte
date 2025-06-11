<script>
	import { goto } from '$app/navigation';
	import { api } from '$lib/api/api';
	import { _login, _refresh } from '$lib/api/auth';
	import { userState } from '$lib/state.svelte';
	import { onMount } from 'svelte';

	let username = $state('');
	let password = $state('');
	let authType = $state(true);
	let waiting = $state(false);

	onMount(() => {
		if (localStorage.getItem('REFRESH_TOKEN_KEY')) {
			console.info('User Return, Trying redirect to /learn');
			goto('/app/learn');
		}
	});

	const login = async () => {
		if (waiting) return;
		waiting = true;
		const response = await _login(username, password);
		if (response) {
			waiting = false;
			goto('/app/learn');
		}
	};

	const signUp = () => {
		goto('/auth/register');
	};
</script>

<div class="min-h-screen flex items-center justify-center">
	<fieldset class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
		<form on:submit|preventDefault={login}>
			<legend class="fieldset-legend">Welcome Back!</legend>

			<label class="label">Username</label>
			<input type="username" class="input validator" required bind:value={username} />

			<label class="label">Password</label>
			<input type="password" class="input validator" required bind:value={password} />

			<button class="btn btn-block btn-primary mt-4" type="submit">Login</button>
		</form>
		<a class="link justify-center" on:click={signUp}>Create New Account here!</a>
	</fieldset>
</div>

