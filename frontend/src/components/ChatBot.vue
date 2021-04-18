<template>
  <div class="chatbot">
    <div class="chatbot--colorbar"></div>
    <div class="chatbot--content" id="content">
      <div class="chatbot--content__logo">
        <p class="chatbot--content__logo-text">Powered by</p>
        <img src="../assets/logo.png" class="chatbot--content__logo-logo" />
      </div>
      <div class="chatbot--content__chat">
        <div class="chatbot--content__chat-content" v-for="message, i in chatContent" :key="i">
          <div class="chatbot--content__chat-message_bot" v-if="message.author === 'Chatbot'">
            <p :style="{ color: 'white' }">{{ message.body }}</p>
          </div>
          <div class="chatbot--content__chat-message_user" v-if="message.author === 'user'">
            <p :style="{ color: 'black' }">{{ message.body }}</p>
          </div>
          <div class="chatbot--content__chat-message_suggestion" v-if="message.author === 'suggestion'">
            <h3>Suggestions:</h3>
            <div v-for="link, i in message.body" :key="i">
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
      <div v-if="isWaiting" class="lds-ellipsis"><div></div><div></div><div></div><div></div></div>
      <div class="chatbot--input__div">
        <input class="chatbot--input__input" v-model="chatInput" placeholder="Enter your question here" />
        <div class="chatbot--input__button" @click="clickOnSend">
          <img src="../assets/send.png" class="chatbot--input__button-img" />
        </div>
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
    },
    isWaiting: false
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
      this.isWaiting = true
      this.scrollToBottom()
      try {
        const { data } = await backend.post('/send-question', {
          chatContent: this.chatContent
        })
        this.chatContent = [this.initMessage, ...data.data]
        this.scrollToBottom()
        this.isWaiting = false
      } catch (err) {
        console.error(`Something went wrong due to ${err}`)
        alert('Something went wrong!')
        this.isWaiting = false
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
    height: 40px
    background-color: #eee

    &__div
      display: flex
      position: absolute
      bottom: 8px
      width: calc(100% - 16px)

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
    height: 430px
    margin-bottom: 60px

    &__chat
      &-message
        &_user
          padding: 10px 15px 10px 15px
          margin-bottom: 10px
          background: linear-gradient(58deg, rgba(170,170,170,1) 0%, rgba(201,201,201,1) 100%)
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
          background: linear-gradient(140deg, rgba(22,153,153,1) 30%, rgba(56,195,214,1) 100%)
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

.lds-ellipsis
  display: inline-block
  position: absolute
  height: 10px
  width: 56px
  left: 50%
  transform: translateX(-70%)

.lds-ellipsis div 
  position: absolute
  top: 0px
  width: 5px
  height: 5px
  border-radius: 50%
  background: #444
  animation-timing-function: cubic-bezier(0, 1, 1, 0)

.lds-ellipsis div:nth-child(1)
  left: 8px
  animation: lds-ellipsis1 1s infinite

.lds-ellipsis div:nth-child(2)
  left: 8px
  animation: lds-ellipsis2 1s infinite

.lds-ellipsis div:nth-child(3)
  left: 32px
  animation: lds-ellipsis2 1s infinite

.lds-ellipsis div:nth-child(4)
  left: 56px
  animation: lds-ellipsis3 1s infinite

@keyframes lds-ellipsis1
  0%
    transform: scale(0)
  100%
    transform: scale(1)

@keyframes lds-ellipsis3
  0%
    transform: scale(1)
  100%
    transform: scale(0)

@keyframes lds-ellipsis2
  0%
    transform: translate(0, 0)
  100%
    transform: translate(24px, 0)

</style>
