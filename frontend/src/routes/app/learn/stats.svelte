<script>
	import { learnState } from "$lib/state.svelte";
    import CircumIcon from "@klarr-agency/circum-icons-svelte";
	import { onMount } from "svelte";

    const user_score = $derived.by(() => {
        if (!learnState.currentWord || !learnState.currentWord[0]) {
            return
        }
        return learnState.currentWord[0].user_score
    })

    const accuracy = $derived.by(() => {
        if (user_score.success < 1 || user_score.fail < 1) return '--'

        let accuracy = user_score.success / (user_score.success + user_score.fail)
        accuracy = accuracy * 100
        accuracy = Math.round(accuracy)
        return accuracy
    })

    const last_seen = $derived.by(() => {
        if (!user_score.last_try) {return '--'}

        const targetDate = new Date(user_score.last_try);
        const today = new Date();

        // Clear time portion to make the difference in full days
        targetDate.setHours(0, 0, 0, 0);
        today.setHours(0, 0, 0, 0);

        const diffInMs = targetDate - today;
        const diffInDays = Math.round(diffInMs / (1000 * 60 * 60 * 24));        
        if (diffInDays === 0){
            return 'Today'
        } else if (diffInDays === 1) {
            return 'Yesterday'
        } else {
            return diffInDays + ' days ago'
        }
    })

    onMount(() => {
        const currentWord = learnState.currentWord[0]
        console.log($state.snapshot(currentWord.user_score));
    })
</script>

{#if user_score}
<div class="stats grow">
    <div class="stat">
        <div class="stat-title">Accuracy</div>
        <div class="stat-value">{accuracy}%</div>
        <div class="stat-desc">Correct Streak: {user_score.score}</div>
        <div class="stat-desc">Last seen: {last_seen}</div>
    </div>
</div>    
{/if}
