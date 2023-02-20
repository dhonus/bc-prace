<template>
  <div class="spinner" ref="spinner">
    <img src="@/assets/spinner.gif" alt="Spinner" />
  </div>
  <div class="home">
    <div class="tablinks">
      <div class="row">
        <div class="single">
          <a href="/">
            <button class="tab">Vyřešit</button>
          </a>
        </div>
        <div class="single">
          <a href="/validate">
            <button class="tab active">Zkontrolovat</button>
          </a>
        </div>
      </div>
    </div>
    <HelloWorld msg="Bc. Práce" style="display: none;"/>
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
            <p style="flex:1; text-align: left; font-size: larger;">Začít</p>
            <img style="color:white; height: 2rem; " src="../assets/control.svg">
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

        <!--<div id="venn_one"></div>
        <div id="venn_two"></div>
        <div id="venn_three"></div>
        <div id="venn_four"></div>
        <div id="venn_five"></div>
        <div id="venn_six"></div>-->
        <div class="steps" ref="steps">
          <div id="venn"></div>
          <div class="solution" v-if="solving">
          </div>
          <h3 class="small-title">Vaše řešení</h3>
          <div ref="solutionTable"></div>
          <h3 class="small-title">Správné řešení</h3>
          <div id="solution"></div>
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
          <h3>Interaktivní diagram</h3>
          <div class="mouseGuide">
            <div>
              <img src="../assets/icons/iconmonstr-mouse-12.svg" title="Vyšrafovat">
              <p>Vyšrafovat</p>
            </div>
            <div>
              <img src="../assets/icons/iconmonstr-mouse-14.svg" title="Přidat otazník">
              <p>Přidat křížek</p>
            </div>
          </div>
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
          <blockquote><p>Na vstupu mohou být premisy, nebo konstanty.</p></blockquote>
          <p><b>Premisa</b> se skládá z <b>literálů</b> a musí začínat kvantifikátorem a proměnnou, na kterou se váže. Následující jsou platné premisy:</p>
          <ul>
            <li>∃x[A(x)]</li>
            <li>∀x[B(x)]</li>
            <li>∃xA(x) ⊃ B(x)</li>
            <li>∀x B(x) & C(x)</li>
            <li>AxB(x)</li>
          </ul>
          <p><b>Literál</b> má vždy tvar Cokoliv(proměnná), kde proměnná je malé písmeno. Platné literály:</p>
          <ul>
            <li>P(x)</li>
            <li>Venn(y)</li>
          </ul>
          <p><b>Konstanty</b> se zapisují bez kvantifikátoru. Jsou pro ně vyhrazeny proměnné [a..g]:</p>
          <ul>
            <li>Q(a)</li>
            <li>P(g) ⊃ ¬Q(g)</li>
          </ul>
          <h3>Příklad validního vstupu:</h3>
          <ul>
            <li>∀x A(x) & !B(x)</li>
            <li>Ex [A(x) > C(x)]</li>
          </ul>
          <hr>
          <ul>
            <li>∃x[C(x)]</li>
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
import { h } from 'vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld,
  },
  data() {
    return {
      currentResponse: null,
      optionalPredicate:false,
      count: 3,
      values: {},
      focused: null,
      zaver: null,
      APIErrorMessage: '',
      validity: null,
      myChart: null,
      resultVenn: null,
      solvedVenn: null,
      Explanation: '',
      containers: [null, null, null, null, null, null],
      container_names: ["#venn_one", "#venn_two", "#venn_three", "#venn_four", "#venn_five", "#venn_six"],
      rootProps: {},
      solving: false,
    }
  },
  methods: {
      onSolve(areas_of_diagram_proxy) {
      if (areas_of_diagram_proxy && this.currentResponse !== null){
        try {
          this.solving = true;
          console.log(areas_of_diagram_proxy, "areas_of_diagram");
          try {
            this.solvedVenn.unmount();
            this.$refs.solutionTable.innerHTML = '';
          } catch (error) {
            // probably ok
          }

          this.solvedVenn = createApp(VennVisualizer, this.rootProps);
          // mount the instance to the DOM element with the id 'venn'
          this.solvedVenn.mount('#solution');

          // Get the reference to the table container
          let tableContainer = this.$refs.solutionTable;

          // Define the areas list
          const areas = this.currentResponse.sets;
          //const areas = ['A', 'B', 'C'];

          // Create the table element
          const table = document.createElement('table');

          // Create the table header row
          const headerRow = document.createElement('tr');

          // Create the header cells
          const areaHeader = document.createElement('th');
          areaHeader.textContent = 'Plocha';
          headerRow.appendChild(areaHeader);

          const predicateHeader = document.createElement('th');
          predicateHeader.textContent = 'Predikát';
          headerRow.appendChild(predicateHeader);

          const stateHeader = document.createElement('th');
          stateHeader.textContent = 'Správný stav';
          headerRow.appendChild(stateHeader);

          const explanationHeader = document.createElement('th');
          explanationHeader.textContent = 'Vysvětlení';
          headerRow.appendChild(explanationHeader);

          const correctHeader = document.createElement('th');
          correctHeader.textContent = 'Správně';
          headerRow.appendChild(correctHeader);

          // Add the header row to the table
          table.appendChild(headerRow);

          // Create the table rows for each area
          for (let i = 0; i < areas.length; i++) {
            // Create the row for the individual area
            const individualAreaRow = document.createElement('tr');

            let found;

            for (const obj in areas_of_diagram_proxy){
              if (areas_of_diagram_proxy[obj].assignment.length === 1
                  && areas_of_diagram_proxy[obj].assignment[0] === areas[i]){
                found = areas_of_diagram_proxy[obj];
                console.log("found", found);
                break;
              }
            }

            // Create the area cell
            const individualAreaCell = document.createElement('td');
            individualAreaCell.textContent = found.assignment.toString();
            individualAreaRow.appendChild(individualAreaCell);

            // Create the predicate, explanation, and correct cells
            const predicateCell = document.createElement('td');
            predicateCell.textContent = 'Predicate';
            individualAreaRow.appendChild(predicateCell);

            const stateCell = document.createElement('td');
            stateCell.textContent = '';

            let foundState = false;
            for (const obj in this.currentResponse.universal){
              if (this.currentResponse.universal[obj].length === 1
                  && this.currentResponse.universal[obj][0] === areas[i]){
                foundState = true;
                break;
              }
            }

            stateCell.classList.add(foundState ? 'hatched-cell' : 'clear-cell');
            stateCell.textContent = (foundState ? 'vyšrafovaná' : 'prázdná')
            individualAreaRow.appendChild(stateCell);

            const explanationCell = document.createElement('td');
            explanationCell.textContent = 'Explanation';
            individualAreaRow.appendChild(explanationCell);

            const correctCell = document.createElement('td');
            console.log(found, "found")
            let checkBox = document.createElement('input');
            checkBox.type = "checkbox";
            checkBox.checked = (foundState === (found.state === "hashed"));
            checkBox.disabled = true;
            correctCell.appendChild(checkBox);
            //correctCell.textContent = (foundState === (found.state === "hashed") ? 'Ano' : 'Ne');
            individualAreaRow.appendChild(correctCell);

            // Add the row to the table
            table.appendChild(individualAreaRow);

            for (let j = i + 1; j < areas.length; j++) {
              const areaCombination = areas[i] + areas[j];

              // Create the table row
              const row = document.createElement('tr');

              // Create the area cell
              const areaCell = document.createElement('td');
              areaCell.textContent = areaCombination;
              row.appendChild(areaCell);

              // Create the predicate, explanation, and correct cells
              const predicateCell = document.createElement('td');
              predicateCell.textContent = 'Predicate';
              row.appendChild(predicateCell);

              const stateCell = document.createElement('td');
              stateCell.textContent = 'State';
              row.appendChild(stateCell);

              const explanationCell = document.createElement('td');
              explanationCell.textContent = 'Explanation';
              row.appendChild(explanationCell);

              const correctCell = document.createElement('td');
              correctCell.textContent = '[]';
              row.appendChild(correctCell);

              // Add the row to the table
              table.appendChild(row);
            }
          }

          // Append the table to the tableContainer ref
          //this.$refs.tableContainer.appendChild(table);

          tableContainer.appendChild(table);

        } catch (error) {
          console.log(error);
        }
      }
      console.log(areas_of_diagram_proxy);
    },
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

      this.$refs.why.classList.remove("activated");
      this.$refs.steps.classList.remove("activated");

      setTimeout(() => this.$refs.why.classList.add("activated"), 100);
      setTimeout(() => this.$refs.steps.classList.add("activated"), 100);

      let predicates = []
      for (let key of Object.keys(this.values)) {
        console.log(key + " -> " + this.values[key]);
        if (this.values[key].length !== 0)
          predicates.push(this.values[key]);
      }

      this.solving = false;
      try {
        this.solvedVenn.unmount();
      } catch (error) {
        // probably ok
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

          this.currentResponse = response.data;

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

          if (!steps) {
            for (let i = 0; i < this.containers.length; i++) {
              if (this.containers[i] != null) this.containers[i].unmount();
            }

            const comp = h(VennVisualizer, {
              onSolve: e => this.onSolve(e),
            })

            this.rootProps = {
              vennSize: response.data["sets"].length,
              sets: response.data["sets"].sort(),
              predicates: response.data["predicates"],
              explanations: response.data["explanations"],
              bad: response.data["bad"],
              // solutions
              existential: existential_sorted,
              universal: universal_sorted,
              step: false,
            }

            this.resultVenn = createApp(comp, {
              vennSize: response.data["sets"].length,
              sets: response.data["sets"].sort(),
              predicates: response.data["predicates"],
              explanations: response.data["explanations"],
              bad: response.data["bad"],
              // solutions
              existential: {},
              universal: [],
              step: false,
              thisInstanceWillActAsUserInput: true,
            });
            // mount the instance to the DOM element with the id 'venn'
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

              this.containers[i] = createApp(VennVisualizer, {
                vennSize: step.sets.length,
                sets: step.sets.sort(),
                predicates: step.predicates,
                explanations: step.explanations,
                bad: l_bad_sorted,
                // solutions
                existential: l_existential_sorted,
                universal: l_universal_sorted,
                canvasPredicate: response.data["predicates"][step.p_index],
                canvasExplanation: response.data["explanations"][step.p_index][0],
                step: true,
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