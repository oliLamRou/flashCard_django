

<script>
    fetch('/api/word/')
        .then(res => res.json())
        .then(data => {
        console.log(data.message); // "Hello from Django!"
    });
</script>


<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>
