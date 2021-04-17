<template>
  <div class="chatbot">
    <div class="chatbot--colorbar"></div>
    <div class="chatbot--content">
      <div class="chatbot--content__logo">
        <p class="chatbot--content__logo-text">Powered by</p>
        <img src="../assets/logo.png" class="chatbot--content__logo-logo" />
      </div>
      <div class="chatbot--content__chat" id="chat">
        <div class="chatbot--content__chat-content" v-for="message in chatContent" :key="Number(message.timestamp)">
          <div class="chatbot--content__chat-message" v-if="message.author === 'Chatbot'" :style="{ 'background-color': '#169999', 'border-radius': '0 20px 20px 20px', 'width': '85%' }">
            <p :style="{ color: 'white' }">{{ message.body }}</p>
          </div>
          <div class="chatbot--content__chat-message" v-if="message.author === 'user'" :style="{ 'background-color': '#aaa', 'border-radius': '20px 0 20px 20px', 'width': '85%', 'margin-left': '9%' }">
            <p :style="{ color: 'white' }">{{ message.body }}</p>
          </div>
        </div>
      </div>
    </div>
    <div class="chatbot--input">
      <input class="chatbot--input__input" v-model="chatInput" placeholder="Enter your question here" />
      <div class="chatbot--input__button" @click="clickOnSend">
        <img src="../assets/send.png" class="chatbot--input__button-img" />
      </div>
    </div>
  </div>
</template>

<script>
import { backend } from '@/utils'

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
      if (this.chatInput === '') {
        return
      }
      const userMessage = this.chatInput
      this.addMessage({
        body: this.chatInput,
        author: 'user',
        timestamp: new Date()
      })
      this.chatInput = ''
      try {
        const { data } = await backend.post('/send-question', {
          question: userMessage
        })
        const { answer } = data
        this.addMessage({
          body: answer,
          author: 'Chatbot',
          timestamp: new Date()
        })
      } catch (err) {
        console.error(`Something went wrong due to ${err}`)
      }
    },
    addMessage(content) {
      this.chatContent.push(content)
      const element = document.getElementById('chat')
      element.scrollTop = element.scrollHeight
      console.log(element.scrollTop)
    }
  },
  mounted() {
    setTimeout(() => this.chatContent.push({
      author: 'Chatbot',
      timestamp: new Date(),
      body: 'Hi! I am your personal compliance expert. How can I help you?'
    }), 1000)
  }
}
</script>

<style lang="sass" scoped>
p
  color: #777
  font-weight: 300
  font-size: 0.9rem

.chatbot
  margin: -8px
  width: 300px
  height: 500px
  position: relative

  &--colorbar
    height: 10px
    width: 100%
    background-color: #169999

  &--input
    position: fixed
    padding: 8px
    bottom: 0
    width: calc(100% - 16px)
    display: flex
    height: 30px
    background-color: #eee

    &__button
      height: 26px
      flex: 1
      background-color: white
      border-radius: 0 20px 20px 0
      position: relative

      &-img
        height: 16px
        position: absolute
        left: 50%
        top: 50%
        transform: translate(-50%, -50%)
        cursor: pointer

    &__input
      flex: 9
      height: 20px
      border-color: transparent
      border-radius: 20px 0 0 20px
      &:focus
        outline: none

  &--content
    padding: 8px

    &__logo
      height: 25vh
      width: 100%
      position: relative
      margin-top: 10%

      &-logo
        height: 70%
        position: absolute
        left: 50%
        top: 0
        transform: translateX(-50%)

      &-text
        width: 100%
        text-align: center
        font-size: 0.8rem

    &__chat
      overflow: scroll
      height: 300px
      margin-bottom: 30px

      &-message
        padding: 10px 15px 10px 15px
        margin-bottom: 10px
</style>
