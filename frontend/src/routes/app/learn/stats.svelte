<script>
	import { learnState } from "$lib/state.svelte";
	import { days_since } from "$lib/utils";
    import CircumIcon from "@klarr-agency/circum-icons-svelte";

    const user_score = $derived.by(() => {
        if (!learnState.currentWord || !learnState.currentWord[0]) {
            return
        }
        return learnState.currentWord[0].user_score
    })

    const accuracy = $derived.by(() => {
        if (user_score.success == 0 && user_score.fail == 0) return '--'
        if (user_score.fail == 0 && user_score.success > 0) return 100
        if (user_score.success == 0 && user_score.fail > 0) return 0

        let accuracy = user_score.success / (user_score.success + user_score.fail)
        accuracy = accuracy * 100
        accuracy = Math.round(accuracy)
        return accuracy
    })
</script>


<div class="stats grow">
    <div class="stat">
        {#if user_score}
        <div class="stat-title">Accuracy</div>
        <div class="stat-value">{accuracy}%</div>
        <div class="stat-desc">Correct Streak: {user_score.score}</div>
        <div class="stat-desc">Last Attempt: {days_since(user_score.last_try)}</div>
        {:else}
        <div class="stat-title">No Stats for Yet!</div>
        {/if}
    </div>
</div>

