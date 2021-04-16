<template lang="pug">
  .chatbot
    .chatbot--chat__content
      p(v-for="message in chatContent") {{ message.body }}
    input(v-model="chatInput")
    button(@click="clickOnSend") Send
</template>

<script>
import { backend } from '../utils'

export default {
  name: 'ChatBot',
  data: () => ({
    chatInput: '',
    chatContent: []
  }),
  props: {
    msg: String
  },
  methods: {
    async clickOnSend() {
      const userMessage = this.chatInput
      this.chatContent.push({
        body: this.chatInput,
        author: 'user',
        timestamp: new Date()
      })
      this.chatInput = ''
      try {
        const res = await backend.post('/send-question', {
          question: userMessage
        })
        console.log(res)
      } catch (err) {
        console.error(`Something went wrong due to ${err}`)
      }
    }
  }
}
</script>

<style lang="sass" scoped>
.chatbot
  margin: 10% 0 0 10%
</style>
