<script lang="ts">
  import "../node_modules/bootstrap/dist/css/bootstrap.css";
  import "../node_modules/bootstrap-icons/font/bootstrap-icons.css"
  import "../node_modules/bootstrap-icons/font/fonts/bootstrap-icons.woff2"

  import Default from "./pages/Default.svelte"
  import PrintEnv from "./pages/PrintEnv.svelte"
  import StationSummary from "./pages/StationSummary.svelte"
  import NotFound from "./pages/NotFound.svelte"

  // Nav Import 
    import {
    Collapse,
    NavbarToggler,
    NavbarBrand,
    Nav,
    Navbar,
    NavItem,
    NavLink,
    Dropdown,
    DropdownToggle,
    DropdownMenu,
    DropdownItem
  } from '@sveltestrap/sveltestrap';


  // nav logic 
  let isOpen = false;

  function handleUpdate(event) {
    isOpen = event.detail.isOpen;
  }

  var hash_loc: string | undefined = undefined;
  if (hash_loc === undefined){
    hash_loc = window.location.hash
  }

  var update_hash = (_x: HashChangeEvent) => hash_loc = window.location.hash;

</script>

<svelte:window on:hashchange={update_hash} />

<Navbar color="light" light expand="md" container="md">
  <NavbarBrand href="/">NavBar with md container</NavbarBrand>
  <NavbarToggler on:click={() => (isOpen = !isOpen)} />
  <Collapse {isOpen} navbar expand="md" on:update={handleUpdate}>
    <Nav class="ms-auto" navbar>
      <NavItem>
        <NavLink href="#components/">Components</NavLink>
      </NavItem>
      <NavItem>
        <NavLink href="https://github.com/sveltestrap/sveltestrap">GitHub</NavLink>
      </NavItem>
      <Dropdown nav inNavbar>
        <DropdownToggle nav caret>Options</DropdownToggle>
        <DropdownMenu end>
          <DropdownItem>Option 1</DropdownItem>
          <DropdownItem>Option 2</DropdownItem>
          <DropdownItem divider />
          <DropdownItem>Reset</DropdownItem>
        </DropdownMenu>
      </Dropdown>
    </Nav>
  </Collapse>
</Navbar>

<main>
  {#if hash_loc === "#home" || hash_loc === ""}
    <StationSummary />
  {:else if hash_loc === "#vite_default"}
    <Default /> 
  {:else }
    <NotFound />
  {/if}
</main>
