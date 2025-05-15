<script>
    import Stats from "./stats.svelte";
    import Options from "./options.svelte";
    import Flashcard from "./flashcard.svelte";

    let { data } = $props();
    let words = $state(data.words)
    
</script>

<Stats/>
<Flashcard words={words}/>
<Options/>