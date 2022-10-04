<template>
  <div class="home">
    <HelloWorld msg="Bc. Práce"/>
    <div class="input_wrapper" @keyup.ctrl.enter="submit">
      <div class="predicates">
        <div v-for="key in count" :key="key">
          <Transition>
            <input @focus="focusOnMe(key)" :rel="'predicate'+key" type="text" v-model="values['dynamic-field-'+key]" :placeholder="key+'. Predikát'" :id="'predicate'+key" >
          </Transition>
        </div>
        <input ref="zaver" placeholder="Závěr" />
        <div class="button_container">
          <button style="padding:0 1em; box-sizing: border-box; flex:1; display: flex; justify-content: left; align-items: center;" class="accept_button" @click="submit">
            <p style="flex:1; text-align: left; font-size: larger;">Vyhodnotit</p>
            <img style="color:white; height: 2rem; " src="../assets/control.svg">
            &nbsp;
            <img style="color:white; height: 2rem; " src="../assets/enter.svg">
          </button>
          <button ref="buttonFour" class="button_plus" @click="addP" title="Přidat predikát">+</button>
          <button ref="buttonFour" class="button_plus" @click="removeP" title="Odebrat poslední predikát">-</button>
        </div>

        <p style="color: #b01b1b;"><b> {{ APIErrorMessage }} </b></p>
        <p>{{ logicResponseExistential }}</p>
        <p>{{ logicResponseUniversal }}</p>

      </div>
      <div class="left_section">
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
        <div class="guide">
          <p>Následuje tabulka podporovaných symbolů<br> včetně jejich akceptovatelných variant.</p>
          <table>
            <tr>
              <td>Implikace</td>
              <td>⊃</td>
              <td>&gt;</td>
            </tr>
            <tr>
              <td>Ekvivalence</td>
              <td>⊃</td>
              <td>&lt;&gt;</td>
            </tr>
            <tr>
              <td>Negace</td>
              <td>¬</td>
              <td>!</td>
            </tr>
            <tr>
              <td>Konjunkce</td>
              <td>∧</td>
              <td>&</td>
            </tr>
            <tr>
              <td>Disjunkce</td>
              <td>∨</td>
              <td>|</td>
            </tr>
            <tr>
              <td>Existenční kvantifikátor</td>
              <td>∃</td>
              <td>E</td>
            </tr>
            <tr>
              <td>Univerzální kvantifikátor</td>
              <td>∀</td>
              <td>A</td>
            </tr>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
// @ is an alias to /src
import HelloWorld from '@/components/home.vue'
import axios from "axios";
import qs from "qs";


export default {
  name: 'HomeView',
  components: {
    HelloWorld
  },
  data() {
    return {
      optionalPredicate:false,
      count: 3,
      values: {},
      focused: null,
      zaver: null,
      APIErrorMessage: '',
      logicResponseExistential: '',
      logicResponseUniversal: '',
    }
  },
  methods: {
    focusOnMe: function(key){
      this.focused = key;
      this.focused = document.getElementById("predicate"+key);
    },
    keyboard: function(value_to_enter){
      if (!this.focused){
        return;
      }
      this.focused.value = this.focused.value + value_to_enter;
    },
    addP: function(){
      if (this.count < 4)
        this.count++;
    },
    removeP: function(){
      if (this.count > 1)
      this.count--;
    },
    remove: function () {
      this.count--;

    },
    async submit(){
      let predicates = []
      for (var key of Object.keys(this.values)) {
        console.log(key + " -> " + this.values[key]);
        if (this.values[key].length !== 0)
        predicates.push(this.values[key]);
      }

      /*let predicates = [
        "∀x[A(x) > !B(x)]",
        "∀x[A(x) > !B(x)]"
      ];*/
      //let conclusion = "∃x[C(x)]"

      let conclusion = this.$refs.zaver.value;
      let formdata = new FormData();
      formdata.append('conclusion', JSON.stringify(conclusion))
      formdata.append('predicates',JSON.stringify(predicates));
      try {
        axios.post('/api', {
            conclusion: conclusion,
            predicates: predicates,
          paramsSerializer: params => {
            return qs.stringify(params)
          }
        })
        .then((response) => {
          console.log(response);
          if (response.data['notes'] !== "OK")
            this.APIErrorMessage = response.data['notes'];
          else{
            this.APIErrorMessage = "";
          }
          this.logicResponseExistential = 'Existenční: ' + response.data["existential"];
          this.logicResponseUniversal = 'Univerzální (vyšrafované oblasti): ' + response.data["universal"];
        }, (error) => {
          console.log(error);
        });
      } catch (err) {
        // uh oh, didn't work, time for plan B
      }
    },
    togg: function(){
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
