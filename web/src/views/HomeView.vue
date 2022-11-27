<template>
  <div class="spinner" ref="spinner">
    <img src="@/assets/spinner.gif" alt="Spinner" />
  </div>
  <div class="home">
    <HelloWorld msg="Bc. Práce"/>
    <div class="input_wrapper" @keyup.ctrl.enter="submitWithKey">
      <div class="predicates">
        <div v-for="key in count" :key="key">
          <Transition>
            <input @focus="focusOnMe(key)" :rel="'predicate'+key" type="text" v-model="values['dynamic-field-'+key]" :placeholder="key+'. premisa'" :id="'predicate'+key" >
          </Transition>
        </div>
        <div class="controls" style="justify-content: right; display: flex;">
          <button ref="buttonFour" class="button_plus" @click="addP" title="Přidat premisu">+</button>
          <button ref="buttonFour" class="button_plus" @click="removeP" title="Odebrat poslední premisu">-</button>
        </div>
        <input @focus="focusOnMe(-1)" ref="zaver" id="zaver" placeholder="Závěr" />
        <div class="button_container">
          <button style="padding:0 1em; box-sizing: border-box; flex:1; display: flex; justify-content: left; align-items: center;" class="accept_button" ref="accept_button" @click="submit">
            <p style="flex:1; text-align: left; font-size: larger;">Vyhodnotit</p>
            <img style="color:white; height: 2rem; " src="../assets/control.svg">
            &nbsp;
            <img style="color:white; height: 2rem; " src="../assets/enter.svg">
          </button>
        </div>

        <p style="color: #b01b1b;"><b> {{ APIErrorMessage }} </b></p>
        <h4>{{ logicResponseExistential }}</h4>
        <h4>{{ logicResponseUniversal }}</h4>
        <h4 v-if="validity === true" style="color:#129412;">Platný úsudek</h4>
        <h4 v-else-if="validity === false" style="color:#7e2626;">Neplatný úsudek</h4>

        <div id="venn">
        </div>

        <div id="container">
        </div>

      </div>
      <div class="left_section">
        <div class="keyboard">
          <button @click="type('⊃')" rel="">⊃</button>
          <button @click="type('≡')" rel="">≡</button>
          <button @click="type('¬')" rel="">¬</button>
          <button @click="type('∧')" rel="">∧</button>
          <button @click="type('∨')" rel="">∨</button>
          <button @click="type('[')" rel="">[</button>
          <button @click="type('∀')" rel="">∀</button>
          <button @click="type('∃')" rel="">∃</button>
          <button @click="type(']')" rel="">]</button>
        </div>
        <div class="guide">
          <p>Následuje tabulka <b>podporovaných symbolů</b><br> včetně jejich <b>akceptovatelných variant</b>.</p>
          <table>
            <tr>
              <td>Implikace</td>
              <td>⊃</td>
              <td>&gt;</td>
            </tr>
            <tr>
              <td>Ekvivalence</td>
              <td>≡</td>
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
            <tr>
              <td>Universum diskursu</td>
              <td></td>
              <td>μ</td>
            </tr>
          </table>

          <p>Premisa musí být ohraničena <b>hranatými závorkami</b> a musí začínat kvantifikátorem a proměnnou:
            <br>&nbsp;&nbsp;&nbsp;<b>∃x[A(x)]</b>
            <br>&nbsp;&nbsp;&nbsp;<b>∀x[B(x)]</b></p>
          <p><b>Konstanty</b> se zapisují bez hranatých závorek: <br><b>&nbsp;&nbsp;&nbsp;Q(a)<br>&nbsp;&nbsp;&nbsp;P(x)</b></p>

          <h3>Příklad validního vstupu:</h3>
          <p>
            P1: ∀x[A(x) > !B(x)]<br>
            P2: ∀x[A(x) > B(x)]<br>
          </p>
          <hr>
          <p>
            Z: ∃x[C(x)]
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/home.vue';
import axios from "axios";
import qs from "qs";
import VennVisualizer from "@/components/venn-visualize";
import { createApp } from 'vue'


