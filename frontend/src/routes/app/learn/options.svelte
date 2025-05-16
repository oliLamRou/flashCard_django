<script>
	import { goto } from "$app/navigation";
    import { archive_word } from "$lib/api/learn";

    let showToast = $state(false);

	function triggerToast() {
		showToast = true;
		setTimeout(() => {
			showToast = false;
		}, 3000);
	}

    const create = () => {
        goto('/app/words/edit')
    }

    const archive = async() => {
        const response = await archive_word()
        if (true) {
            showToast = !showToast
        }
    }

</script>

<div class="card card-border bg-base-100 m-2">
    <div class="card-body">
        <p class="card-title">Options</p>
        <div class="card-actions">
            <button onclick={create} class="btn btn-xs btn-primary">New Word</button>
            <button disabled class="btn btn-xs btn-primary">New List</button>
            <div class="tooltip" data-tip="Archive it and you can choose in setting to see or not">
                <button onclick={archive} class="btn btn-xs btn-warning">Archive</button>
            </div>
        </div>
    </div>
</div>

{#if showToast}
<div transition:fade class="toast toast-center">
    <div class="alert alert-success">
        <span>Word Created</span>
    </div>
</div>
{/if}