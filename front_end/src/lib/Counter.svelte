<script lang="ts">
    import { opiClient } from "./client";

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
    opiClient.getFullConfigConfigGet().then(console.log)
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

