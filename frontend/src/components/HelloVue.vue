<script setup>
console.info('Hello Vue');

const hello = '<h1>Hello Vue</h1>';
const buttondisabled = false;
const data = {
    id: 'hello',
    class: 'hello',
}


</script>

<template>
    <h1  v-bind="data">{{ hello }}</h1>
    <div :class="data.class" v-html="hello"></div>
    <button :disabled="buttondisabled">This is button</button>

    
</template>

<style scoped>
.hello {
    color: green;
}
</style>