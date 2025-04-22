<script lang="ts">
    import { opiClient } from "../lib/client";
    import type { 
      SetStationDescriptionConfigStationStationIdDescriptionPutRequest, 
      GetStationConfigStationStationNoGetRequest 
    } from "./openapi_client";


    import {
    Button,
    Icon,
    Card,
    CardBody,
    CardHeader,
    CardTitle
  } from '@sveltestrap/sveltestrap';

  const do_the_thing = () => {
    console.log(import.meta.env)
    console.log(import.meta?.env?.DEV === true ? {basePath: "http://localhost:8000"} : {basePath: window.location.origin})
  }
</script>

<Card>
  <CardHeader>
    <CardTitle >Print Env<Icon name="sun-fill" /></CardTitle>
  </CardHeader>
  <CardBody>

    <Button
      color="primary"
      outline
      on:click={do_the_thing}
    >
      Click Button To Reveal Environment
      <Icon name="sun-fill" />
    </Button>
  </CardBody>
</Card>

