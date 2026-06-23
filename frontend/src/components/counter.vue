<script setup>
import { ref } from 'vue';

console.info('Load Component')
let counter = ref({
    count : 0,
    name : 'Eka'
});

function increment() {
    console.info(`Increment Counter : ${counter.value.count}`);
    counter.value = {
        name : counter.value.name,
        count : counter.value.count + 1
    }
}

function decrement() {
    console.info(`Decrement Counter : ${counter.value.count}`);
    counter.value = {
        name : counter.value.name,
        count : counter.value.count - 1
    };
}

function reset() {
    console.info(`Reset Counter : ${counter.value.count}`);
    counter.value = {
        name : counter.value.name,
        count : 0
    };

/*
Bisa menggunakan asyn juga di vue, dan promise diganti dengan await
async function increment() {
    console.info(`Increment Counter : ${counter.value.count}`);
    counter.value = {
        name : counter.value.name,
        count : counter.value.count + 1
    }
}

counter.value.count++

await nextTick(); // untuk menunggu update selesai

console.log('increment count after nextTick')

*/    
}
</script>

<template>
    <div>
        <h1 id="counter">Counter {{ counter.name }}: {{ counter.count }}</h1>
        <button v-on:click="increment">Increment</button>
        <button v-on:click="decrement">Decrement</button>
        <button v-on:click="reset">Reset</button>
    </div>
</template>

<style>

</style>