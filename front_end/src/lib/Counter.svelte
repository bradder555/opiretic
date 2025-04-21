<script lang="ts">
    import { opiClient } from "./client";
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

 

  let count: number = $state(0)
  const increment = () => {
    count += 1
    opiClient.getStationConfigStationStationNoGet({stationNo: 1}).then(x => {console.log(x); return x.stationId})
      .then((sid) => {
        opiClient.setStationDescriptionConfigStationStationIdDescriptionPut({
          stationId: sid,
          desc: "Rose Garden"
        })
        return sid 
      }).then( (sid) => opiClient.getStationConfigStationStationNoGet({stationNo: sid}))
      .then(x => x.description)
  }
</script>

<Card>
  <CardHeader>
    <CardTitle >Card title <Icon name="sun-fill" /></CardTitle>
  </CardHeader>
  <CardBody>

    <Button
      color="primary"
      outline
      on:click={increment}
    >
      <Icon name="sun-fill" />
      count is {count}
    </Button>
  </CardBody>
</Card>

