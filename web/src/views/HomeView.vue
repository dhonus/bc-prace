<template>
  <div class="home">
    <p>This is code from Vue</p>
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <div class="input_wrapper">
      <div class="predicates">
        <p>Error message: {{ message }}</p>
        <input v-model="message" placeholder="1. premisa" />
        <input v-model="message2" placeholder="2. premisa" />
        <div class="button_container">
          <input style="flex:1" v-model="message3" placeholder="3. premisa" />
          <button ref="buttonFour" class="button_plus" @click="optionalPredicate = !optionalPredicate; togg()">+</button>
        </div>
        <Transition>
          <input v-if="optionalPredicate" v-model="message4" placeholder="4. premisa" />
        </Transition>
        <input v-model="message" placeholder="Závěr" />
        <button class="accept_button" >Vyhodnotit</button>
      </div>
      <div class="keyboard">
        <button>⊃</button>
        <button>≡</button>
        <button>¬</button>
        <button>∧</button>
        <button>∨</button>
        <button>(</button>
        <button>∀</button>
        <button>∃</button>
        <button>)</button>
      </div>
    </div>


  </div>
</template>


<script>
// @ is an alias to /src
import HelloWorld from '@/components/home.vue'


export default {
  name: 'HomeView',
  components: {
    HelloWorld
  },
  data() {
    return {
      optionalPredicate:false
    }
  },
  methods: {
    togg(){
      if (this.$refs.buttonFour.innerText == '+'){
        this.$refs.buttonFour.innerText = "-";
      }
      else {
        this.$refs.buttonFour.innerText = "+";
      }

    },
  }
}
</script>
