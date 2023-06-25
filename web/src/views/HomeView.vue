<template>
  <HelpHome v-if="help" @close="showHelp"/>
  <div class="spinner" ref="spinner">
    <img src="@/assets/spinner.gif" alt="Spinner" />
  </div>
  <div class="home">
    <div class="tablinks">
      <div class="col">
        <div class="single">
          <a href="/">
            <button class="tab active">Vyřešit</button>
          </a>
        </div>
        <div class="single">
          <a href="/validate">
          <button class="tab">Zkontrolovat</button>
          </a>
        </div>
      </div>
      <div class="col">
        <div class="help-button" @click="showHelp">
            <span class="download-text">Nápověda</span>
            <img src="../assets/icons/iconmonstr-question-thin.svg" title="Nápověda">
          </div>
      </div>
    </div>
    <HelloWorld msg="Bc. Práce" />
    <div class="input_wrapper" @keyup.ctrl.enter.exact="submitWithKey" @keyup.shift.enter.exact="submitWithKeySteps">
      <div class="predicates bubble">
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
        <div style="height: 1px; background: #dddde0; margin: 1rem auto auto auto; width: 90%;"></div>
        <div class="why" ref="why">
          <p v-if="APIErrorMessage.length > 0" style="color: #b01b1b;"><b> {{ APIErrorMessage }} </b></p>
          <span v-if="APIErrorMessage.length <= 0">
            <h3 v-if="validity === true" style="color:#129412;">Platný úsudek</h3>
            <h3 v-else-if="validity === false" style="color:#7e2626;">Neplatný úsudek</h3>
            <p>{{ Explanation }}</p>
          </span>
        </div>
        <div class="steps" ref="steps">
          <div id="venn_one"></div>
          <div id="venn_two"></div>
          <div id="venn_three"></div>
          <div id="venn_four"></div>
          <div id="venn_five"></div>
          <div id="venn_six"></div>
          <div id="venn"></div>
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
      <div class="left_section bubble">
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
          <p>Následuje tabulka <b>podporovaných symbolů</b> a jejich <b>povolených variant</b>. Tyto symboly <br>mohou být libovolně kombinovány.</p>
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
          <blockquote><p>Na vstupu mohou být uzavřené formule s právě jednou proměnnou nebo konstantou.</p></blockquote>
          <p><b>Premisa</b> se skládá z <b>literálů</b> a musí začínat kvantifikátorem a proměnnou, na kterou se váže. Musí být také <b>uzavřena hranatými závorkami</b>. Následující jsou platné premisy:</p>
          <ul>
            <li>∃x[A(x)]</li>
            <li>∀x[B(x)]</li>
            <li>∃x [A(x) & B(x)]</li>
            <li>∀x [B(x) ⊃ C(x)]</li>
          </ul>
            <p><b>Literál</b> je vždy ve tvaru atomické formule, nebo její negace → <span style="background: #ececec; padding: 0 .3rem; border-radius: 7px;">Predikát(proměnná)</span>, kde proměnná je malé písmeno. Platné literály:</p>
          <ul>
            <li>P(x)</li>
            <li>¬Venn(x)</li>
            <li>Q(y)</li>
          </ul>
            <p>
                Premisa může alternativně obsahovat <b>konstanty</b>. Pro ty jsou vyhrazeny znaky [a..g]. V takové premise se musí vyskytovat právě jedna konstanta. Platné premisy obsahující konstanty:
            </p>
          <ul>
            <li>P(a) & S(a)</li>
            <li>¬Venn(b)</li>
            <li>P(g) ⊃ ¬Q(g)</li>
          </ul>
          <h3>Příklad validního vstupu:</h3>
          <ul>
            <li>∀x [A(x) & !B(x)]</li>
            <li>Ex [A(x) > C(x)]</li>
          </ul>
          <hr>
          <ul>
            <li>∃x[C(x)]</li>
          </ul>
          <h3>Příklad neplatného vstupu:</h3>
          <ul>
            <li>A(x) & B(x)</li>
            <li>∃x [A(x)] & ∃x [B(x)]</li>
            <li>∀x [A(x) > A(a)]</li>
          </ul>
          <hr>
          <ul>
            <li>C(x)</li>
          </ul>
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
import HelpHome from "@/components/HelpHome.vue";


