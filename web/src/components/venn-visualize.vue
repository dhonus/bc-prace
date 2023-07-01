<!-- https://axios-http.com/docs/post_example -->

<template>
  <div v-if="!limit" class="canvasWrapper" ref="canvasWrapper" oncontextmenu="return false;">
    <div v-if="step" class="information">
      <p ref="canvasPredicate">{{ canvasPredicate }}</p>
      <p ref="canvasExplanation">{{ canvasExplanation }}</p>
    </div>
    <p v-if="limit" class="information">Pro tuto velikost není náhled Vennova diagramu k dispozici.</p>
    <div class="entry_variable" v-if="thisInstanceWillActAsUserInput">
      <p>Proměnná / konstanta</p>
      <input type="text"
             maxlength="1"
             v-model="entryVariable"
             ref="entryVariableInput"
             @input="smallOrNot"
             placeholder="x" />
    </div>
    <svg width="600" height="400" ref="canvas"></svg>
    <button class="accept_button"
            @click="emitSolve"
            v-if="thisInstanceWillActAsUserInput">
      Provést kontrolu
    </button>
  </div>
</template>

<script>
import * as d3 from 'd3'
import vennOne from './vennOne.vue'
import vennTwo from './vennTwo.vue'
import vennThree from './vennThree.vue'
import vennFour from './vennFour.vue'
import Area from "@/components/Area";
import d3Element from "@/components/d3Element";

const margin = {
  top: 0,
  right: 20,
  bottom: 30,
  left: 20,
};

/*
* In the other size files (VennOne ... VennFour), a lot of the code is duplicated, the refactoring would only make it more complicated to read.
* In the end we just recalculate some variables for each size, because for each of them the positioning code is slightly different.
* Enough to warrant this level of boilerplate.
* */

