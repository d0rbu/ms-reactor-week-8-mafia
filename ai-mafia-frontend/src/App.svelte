<script>
  import * as Card from "$lib/components/ui/card";
  import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";
  import { Input } from "$lib/components/ui/input";
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import logo from './assets/logo.svg';

  import {
    Button,
    buttonVariants
  } from "$lib/components/ui/button/index.js";
  import * as Dialog from "$lib/components/ui/dialog/index.js";
  import { Label } from "$lib/components/ui/label/index.js";

  let gameOver = writable(false);
  let messages = writable([]);
  let socket = null;
  let value = "";

  onMount(() => {
    socket = new WebSocket("ws://10.104.150.35:8000/ws");
    socket.onmessage = (event) => {
      messages.update((messages) => [...messages, JSON.parse(event.data)]);

      // scroll down
      const scrollArea = document.getElementById("scroll-area");
      scrollArea.scrollTop = scrollArea.scrollHeight;
    };
    
    // get initial messages
    fetch("http://10.104.150.35:8000/messages")
      .then((response) => response.json())
      .then((data) => {
        messages.set(data);
      });
  });
</script>

<main class="bg-slate-950 h-screen w-screen flex items-center justify-center flex-col">
  <img src={logo} class="h-64 -my-24" alt="logo">
  <h2 class="text-white text-xl mt-16 mb-6 bold">Auto-Mafioso</h2>
  <div class="w-1/2 rounded-md bg-slate-900 pt-4 space-y-6">
    <ScrollArea class="h-96 px-4 my-2" id="scroll-area">
      <!-- Div containing two columns, on the left are the messages recieved, and on the right are messages sent -->
      <div class="flex flex-col space-y-2">
        {#each $messages as message}
          {#if message.content != "NO_RESPONSE"}
            <div class="flex {(message.user === 'system') ? '' : ((message.user === 'user') ? 'justify-end' : 'justify-start')}">
              <Card.Root class="p-2 bg-{message.color}-800 rounded-lg border-none text-white">
                <Card.Description class="text-slate-300">{message.user === 'user' ? 'You' : message.user}</Card.Description>
                <p class="{(message.user === 'user') ? "text-right" : "text-left" }">
                  {message.content}
                </p>
              </Card.Root>
            </div>
          {/if}
        {/each}
      </div>
    </ScrollArea>
    <form class="mx-4 my-auto" on:submit={(e) => {
      e.preventDefault();
      const latest_message = {
        user: "user",
        content: value,
        color: "blue",
      }
      messages.update((messages) => [...messages, latest_message]);
      value = "";

      const scrollArea = document.getElementById("scroll-area");
      scrollArea.scrollTop = scrollArea.scrollHeight;

      socket.send(JSON.stringify(latest_message));
    }}>
      <Input class="bg-slate-800 border-none text-white outline-none focus:outline-none" disabled={$gameOver} bind:value={value} />
    </form>
    <div class="bg-red-800" />
    <div class="bg-orange-800" />
    <div class="bg-yellow-800" />
    <div class="bg-green-800" />
    <div class="bg-blue-800" />
    <div class="bg-indigo-800" />
    <div class="bg-purple-800" />
    <div class="bg-violet-800" />
    <div class="bg-rose-800" />
    <div class="bg-sky-800" />
    <div class="bg-fuchsia-800" />
  </div>
  
  <div class="w-1/2 p-2 mt-8 -mb-16">
    <h2 class="text-white text-center text-lg">Who is the Mafioso?</h2>
    <div class="w-full flex justify-center mt-2">
    
      <div class="flex flex-col m-2 mx-4">
        <h4 class="text-white text-md text-center">Heidi</h4>
        <form on:submit={(e) => {
          e.preventDefault();
          gameOver.set(true);
          fetch("http://10.104.150.35:8000/guess/Heidi")
            .then((response) => response.json())
            .then((data) => {
              messages.update((messages) => [...messages, data]);
              socket.send("GAME_OVER");
            });
        }}>
          <Button type="submit" class="w-12" disabled={$gameOver}>Vote</Button>
        </form>
        
      </div>
  
      <div class="flex flex-col m-2 mx-4">
        <h4 class="text-white text-md text-center">Vincent</h4>
        <form on:submit={(e) => {
          e.preventDefault();
          gameOver.set(true);
          fetch("http://10.104.150.35:8000/guess/Vincent")
            .then((response) => response.json())
            .then((data) => {
              messages.update((messages) => [...messages, data]);
              socket.send("GAME_OVER");
            });
        }}>
          <Button type="submit" class="w-12" disabled={$gameOver}>Vote</Button>
        </form>
      </div>
  
      <div class="flex flex-col m-2 mx-4">
        <h4 class="text-white text-md text-center">Isabella</h4>
        <form on:submit={(e) => {
          e.preventDefault();
          gameOver.set(true);
          fetch("http://10.104.150.35:8000/guess/Isabella")
            .then((response) => response.json())
            .then((data) => {
              messages.update((messages) => [...messages, data]);
              socket.send("GAME_OVER");
            });
        }}>
          <Button type="submit" class="w-12" disabled={$gameOver}>Vote</Button>
        </form>
      </div>
    </div>
  </div>
</main>
