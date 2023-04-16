<!-- https://axios-http.com/docs/post_example -->

<template>
  <div v-if="!limit" class="canvasWrapper" ref="canvasWrapper" oncontextmenu="return false;">
    <div v-if="step" class="information">
      <p ref="canvasPredicate">{{ canvasPredicate }}</p>
      <p ref="canvasExplanation">{{ canvasExplanation }}</p>
    </div>
    <p v-if="limit" class="information">Pro tuto velikost není náhled Vennova diagramu k dispozici.</p>
    <div class="entry_variable" v-if="thisInstanceWillActAsUserInput">
      <p>Proměnná</p>
      <input type="text"
             maxlength="1"
             v-model="entryVariable"
             ref="entryVariableInput"
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
    // solutions
    existential: Object,
    universal: Array,
    canvasPredicate: String,
    canvasExplanation: String,
    step: Boolean,
    thisInstanceWillActAsUserInput: Boolean,
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
    };
  },
  methods: {
    emitSolve: function (){
      this.$emit('solve', this.areas_of_diagram);
      console.log("emitted")
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
      console.log(this.currentModifierButton);
    },
    prepare: function() {
      let svg = d3.select(this.$refs.canvas);

      this.width = svg.attr("width") - margin.left - margin.right;
      this.height = +svg.attr("height") - margin.top - margin.bottom;

      // add hatching pattern to svg
      let pattern = svg.append("pattern").attr("id", "diagonalHatch").attr("patternUnits", "userSpaceOnUse").attr("width", 8).attr("height", 8);
      pattern.append("path").attr("d", "M-2,2 l4,-4 M0,8 l8,-8 M6,10 l4,-4").attr("style", "stroke: #3f3f3f; stroke-width: 2px;");

      let patternUniversum = svg.append("pattern").attr("id", "universumHatch").attr("patternUnits", "userSpaceOnUse").attr("width", 8).attr("height", 8);
      patternUniversum.append("path").attr("d", "M-2,2 l4,-4 M0,8 l8,-8 M6,10 l4,-4").attr("style", "stroke: #929292; stroke-width: 2px");
      patternUniversum.attr("patternTransform", "rotate(90)");

      const g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
      console.log(g);
      return g;
    },
    emptyDict: function(dict) {
      return Object.keys(dict).length === 0;
    },
    wipe: function(i){
      console.log("hey", this.positioned[i]);
      // remove all elements from the array
      this.positioned[i].length = 0;
      this.positioned[i] = [];
      console.log("hey", this.positioned[i]);
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
    universum_hatch_check: function (g){
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
            .attr("d", "M0,20 L" + this.width + ",20 L"
                + this.width + "," + (this.height + 20) + " L0," + (this.height + 20) + " L0,20")
            .attr("class", "segment")
            .attr("fill", hatched ? "url(#universumHatch)" : "#fbfbfb")
            .attr("opacity", 0.6);
      };
      // if universum is hashed
      if (this.universal.flat().includes('Ω')) {
        console.log("so flat", this.universal.flat());
        universum(g, true);
        return new Area("Universum", "hashed", "#fbfbfb", "A 0 20 0 0 1 " + this.width + " " + this.height);
      }
      else {
        universum(g, false);
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
        this.venn1();
        break;
      case 2:
        this.venn2();
        break;
      case 3:
        this.venn3();
        break;
      case 4:
        this.venn4();
        break;
      default:
        this.limit = true;
        console.log("no type specified");
    }
    console.log("created venn of size " + this.vennSize);
  },
};
</script>