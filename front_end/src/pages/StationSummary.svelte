<script lang="ts">

  import { opiClient } from "../lib/client";
  import {
    Button,
    Container,
    Icon,
    Card,
    CardBody,
    CardHeader,
    CardTitle
  } from '@sveltestrap/sveltestrap';
    import { ConfigModelFromJSON, type ConfigModel, type StationModel } from "../lib/openapi_client";

  let loading: boolean = $state(false);
  let stations: any = $state({})

  $inspect(stations )

  var load_stations = () => {
    loading = true
    opiClient.getFullConfigConfigGet().then(x => console.log(Object.values(x.stations)))
  }
  
  load_stations()
</script>

<main>
  <Container class="mx-auto">
    {#each stations as station}
      <p>{station.stationId}</p>
    {/each}

  </Container>  
</main>
