<template>
  <div class="home">
    <HelloWorld msg="Bc. Práce"/>
    <div class="input_wrapper" @keyup.ctrl.enter="submitWithKey">
      <div class="predicates">
        <div v-for="key in count" :key="key">
          <Transition>
            <input @focus="focusOnMe(key)" :rel="'predicate'+key" type="text" v-model="values['dynamic-field-'+key]" :placeholder="key+'. predikát'" :id="'predicate'+key" >
          </Transition>
        </div>
        <div class="controls" style="justify-content: right; display: flex;">
          <button ref="buttonFour" class="button_plus" @click="addP" title="Přidat predikát">+</button>
          <button ref="buttonFour" class="button_plus" @click="removeP" title="Odebrat poslední predikát">-</button>
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
        <!--<h4>{{ logicResponseExistential }}</h4>-->
        <h4>{{ logicResponseUniversal }}</h4>

        <img src="@/assets/venn3_example.png" width="600">

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
          <p>Následuje tabulka podporovaných symbolů<br> včetně jejich akceptovatelných variant.</p>
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

          <h3>Příklad validního vstupu:</h3>
          <p>
            &nbsp;&nbsp;∀x[A(x) > !B(x)]<br>
            &nbsp;&nbsp;∀x[A(x) > B(x)]<br>
          </p>
          <hr>
          <p>
            &nbsp;&nbsp;∃x[C(x)]
          </p>
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
      if(key === -1){
        this.focused = document.getElementById("zaver");
        return;
      }
      this.focused = document.getElementById("predicate"+key);
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
    submitWithKey: function(){
      this.$refs.accept_button.classList.add("activated");
      this.submit();
      setTimeout(() => {
        this.$refs.accept_button.classList.remove("activated");
      }, 250);

    },
    type: function(value_to_enter){
      if (!this.focused){
        return;
      }
      const [start, end] = [this.focused.selectionStart, this.focused.selectionEnd];
      this.focused.setRangeText(value_to_enter, start, end, 'select');
      this.focused.setSelectionRange(end+1,end+1);
      this.focused.focus();
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
          this.logicResponseExistential = 'Existenční: ' + response.data["existential"] + "TBA";
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
  },
  mounted: function() {
    console.log("Mounted!")
    document.getElementById("predicate1").focus();
  },
}
</script>