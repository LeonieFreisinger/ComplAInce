<template lang="pug">
  #app
    chat-bot
</template>

<script>
import ChatBot from './components/ChatBot.vue'

export default {
  name: 'App',
  components: {
    "chat-bot": ChatBot
  }
}
</script>

<style lang="sass">
#app
  font-family: Avenir, Helvetica, Arial, sans-serif
  -webkit-font-smoothing: antialiased
  -moz-osx-font-smoothing: grayscale
  color: #2c3e50
  margin-top: 60px
</style>
