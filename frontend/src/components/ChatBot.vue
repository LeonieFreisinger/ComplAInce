<template>
  <div class="chatbot">
    <div class="chatbot--colorbar"></div>
    <div class="chatbot--content" id="content">
      <div class="chatbot--content__logo">
        <p class="chatbot--content__logo-text">Powered by</p>
        <img src="../assets/logo.png" class="chatbot--content__logo-logo" />
      </div>
      <div class="chatbot--content__chat">
        <div class="chatbot--content__chat-content" v-for="message in chatContent" :key="Number(message.timestamp)">
          <div class="chatbot--content__chat-message_bot" v-if="message.author === 'Chatbot'">
            <p :style="{ color: 'white' }">{{ message.body }}</p>
          </div>
          <div class="chatbot--content__chat-message_user" v-if="message.author === 'user'">
            <p :style="{ color: 'black' }">{{ message.body }}</p>
          </div>
          <div class="chatbot--content__chat-message_suggestion" v-if="message.author === 'suggestion'">
            <h3>Suggestions:</h3>
            <div v-for="link in message.body" :key="link.link">
              <div class="horizontal-line"></div>
              <p :style="{ color: 'black' }">
                I want to know more about
                <a :href="link.link" target="_blank" :style="{ 'text-decoration': 'solid', 'color': '#169999', 'font-weight': 700 }">{{ link.link_text }}</a>
              </p>
            </div>
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
    chatContent: [],
    initMessage: {
      author: 'Chatbot',
      timestamp: new Date(),
      body: 'Hi! I am your personal compliance expert. How can I help you?'
    }
  }),
  props: {
    msg: String
  },
  methods: {
    async clickOnSend() {
      if (this.chatInput === '') {
        return
      }
      this.chatContent.push({
        body: this.chatInput,
        author: 'user',
        timestamp: new Date()
      })
      this.chatInput = ''
      this.scrollToBottom()
      try {
        const { data } = await backend.post('/send-question', {
          chatContent: this.chatContent
        })
        this.chatContent = [this.initMessage, ...data.data]
        this.scrollToBottom()
      } catch (err) {
        console.error(`Something went wrong due to ${err}`)
      }
    },
    scrollToBottom() {
      setTimeout(() => {
        const container = this.$el.querySelector("#content")
        container.scrollTop = container.scrollHeight
      }, 100)

    }
  },
  mounted() {
    setTimeout(() => this.chatContent.push(this.initMessage), 500)
  }
}
</script>

<style lang="sass" scoped>
p
  color: #777
  font-weight: 300
  font-size: 0.9rem
  margin-top: 0.5rem
  margin-bottom: 0.5rem

.horizontal-line
  background-color: #ddd
  height: 1px

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

    &__input
      flex: 9
      height: 25px
      border-color: transparent
      border-radius: 20px 0 0 20px
      font-size: 0.9rem
      padding-left: 10px
      &:focus
        outline: none

    &__button
      height: 31px
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

  &--content
    padding: 8px
    overflow: scroll
    height: 450px
    margin-bottom: 30px

    &__chat
      &-message
        &_user
          padding: 10px 15px 10px 15px
          margin-bottom: 10px
          background-color: #aaa
          border-radius: 20px 0 20px 20px
          width: 85%
          margin-left: 4%
          -webkit-animation: fadein 1s

        &_suggestion
          padding: 10px 10px 10px 10px
          margin-bottom: 10px
          background-color: white
          color: black
          border-radius: 5px
          -webkit-animation: fadein 1s

          h3
            font-size: 1rem
            font-weight: 500
            margin-top: 0.5rem
            margin-bottom: 0.5rem

        &_bot
          padding: 10px 15px 10px 15px
          margin-bottom: 10px
          background-color: #169999
          border-radius: 0 20px 20px 20px
          width: 85%
          -webkit-animation: fadein 1s

    &__logo
      height: 25vh
      width: 100%
      position: relative
      margin-top: 10%
      -webkit-animation: fadein 1s

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

@keyframes fadein
  from
    opacity: 0
  to
    opacity: 1
</style>