export default {
  name: 'vennVisualizer',
  mixins: [vennOne, vennTwo, vennThree, vennFour],
  props: {
    vennSize: Number,
    sets: Array,
    predicates: Object,
    explanations: Object,
    bad: Object,
    counts: Object,
    // solutions
    existential: Object,
    universal: Array,
    canvasPredicate: String,
    canvasExplanation: String,
    step: Boolean,
    thisInstanceWillActAsUserInput: Boolean,
    area_combinations: Array

  },
  data: () => {
    return {
      msg: '',
      entryVariable: '',
      currentModifierButton: "hatched",
      width: 0,
      height: 0,
      limit: false,
      mouseHatching: false,
      positioned: Object,
      areas_of_diagram: [],
      // the following are used for the hatching
      keys: Object,
    };
  },
  methods: {
    emitSolve: function (){
      this.$emit('solve', this.areas_of_diagram);
    },
    smallOrNot: function() {
      // get ref entryVariableInput
      //check if entryVariable is lowercase
      if (this.entryVariable.toLowerCase() !== this.entryVariable) {
        this.entryVariable = "";
      }
      if (this.entryVariable.toUpperCase() === this.entryVariable){
        this.entryVariable = "";
      }
    },
    // sets the current active button to the one that was clicked on
    activate: function(button){
      if(this.currentModifierButton !== null){
          this.$refs.question.classList.remove("activeCanvasControls");
          this.$refs.hatched.classList.remove("activeCanvasControls");
      }
      if (button === "question") {
        this.$refs.question.classList.add("activeCanvasControls");
        this.mouseHatching = false;
      }
      if (button === "hatched") {
        this.$refs.hatched.classList.add("activeCanvasControls");
        this.mouseHatching = true;
      }
      this.currentModifierButton = button;
    },
    prepare: function() {
      let svg = d3.select(this.$refs.canvas);

      this.width = svg.attr("width") - margin.left - margin.right;
      this.height = +svg.attr("height") - margin.top - margin.bottom;

      // add hatching pattern to svg
      let pattern = svg.append("pattern").attr("id", "diagonalHatch").attr("patternUnits", "userSpaceOnUse").attr("width", 8).attr("height", 8);
      pattern.append("path").attr("d", "M-2,2 l4,-4 M0,8 l8,-8 M6,10 l4,-4").attr("style", "stroke: #3f3f3f; stroke-width: 2px;");

      let patternUniversum = svg.append("pattern").attr("id", "universumHatch").attr("patternUnits", "userSpaceOnUse").attr("width", 8).attr("height", 8);
      patternUniversum.append("path").attr("d", "M-2,2 l4,-4 M0,8 l8,-8 M6,10 l4,-4").attr("style", "stroke: #c6c2c2; stroke-width: 2px");
      patternUniversum.attr("patternTransform", "rotate(90)");

      this.generateHatching(svg);

      const g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
      return g;
    },
    emptyDict: function(dict) {
      return Object.keys(dict).length === 0;
    },
    generateHatching(svg){
      // given a dictionary, where the key is a number and the value is an array of tuples, generate list of keys in which the given tuple is present
      let keys = {};
      /*for (let key in area_dict){
        if (area_dict[key].includes(tuple)){
          keys.push(key);
        }
      }*/
      for (let key in this.counts) {
          for (let value in this.counts[key]) {
              if (keys[this.counts[key][value]] === undefined) {
                  keys[this.counts[key][value]] = [];
              }
              keys[this.counts[key][value]].push(key);
          }
          // sort

      }

      // generate hatching pattern for each key. The dictionary is for example "A,B": [1,2,3]
      /*for (let key in keys){
          const concat = keys[key].join(",");
          // if such a pattern already exists, don't generate it again
          if (document.getElementById("diagonalHatch-" + concat) !== null){
              continue;
          }
          let pattern = svg.append("pattern").attr("id", "diagonalHatch-" + concat).attr("patternUnits", "userSpaceOnUse").attr("width", 8).attr("height", 8);
          for (let i = 0; i < keys[key].length; i++){
              console.log(i)
              let angle = 35 * (i+1); // Replace 'i' with your desired angle value

              // rotate the pattern by 45 degrees for each increment
              let p = pattern.append("pattern").attr("id", "diagonalHatch-" + concat + "-" + i).attr("patternUnits", "userSpaceOnUse").attr("width", 8).attr("height", 8);
              p.append("path").attr("d", "M-2,2 l4,-4 M0,8 l8,-8 M6,10 l4,-4").attr("style", "stroke: #3f3f3f; stroke-width: 2px;")

              pattern.append("rect").attr("width", 8).attr("height", 8).attr("fill", "url(#diagonalHatch-" + concat + "-" + i + ")")
              pattern.attr("patternTransform", "rotate(" + angle + ")");

          }*/
/*
          let pattern = svg.append("pattern").attr("id", "diagonalHatch-" + concat).attr("patternUnits", "userSpaceOnUse").attr("width", 8).attr("height", 8);

          for (let i = 0; i < keys[key].length; i++){
              if (document.getElementById("comp-" + keys[key][i]) !== null){
                  continue;
              }
              let angle = 35 * i; // Replace 'i' with your desired angle value

              let pathString = "M0,0 l8,8 M8,0 l-8,8";

              pattern
                .append("path")
                .attr("d", pathString)
                .attr("style", "stroke: #3f3f3f; stroke-width: 2px;")
                .attr("transform", "rotate(" + angle + ")");
          }
      }*/
      this.keys = keys;
    },
    wipe: function(i){
      // remove all elements from the array
      this.positioned[i].length = 0;
      this.positioned[i] = [];
      return true;
    },
    checkVar: function (i, variable){
      // check if the variable is already in the array
      for (let j = 0; j < this.positioned[i].length; j++){
        if (this.positioned[i][j].variable === variable){
          return true;
        }
      }
      return false;
    },
    universum_hatch_check: function (g, hatched){
     let keys = {};
      for (let key in this.counts) {
          for (let value in this.counts[key]) {
              if (keys[this.counts[key][value]] === undefined) {
                  keys[this.counts[key][value]] = [];
              }
              keys[this.counts[key][value]].push(key);
          }
      }
      const arr = keys["Ω"];
      for (let value in arr) {
          if (document.getElementById("uniHatch-" + arr[value]) !== null){
              g.append("rect")
                .attr("x", 0)
                .attr("y", 20)
                .attr("width", this.width)
                .attr("height", this.height)
                .attr("stroke", "#9782ae")
                .attr("fill", "url(#uniHatch-" + arr[value] +")")
              g.append("path")
                .attr("id", "Universum")
                .attr("name", "Ω")
                .attr("d", "M0,20 L" + this.width + ",20 L"
                    + this.width + "," + (this.height + 20) + " L0," + (this.height + 20) + " L0,20")
                .attr("class", "segment")
                .attr("fill", hatched ? "url(#uniHatch-" + arr[value] +")" : "#fbfbfb")
                .attr("opacity", 0.2);
              continue;
          }
          let pattern = g.append("pattern").attr("id", "uniHatch-" + arr[value]).attr("patternUnits", "userSpaceOnUse").attr("width", 12).attr("height", 12);
          pattern.append("path").attr("d", "M-3,3 l6,-6 M0,12 l12,-12 M9,15 l6,-6").attr("style", "stroke: #3f3f3f; stroke-width: 1.4px;")
          // add some spacing to the stroke
          pattern.attr("patternTransform", "rotate("+ arr[value] * 45 +" 0 0)")

          g.append("rect")
            .attr("x", 0)
            .attr("y", 20)
            .attr("width", this.width)
            .attr("height", this.height)
            .attr("stroke", "#9782ae")
            .attr("fill", "url(#uniHatch-" + arr[value] +")")

          g.append("path")
            .attr("id", "Universum")
            .attr("name", "Ω")
            .attr("d", "M0,20 L" + this.width + ",20 L"
                + this.width + "," + (this.height + 20) + " L0," + (this.height + 20) + " L0,20")
            .attr("class", "segment")
            .attr("fill", hatched ? "url(#uniHatch-" + arr[value] +")" : "#fbfbfb")
            .attr("opacity", 0.15);
      }

      // empty inline function
      let universum = (g, hatched) => {
        // add square to svg
        g.append("rect")
            .attr("x", 0)
            .attr("y", 20)
            .attr("width", this.width)
            .attr("height", this.height)
            .attr("fill", "none")
            .attr("stroke", "#9782ae");
        g.append("path")
            .attr("id", "Universum")
            .attr("name", "Ω")
            .attr("d", "M0,20 L" + this.width + ",20 L"
                + this.width + "," + (this.height + 20) + " L0," + (this.height + 20) + " L0,20")
            .attr("class", "segment")
            .attr("fill", hatched ? "url(#universumHatch)" : "#fbfbfb")
            .attr("opacity", 0.6);
      };
      // if universum is hashed
      if (this.universal.flat().includes('Ω')) {
        return new Area("Universum", "hashed", "#fbfbfb", "A 0 20 0 0 1 " + this.width + " " + this.height);
      }
      else {
        universum(g, false)
        return new Area("Universum", "clear", "#fbfbfb", "A 0 20 0 0 1 " + this.width + " " + this.height);
      }
    },
  },
  // called when the component is created and inserted into the DOM
  mounted: function () {
    this.limit = false;
    if (this.thisInstanceWillActAsUserInput){
      this.mouseHatching = true;
    }
    this.positioned = {
      '.': [],
    };
    switch (this.vennSize) {
      case 1:
        this.venn1(this.thisInstanceWillActAsUserInput, this.area_combinations);
        break;
      case 2:
        this.venn2(this.thisInstanceWillActAsUserInput, this.area_combinations);
        break;
      case 3:
        this.venn3(this.thisInstanceWillActAsUserInput, this.area_combinations);
        break;
      case 4:
        this.venn4(this.thisInstanceWillActAsUserInput, this.area_combinations);
        break;
      default:
        this.limit = true;
        console.log("no type specified");
    }
  },
};
</script>