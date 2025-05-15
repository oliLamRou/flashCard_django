<script>
	import { goto } from "$app/navigation";

    const create = () => {
        goto('/app/words/edit')
    }
</script>

<div class="card card-border bg-base-200 m-2">
    <div class="card-body">
        <p class="card-title">Options</p>
        <div class="card-actions">
            <button onclick={create} class="btn btn-primary btn-soft">New Word</button>
            <button disabled class="btn btn-primary btn-soft">New List</button>
        </div>
    </div>
</div>