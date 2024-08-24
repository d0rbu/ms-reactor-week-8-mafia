<script>
  import * as Card from "$lib/components/ui/card";
  import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";
  import { Input } from "$lib/components/ui/input";
  import { onMount } from "svelte";

  let messages = ["Hello", "World"];

  onMount(() => {
    const socket = new WebSocket("ws://localhost:8000/ws");
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
    <ScrollArea class="h-96 border border-blue-400 p-2">
      <!-- Div containing two columns, on the left are the messages recieved, and on the right are messages sent -->
      <div class="flex flex-col space-y-2 border border-green-400 p-4">
        {#each messages as message}
          <div class="flex justify-start border border-border-3 border-red-400 pr-32">
            <Card.Root class="border border-green-300 w-full p-2">
              <Card.Header>
                <Card.Title>Card Title</Card.Title>
                <Card.Description>Card Description</Card.Description>
              </Card.Header>
              <Card.Content>
                <p>{message}</p>
              </Card.Content>
              <Card.Footer>
                <p>Card Footer</p>
              </Card.Footer>
            </Card.Root>
          </div>
        {/each}
        {#each messages as message}
        <div class="flex justify-end border border-border-3 border-yellow-400 pl-32 p-2">
          <Card.Root class="border border-green-300 w-full">
            <Card.Header>
              <Card.Title>Card Title</Card.Title>
              <Card.Description>Card Description</Card.Description>
            </Card.Header>
            <Card.Content>
              <p>{message}</p>
            </Card.Content>
            <Card.Footer>
              <p>Card Footer</p>
            </Card.Footer>
          </Card.Root>
        </div>
      {/each}
      </div>
      <!-- <Card.Root class="border border-red-300">
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
      </Card.Root> -->
      
    </ScrollArea>
    <Input class="bg-slate-800 border-none text-white outline-none focus:outline-none" />
  </div>
</main>
