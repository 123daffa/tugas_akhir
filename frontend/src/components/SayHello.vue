<script setup>
import { reactive } from 'vue';

/* Kalau tipe data biasa pakai ref, karena ini array menggunakan reactive*/

const person = reactive({
    firstName : "",
    lastName : "",
})

function sayHello() {
    person.firstName = document.getElementById("firstName").value;
    person.lastName = document.getElementById("lastName").value;
}

/* Untuk mecegah template re-rendering ulang, bisa menggunakan compute 
const fullName = computed(() => {
    console.log('fullName called')
    return `${person.firstName} ${person.lastName}`;
})
Jika ingin mengetahui value sebelumnya, bisa ditambahkan parameter
const fullName = computed((oldName) => {
console.log(`Changed from ${oldName}`)
return `${person.firstName} ${person.lastName}`;
*/

function fullName () {
    console.log('fullName called')
    return `${person.firstName} ${person.lastName}`;
}

</script>

<template>
    <div>
        <input placeholder="First Name" type="text" id="firstName"> <br>
        <input placeholder="Last Name" type="text" id="lastName"> <br>
        <button v-on:click="sayHello">Say Hello</button>
    </div>
    <h1>Hello, {{ fullName() }}</h1>
    
</template>

<style scoped>

</style>