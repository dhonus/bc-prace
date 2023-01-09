<template>
  <div class="spinner" ref="spinner">
    <img src="@/assets/spinner.gif" alt="Spinner" />
  </div>
  <div class="home">
    <HelloWorld msg="Bc. Práce" />
    <div class="input_wrapper" @keyup.ctrl.enter.exact="submitWithKey" @keyup.shift.enter.exact="submitWithKeySteps">
      <div class="predicates">
        <div v-for="key in count" :key="key">
          <Transition>
            <input @focus="focusOnMe(key)" :rel="'predicate'+key" type="text" v-model="values['dynamic-field-'+key]" :placeholder="key+'. premisa'" :id="'predicate'+key" class="input-print">
          </Transition>
        </div>
        <div class="controls" style="justify-content: right; display: flex;">
          <button ref="buttonFour" class="button_plus" @click="addP" title="Přidat premisu">+</button>
          <button ref="buttonFour" class="button_plus" @click="removeP" title="Odebrat poslední premisu">-</button>
        </div>
        <input @focus="focusOnMe(-1)" ref="zaver" id="zaver" placeholder="Závěr" />
        <div class="button_container">
          <button class="accept_button" ref="accept_button" @click="submit(false)">
            <p style="flex:1; text-align: left; font-size: larger;">Vyhodnotit</p>
            <img style="color:white; height: 2rem; " src="../assets/control.svg">
            &nbsp;
            <img style="color:white; height: 2rem; " src="../assets/enter.svg">
          </button>
          <button style="flex:1;" class="accept_button" ref="step_button" @click="submit(true)">
            <p style="flex:1; text-align: left; font-size: larger;">Odkrokovat</p>
            <img style="color:white; height: 2rem; " src="../assets/shift.svg">
            &nbsp;
            <img style="color:white; height: 2rem; " src="../assets/enter.svg">
          </button>
        </div>

        <div class="why">
          <p v-if="APIErrorMessage.length > 0" style="color: #b01b1b;"><b> {{ APIErrorMessage }} </b></p>
          <span v-if="APIErrorMessage.length <= 0">
            <h3 v-if="validity === true" style="color:#129412;">Platný úsudek</h3>
            <h3 v-else-if="validity === false" style="color:#7e2626;">Neplatný úsudek</h3>
            <p>{{ Explanation }}</p>
          </span>
        </div>

        <div id="venn_one"></div>
        <div id="venn_two"></div>
        <div id="venn_three"></div>
        <div id="venn_four"></div>
        <div id="venn"></div>
        <div class="out-info">
          <h4>{{ logicResponseExistential }}</h4>
          <h4>{{ logicResponseUniversal }}</h4>
        </div>

        <div id="container">
        </div>
        <div class="print-wrapper">
          <div class="offset"></div>
          <div class="print-button" @click="printCanvas">
            <span class="download-text">Stáhnout</span>
            <img src="../assets/icons/iconmonstr-save-thin.svg" title="Tisk">
          </div>
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
              <td>Ω</td>
            </tr>
          </table>
          <p><b>Literál</b> má vždy tvar Cokoliv(proměnná), kdy proměnná je malé písmeno. Platné literály:</p>
          <ul>
            <li>P(x)</li>
            <li>Auto(y)</li>
          </ul>
          <p>Na vstupu mohou být premisy, nebo konstanty.</p>
          <p><b>Premisa</b> musí začínat kvantifikátorem a proměnnou na kterou se váže. Následující jsou platné premisy:</p>
          <ul>
            <li>∃x[A(x)]</li>
            <li>∀x[B(x)]</li>
            <li>∃xA(x) > B(x)</li>
            <li>∀x B(x) & C(x)</li>
            <li>AxB(x)</li>
          </ul>
          <p><b>Konstanty</b> se zapisují bez hranatých závorek:</p>
          <ul>
            <li>Q(a)</li>
            <li>P(x)</li>
          </ul>
          <h3>Příklad validního vstupu:</h3>
          <p>
            P1: ∀x A(x) > !B(x)<br>
            P2: Ex[A(x) > C(x)]<br>
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
      Explanation: '',
      containers: [null, null, null, null],
      container_names: ["#venn_one", "#venn_two", "#venn_three", "#venn_four"]
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
    printCanvas: function (){
      //const canvas = this.$refs.canvas;
      //const img    = canvas.toDataURL('image/png');
      //this.$refs.canvasExportImage.src = img;
      print();
    },
    // submits the form on ctrl + enter 
    submitWithKey: function(){
      this.$refs.accept_button.classList.add("activated");
      this.submit(false);
      setTimeout(() => {
        this.$refs.accept_button.classList.remove("activated");
      }, 250);
    },
    submitWithKeySteps: function() {
      this.$refs.step_button.classList.add("activated");
      this.submit(true);
      setTimeout(() => {
        this.$refs.step_button.classList.remove("activated");
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
    async submit(steps){

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

              // this is the message to the user!
              // the result reasoning is on the 0th position
              // if we cannot find it, we will display the last one
              if (response.data["explanations"][0] !== undefined){
                this.Explanation = String(response.data["explanations"][0]);
              }
              else{
                const max = Object.keys(response.data["explanations"]).length;
                console.log(max);
                this.Explanation = String(response.data["explanations"][max]);
              }

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
              let existential_sorted = {};
              // sort dict entries
              for (let [key, value] of Object.entries(response.data["existential"])) {
                console.log(key, value, "key value");
                for (let i = 0; i < value.length; i++) {
                  value[i].sort();
                }
                existential_sorted[key] = value.sort();
              }
              /*
              *
      //createApp with props
      createApp(VennVisualizer, {
        vennSize: 300,
      }).mount('#container')*/
              if (!steps) {
                this.resultVenn = createApp(VennVisualizer, {
                  vennSize: response.data["sets"].length,
                  sets: response.data["sets"].sort(),
                  predicates: response.data["predicates"],
                  explanations: response.data["explanations"],
                  // solutions
                  existential: existential_sorted,
                  universal: universal_sorted,
                });
                this.resultVenn.mount('#venn');
              } else {
                console.log(response.data["steps"]);
                // for each in steps
                let i = 1;
                for (const step of response.data["steps"]){
                  const container =
                  console.log(step);
                  if (this.containers[i] != null){
                    this.containers[i].unmount();
                  }
                  this.containers[i] = createApp(VennVisualizer, {
                    vennSize: step.sets.length,
                    sets: step.sets.sort(),
                    predicates: step.predicates,
                    explanations: step.explanations,
                    // solutions
                    existential: step.existential,
                    universal: step.universal,
                  });
                  this.containers[i].mount(this.container_names[i++]);
                }

              }


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
    setTimeout(() => this.$refs.spinner.style.display = "none", 0);
    //setTimeout(() => this.$refs.spinner.style.opacity = "0", 1000);
    //setTimeout(() => this.$refs.spinner.style.display = "none", 1300);
  },
}
</script>