export default {
  name: 'HomeView',
  components: {
    HelloWorld,
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
      validity: null,
      myChart: null,
      resultVenn: null,
    }
  },
  methods: {
    // sets the active input field to the one that was clicked on
    focusOnMe: function(key){
      this.focused = key;
      if(key === -1){
        this.focused = document.getElementById("zaver");
        return;
      }
      this.focused = document.getElementById("predicate"+key);
    },
    // adds a new input field 
    addP: function(){
      if (this.count < 4)
        this.count++;
    },
    // removes the last input field
    removeP: function(){
      if (this.count > 1)
      this.count--;
    },
    remove: function () {
      this.count--;
    },
    // submits the form on ctrl + enter 
    submitWithKey: function(){
      this.$refs.accept_button.classList.add("activated");
      this.submit();
      setTimeout(() => {
        this.$refs.accept_button.classList.remove("activated");
      }, 250);

    },
    // adds the symbol from the virtual keyboard to the active input field
    type: function(value_to_enter){
      if (!this.focused){
        return;
      }
      const [start, end] = [this.focused.selectionStart, this.focused.selectionEnd];
      this.focused.setRangeText(value_to_enter, start, end, 'end');
      this.focused.setSelectionRange(end+1,end+1);
      this.focused.focus();
      this.focused.dispatchEvent(new Event('input')); // this is done because vue doesnt detect changes without an event
    },
    // submits the form and requests the data from the API
    async submit(){

      //createApp with props
      /*createApp(VennVisualizer, {
        vennSize: 300,
      }).mount('#container')
*/


      let predicates = []
      for (var key of Object.keys(this.values)) {
        console.log(key + " -> " + this.values[key]);
        if (this.values[key].length !== 0)
        predicates.push(this.values[key]);
      }

      let conclusion = this.$refs.zaver.value;
      let formdata = new FormData();
      formdata.append('conclusion', JSON.stringify(conclusion))
      formdata.append('predicates',JSON.stringify(predicates));
      /*
      axios.post('/api', {
            conclusion: conclusion,
            predicates: predicates,
          paramsSerializer: params => {
            return qs.stringify(params)
          }
      */
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
          this.logicResponseExistential = "Existenciální: "
          //response.data["existential"].forEach(appendExistential);
          for (const [key, value] of Object.entries(response.data["existential"])) {
            console.log(key, value);
            this.logicResponseExistential += key + " -> ";
            for (const val of value){
              this.logicResponseExistential += val + ", ";
            }
            this.logicResponseExistential += "\n";
          }

          this.logicResponseUniversal = 'Univerzální (vyšrafované oblasti): ' + response.data["universal"];
          this.validity = response.data["valid"];

          let theData = []
          for (const element of response.data["sets"]) {
            theData.push({ label: String(element), values: []})
          }

          console.log(theData, "thedata");
          console.log([
            { label: 'A', values: [] },
            { label: 'B', values: [] },
            { label: 'C', values: [] },
          ]);

          if (this.resultVenn != null){
            this.resultVenn.unmount();
          }
          let universal_sorted = response.data["universal"];
          // sort every array inside this.universal alphabetically
          for (let i = 0; i < universal_sorted.length; i++) {
            universal_sorted[i].sort();
          }

          this.resultVenn = createApp(VennVisualizer, {
            vennSize: response.data["sets"].length,
            sets: response.data["sets"],
            predicates: response.data["predicates"],
            explanations: response.data["explanations"],
            // solutions
            existential: response.data["existential"],
            universal: universal_sorted,
          });
          this.resultVenn.mount('#venn');


        }, (error) => {
          console.log(error);
        });
      } catch (err) {
        // uh oh, didn't work, time for plan B
      }


    },
    togg: function(){
      if (this.$refs.buttonFour.innerText === '+'){
        this.$refs.buttonFour.innerText = "-";
      }
      else {
        this.$refs.buttonFour.innerText = "+";
      }

    },
    makeChart() {

    },
  },
  mounted: function() {
    console.log("Mounted!")
    document.getElementById("predicate1").focus();
    setTimeout(() => this.$refs.spinner.style.display = "none", 1000);
  },
}
</script>