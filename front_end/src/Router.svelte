<script lang="ts">
  import "../node_modules/bootstrap/dist/css/bootstrap.css";
  import "../node_modules/bootstrap-icons/font/bootstrap-icons.css"
  import "../node_modules/bootstrap-icons/font/fonts/bootstrap-icons.woff2"

  import Default from "./Default.svelte";
  import NotFound from "./NotFound.svelte";
  import Home from "./Home.svelte";

  var hash_loc: string | undefined = undefined;
  if (hash_loc === undefined){
    hash_loc = window.location.hash
  }

  var update_hash = (_x: HashChangeEvent) => hash_loc = window.location.hash;

</script>

<svelte:window on:hashchange={update_hash} />

<main>
  {#if hash_loc === "#home" || hash_loc === ""}

    <Home />
  {:else if hash_loc === "#vite_default"}
    <Default />
  {:else }
    <NotFound/>
  {/if}
</main>
