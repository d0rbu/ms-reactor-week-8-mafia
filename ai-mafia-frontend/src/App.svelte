<script>
  import * as Card from "$lib/components/ui/card";
  import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";
  import { Input } from "$lib/components/ui/input";
  import { onMount } from "svelte";

  let messages = [];

  onMount(() => {
    const socket = new WebSocket("ws://localhost:8080");
    socket.onmessage = (event) => {
      messages = [...messages, event.data];
    };
    
    // get initial messages
    fetch("http://localhost:8000/messages")
      .then((response) => response.json())
      .then((data) => {
        messages = data;
      })
      .then(() => {
        console.log(messages);
      });
  });
</script>

<main class="bg-slate-950 h-screen w-screen flex items-center justify-center flex-col">
  <div class="w-1/2 rounded-md bg-slate-900 p-4">
    <ScrollArea class="h-96">
      <Card.Root>
        <Card.Header>
          <Card.Title>Card Title</Card.Title>
          <Card.Description>Card Description</Card.Description>
        </Card.Header>
        <Card.Content>
          <p>Card Content</p>
        </Card.Content>
        <Card.Footer>
          <p>Card Footer</p>
        </Card.Footer>
      </Card.Root>
    </ScrollArea>
    <Input class="bg-slate-800 border-none text-white outline-none focus:outline-none" />
  </div>
</main>
