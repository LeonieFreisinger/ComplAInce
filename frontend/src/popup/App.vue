<template>
  <chat-bot />
</template>

<script>
import ChatBot from '@/components/ChatBot.vue'

export default {
  name: 'App',
  components: { ChatBot }
}
</script>

<style lang="sass">
html
  font-family: Helvetica
  width: 300px
  height: 500px
  background-color: #eee
</style>
