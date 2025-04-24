<script>
    import "../app.css";
    let { children } = $props();
</script>


<div class="navbar bg-base-100 shadow-sm">
    <div class="flex-1">
      <a href="/words" class="btn btn-ghost text-xl">Home</a>
    </div>
    <div class="flex-1">
        <a href="/words" class="btn btn-ghost text-xl">Words</a>
    </div>
    <div class="flex-1">
        <a href="/learn" class="btn btn-ghost text-xl">Learn</a>
    </div>
    <div class="flex-1">
        <a href="/preferences" class="btn btn-ghost text-xl">Preferences</a>
    </div>
    <div class="flex-1">
        <a href="/credentials" class="btn btn-ghost text-xl">Logout</a>
    </div>
</div>

{@render children()}