export default {
  name: 'HomeView',
  components: {
    HelpHome,
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
      validity: null,
      help: false,
      myChart: null,
      resultVenn: null,
      Explanation: '',
      containers: [null, null, null, null, null, null],
      container_names: ["#venn_one", "#venn_two", "#venn_three", "#venn_four", "#venn_five", "#venn_six"]
    }
  },
  methods: {
    // sets the active input field to the one that was clicked on
    focusOnMe: function(key){
      console.log(key);
      let orig;
      if(key === -1){
        orig = this.focused;
        this.focused = document.getElementById("zaver");
        if (orig != null) {
          return;
        }
      }
      if (this.focused !== null && this.focused.value === ""){
        this.focused.classList.remove("invalid");
      }
      if (this.focused !== null && this.focused.value !== ""){
        if (!orig) orig = this.focused;
        try {
          axios.post('/val', {
            predicate: this.focused.value.toString(),
          }).then(response => {
           if (response.data.valid) {
             // good
              orig.classList.remove("invalid");
              this.$refs.why.classList.remove("bad");
              this.Explanation = "";
           }
           else {
             // color red
              orig.classList.add("invalid");
              console.log(orig);
              this.Explanation = response.data.err;
              this.validity = "";
              this.$refs.why.classList.add("activated");
              this.$refs.why.classList.add("bad");

           }
          });
        } catch (e) {
          console.log(e);
        }
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
      this.values['dynamic-field-' + this.count] = ''; // Set the value to an empty string
      if (this.count > 1)
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
    showHelp: function() {
      if (!this.help) {
        this.help = true;
        return;
      }
      this.help = false;
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
      this.focused.dispatchEvent(new Event('input')); // this is done because vue doesn't detect changes without an event
    },
    // submits the form and requests the data from the API
    async submit(steps){

      this.$refs.why.classList.remove("activated");
      this.$refs.why.classList.remove("bad");
      this.$refs.steps.classList.remove("activated");

      document.querySelectorAll(".bubble-thing").forEach(el => el.remove());

      setTimeout(() => this.$refs.why.classList.add("activated"), 100);
      setTimeout(() => this.$refs.steps.classList.add("activated"), 100);

      const invalids = document.getElementsByClassName("invalid");
      for (let i = 0; i < invalids.length; i++) {
        invalids[i].classList.remove("invalid");
      }


      let predicates = []
      for (let key of Object.keys(this.values)) {
        console.log(key + " -> " + this.values[key]);
        if (this.values[key].length !== 0)
          predicates.push(this.values[key]);
      }

      let conclusion = this.$refs.zaver.value;
     
      try {
        axios.post('/api', {
          conclusion: conclusion,
          predicates: predicates,
          paramsSerializer: params => {
            return qs.stringify(params)
          }
        }).then((response) => {
          console.log(response);

          this.APIErrorMessage = response.data['notes'] !== "OK" ? response.data['notes'] : "";
          this.validity = response.data["valid"];

          // this is the message to the user!
          // the "result" reasoning is at the 0th position
          // if we cannot find it, we will display the last one
          if (response.data["explanations"][0] !== undefined) {
            this.Explanation = String(response.data["explanations"][0]);
          }
          else {
            const max = Object.keys(response.data["explanations"]).length;
            this.Explanation = String(response.data["explanations"][max]);
            //console.log(max);
          }

          let theData = []
          for (const element of response.data["sets"]) {
            theData.push({ label: String(element), values: []})
          }

          if (this.resultVenn != null){
            this.resultVenn.unmount();
            this.resultVenn = null;
          }

          // sort every array inside this.universal alphabetically
          let universal_sorted = response.data["universal"];
          for (let i = 0; i < universal_sorted.length; i++) universal_sorted[i].sort();

          let existential_sorted = {};

          // sort dict entries
          for (let [key, value] of Object.entries(response.data["existential"])) {
            console.log(key, value, "key value");
            for (let i = 0; i < value.length; i++) value[i].sort();

            existential_sorted[key] = value.sort();
          }

          // sort bad dict
          let bad_sorted = {};
          for (let [key, value] of Object.entries(response.data["bad"])) {
            for (let i = 0; i < value.length; i++) value[i].sort();
            bad_sorted[key] = value.sort();
          }

          // sort counts keys
          let counts_sorted = {};
          console.log(response.data["counts"]);
          for (let [key, value] of Object.entries(response.data["counts"])) {
            for (let i = 0; i < value.length; i++) value[i].sort();
            counts_sorted[key] = value.sort();
          }
          if (!steps) {
            for (let i = 0; i < this.containers.length; i++) {
              if (this.containers[i] != null) this.containers[i].unmount();
            }

            this.resultVenn = createApp(VennVisualizer, {
              vennSize: response.data["sets"].length,
              sets: response.data["sets"].sort(),
              predicates: response.data["predicates"],
              explanations: response.data["explanations"],
              counts: counts_sorted,
              bad: bad_sorted,
              // solutions
              existential: existential_sorted,
              universal: universal_sorted,
              step: false,
              thisInstanceWillActAsUserInput: false,
            });
            this.resultVenn.mount('#venn');

          } else {
            if (this.resultVenn != null)
              this.resultVenn.unmount();

            // for each in steps
            let i = 1;
            for (const step of response.data["steps"]){
              //console.log(step, i);
              if (this.containers[i] != null)
                this.containers[i].unmount();

              let l_universal_sorted = step.universal;

              // sort every array inside this.universal alphabetically
              for (let i = 0; i < l_universal_sorted.length; i++) l_universal_sorted[i].sort();

              let l_existential_sorted = {};
              // sort dict entries
              for (let [key, value] of Object.entries(step.existential)) {
                //console.log(key, value, "key value");
                for (let i = 0; i < value.length; i++) value[i].sort();
                l_existential_sorted[key] = value.sort();
              }

              let l_bad_sorted = {};
              // sort dict entries
              for (let [key, value] of Object.entries(step.bad)) {
                //console.log(key, value, "key value");
                for (let i = 0; i < value.length; i++) value[i].sort();
                l_bad_sorted[key] = value.sort();
              }

              // sort counts keys
              let l_counts_sorted = {};
              for (let [key, value] of Object.entries(step.counts)) {
                for (let i = 0; i < value.length; i++) value[i].sort();
                l_counts_sorted[key] = value.sort();
              }

              this.containers[i] = createApp(VennVisualizer, {
                vennSize: step.sets.length,
                sets: step.sets.sort(),
                predicates: step.predicates,
                explanations: step.explanations,
                counts: l_counts_sorted,
                bad: l_bad_sorted,
                // solutions
                existential: l_existential_sorted,
                universal: l_universal_sorted,
                canvasPredicate: response.data["predicates"][step.p_index],
                canvasExplanation: response.data["explanations"][step.p_index][0],
                step: true,
                thisInstanceWillActAsUserInput: false,
              });
              this.containers[i].mount(this.container_names[i++]);
            }
          }
        }, (error) => {
          console.log(error);
          this.APIErrorMessage = "Něco se pokazilo na pozadí. Pokud problém přetrvává, kontaktujte administrátora.";
        });
      } catch (err) {
        // uh oh, didn't work, time for plan B
        console.log("?????");
      }
    },
  },
  mounted: function() {
    console.log("Mounted!")
    document.getElementById("predicate1").focus();
    //setTimeout(() => this.$refs.spinner.style.display = "none", 0);
    setTimeout(() => this.$refs.spinner.style.opacity = "0", 600);
    setTimeout(() => this.$refs.spinner.style.display = "none", 900);
  },
}
</script>