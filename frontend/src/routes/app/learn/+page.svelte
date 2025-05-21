<script>
    import Stats from "./stats.svelte";
    import Options from "./options.svelte";
    import Flashcard from "./flashcard.svelte";
    
</script>

<Flashcard/>
<div class="flex">
    <div class="grow">
        <Options/>
    </div>
    <div class="grow">
        <Stats/>
    </div>
</div>