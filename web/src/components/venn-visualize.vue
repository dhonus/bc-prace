<!-- https://axios-http.com/docs/post_example -->

<template>
  <div class="canvasControls">
    <div class="left">
      <p>Funkce diagramu:</p>
      <p ref="canvasMessage">{{ msg }}</p>
    </div>
    <div class="right">
      <div class="canvasButton" ref="empty" @click="activate('empty')">
        <img src="../assets/icons/empty.svg" title="Vyprázdnit">
      </div>
      <div class="canvasButton" ref="question" @click="activate('question')">
        <img src="../assets/icons/iconmonstr-question-thin.svg" title="Přidat otazník">
      </div>
      <div class="canvasButton" ref="hatched" @click="activate('hatched')">
        <img src="../assets/icons/hashed.svg" title="Vyšrafovat">
      </div>
    </div>
  </div>
  <div class="canvasWrapper" ref="canvasWrapper">
    <svg width="600" height="400" ref="canvas"></svg>
    <img ref="canvasExportImage">
  </div>
  <div class="print-wrapper">
    <div class="offset"></div>
    <div class="print-button" @click="printCanvas">
      <span class="download-text">Stáhnout</span>
      <img src="../assets/icons/iconmonstr-save-thin.svg" title="Tisk">
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import {indexOf} from "core-js/internals/array-includes";

class Area {
  constructor(id, state, color, assignment) {
    this.id = id;
    this.state = state; // clear | hashed | questioning
    this.color = color;
    this.comment = "";
    // this corresponds to the areas we get from the API.
    // Hardcoded in each of the venn functions because the API doesn't return the areas of the same name every time
    this.assignment = assignment;
  }
}

const margin = {
  top: 0,
  right: 20,
  bottom: 30,
  left: 20,
};

export default {
  name: 'vennVisualizer',
  props: {
    vennSize: Number,
    sets: Array,
    predicates: Object,
    explanations: Object,
    // solutions
    existential: Object,
    universal: Array,
  },
  data: () => {
    return {
      msg: '',
      currentModifierButton: null,
      width: 0,
      height: 0,
    };
  },
  methods: {
    printCanvas: function (){
      //const canvas = this.$refs.canvas;
      //const img    = canvas.toDataURL('image/png');
      //this.$refs.canvasExportImage.src = img;
      print();
    },
    // sets the current active button to the one that was clicked on
    activate: function(button){
      if(this.currentModifierButton !== null){
          this.$refs.empty.classList.remove("activeCanvasControls");
          this.$refs.question.classList.remove("activeCanvasControls");
          this.$refs.hatched.classList.remove("activeCanvasControls");
      }
      if (button === "empty") {
        this.$refs.empty.classList.add("activeCanvasControls");
      }
      if (button === "question") {
        this.$refs.question.classList.add("activeCanvasControls");
      }
      if (button === "hatched") {
        this.$refs.hatched.classList.add("activeCanvasControls");
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
      patternUniversum.append("path").attr("d", "M-2,2 l4,-4 M0,8 l8,-8 M6,10 l4,-4").attr("style", "stroke: #929292; stroke-width: 2px");
      patternUniversum.attr("patternTransform", "rotate(90)");

      const g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
      console.log(g);
      return g;
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
            .attr("fill", hatched ? "url(#universumHatch)" : "rgb(206, 206, 206)")
            .attr("opacity", 0.6);
      };
      // if universum is hashed
      if (this.universal.flat().includes('μ')) {
        console.log("so flat", this.universal.flat());
        universum(g, true);
        return new Area("Universum", "hashed", "#cecece", "A 0 20 0 0 1 " + this.width + " " + this.height);
      }
      else {
        universum(g, false);
        return new Area("Universum", "clear", "#cecece", "A 0 20 0 0 1 " + this.width + " " + this.height);
      }
    },
    venn1: function (){
      let g = this.prepare();
      let areas_of_diagram = [];

      // center of first circle
      const centerX_1 = 280;
      const centerY_1 = 200;
      const vennRadius = 100;

      const factor = 1.26;
      const offset = factor * vennRadius;
      // center of second circle
      const centerX_2 = centerX_1 + offset;
      const centerY_2 = centerY_1; //creating new var for clarity
      // center of third circle
      const centerX_3 = centerX_1 + offset / 2;
      const centerY_3 = centerY_1 + (Math.sqrt(3) * offset) / 2;

      areas_of_diagram.push(this.universum_hatch_check(g));

      // add circles to svg (The ones with _ are background circles)
      let circle1_ = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_1 + "," + centerY_1 + ")")
          .attr("class", "circle-background");
      let circle1 = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_1 + "," + centerY_1 + ")");

      // calculate points of intersections
      const generalHeight = Math.sqrt(vennRadius ** 2 - (offset / 2) ** 2);
      const C1__C2_X_up = centerX_3;
      const C1__C2_Y_up = centerY_1 - generalHeight;
      const C1__C2_X_down = centerX_3;
      const C1__C2_Y_down = centerY_1 + generalHeight;

      //treat "triHeight" as the hypoteneuse of a 30.60.90 triangle.
      //this tells us the shift from the midpoint of a leg of the triangle
      //to the point of intersection
      const xDelta = (generalHeight * Math.sqrt(3)) / 2;
      const yDelta = generalHeight / 2;

      const xMidpointC1C3 = (centerX_1 + centerX_3) / 2;
      const xMidpointC2C3 = (centerX_2 + centerX_3) / 2;
      const yMidpointBoth = (centerY_1 + centerY_3) / 2;

      // calculate the rest of the points of intersection
      const xIsect2 = xMidpointC1C3 - xDelta;
      const yIsect2 = yMidpointBoth + yDelta;
      const xIsect3 = xMidpointC2C3 + xDelta;
      const yIsect3 = yMidpointBoth + yDelta;

      const xIsect5 = xMidpointC1C3 + xDelta;
      const yIsect5 = yMidpointBoth - yDelta;
      const xIsect6 = xMidpointC2C3 - xDelta;
      const yIsect6 = yMidpointBoth - yDelta;

      let xPoints = [C1__C2_X_up, xIsect2, xIsect3, C1__C2_X_down, xIsect5, xIsect6];
      let yPoints = [C1__C2_Y_up, yIsect2, yIsect3, C1__C2_Y_down, yIsect5, yIsect6];

      const singleSetArea = ([x1, x2, x3, y1, y2, y3]) => {
        let path = `M ${x1} ${y1}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x2} ${y2}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x3} ${y3}
             A ${vennRadius} ${vennRadius} 0 1 1 ${x1} ${y1}`;
        return path;
      };

      let sunPoints = [
        [1, 5,  4],
      ];
      let sunPointsNames = [
        [this.sets[0]],
      ]
      let roundedTriPoints = [[5, 4, 6]];
      let roundedTriNames = [
        [this.sets[1], this.sets[2], this.sets[0]].sort(),
      ]

      const compareArrays = (arr1, arr2) => {
        return arr1.length === arr2.length && arr1.every((val, index) => val === arr2[index]);
      }

      console.log("our universal friends are ", this.universal)


      // find common
      let hash_these = sunPointsNames.filter((arr) => {
        return this.universal.some((arr2) => {
          return compareArrays(arr, arr2);
        });
      });
      console.log(hash_these, "hash these");

      let i = 0;
      let sunFill = "#8f8f8f";
      for (const points of sunPoints) {
        const ptCycle = points
            .map((i) => xPoints[i - 1])
            .concat(points.map((i) => yPoints[i - 1]));
        const shape = singleSetArea(ptCycle);
        const theId = String(points[0]) + String(points[1]) + String(points[2]);

        // if points is contained in hash_these
        if (hash_these.some((arr) => {
          return compareArrays(arr, sunPointsNames[i]);
        })) {
          // they are the same, so we need to hatch it
          console.log("hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "url(#diagonalHatch)")
              .attr("opacity", 1);
          areas_of_diagram.push(new Area(theId, "hashed", sunFill, sunPointsNames[i]));
        } else {
          console.log("dont hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", sunFill)
              .attr("opacity", 1);
          areas_of_diagram.push(new Area(theId, "clear", sunFill, sunPointsNames[i]));
        }
        i++;
      }

      // this is the function that will be called when the user clicks on a segment
      g.selectAll("path.segment").on("click", function () {
        const svg = d3.select(this);
        console.log(svg);
        console.log(svg.attr('id'));
        if (areas_of_diagram.find(e => e.id === svg.attr('id')).state === "hashed"){
          let area = areas_of_diagram.find(e => e.id === svg.attr('id'))
          area.state = "clear";
          svg.transition().attr("fill", area.color);
        } else {
          areas_of_diagram.find(e => e.id === svg.attr('id')).state = "hashed"; // mark the area as hatched
          if (svg.attr('id') === "Universum") {
            svg.transition().attr("fill", "url(#universumHatch)");
          } else {
            svg.transition().attr("fill", "url(#diagonalHatch)");
          }
        }
      });

      var tooltip = d3.select("body")
          .append("div")
          .style("position", "absolute")
          .style("z-index", "10")
          .style("visibility", "hidden")
          .style("background-color", "rgb(54, 54, 54)")
          .style("padding", ".8rem");

      var vis = d3.select("body").append("svg:svg")
          .attr("width", 0)
          .attr("height", 0);

      // hover over a segment and get its description
      g.selectAll("path.segment").on("mousemove", function (event) {
        const svg = d3.select(this);
        tooltip.text("ID plochy: " + svg.attr('id'));
        tooltip.style("visibility", "visible");
        tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");
        svg.style("", "url(#drop-shadow)");
      });

      g.selectAll("path.segment").on("mouseout", function (event) {
        tooltip.style("visibility", "hidden");
        const svg = d3.select(this);
      });

      g.append("text")
          .text("Ω")
          .attr("x", (this.width - 30))
          .attr("y", 50)
          .style('fill', '#323232')
          .style('font-size', '1.5rem');

      g.append("text")
          .text(this.sets[0])
          .attr("x", centerX_1 + vennRadius - 20)
          .attr("y", centerY_1 - vennRadius*0.8)
          .style('fill', '#323232');
    },
    venn2: function (){
      let g = this.prepare();
      let areas_of_diagram = [];

      // center of first circle
      const centerX_1 = 220;
      const centerY_1 = 200;
      const vennRadius = 100;

      const factor = 1.26;
      const offset = factor * vennRadius;
      // center of second circle
      const centerX_2 = centerX_1 + offset;
      const centerY_2 = centerY_1; //creating new var for clarity
      // center of third circle
      const centerX_3 = centerX_1 + offset / 2;
      const centerY_3 = centerY_1 + (Math.sqrt(3) * offset) / 2;

      areas_of_diagram.push(this.universum_hatch_check(g));

      // add circles to svg (The ones with _ are background circles)
      let circle1_ = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_1 + "," + centerY_1 + ")")
          .attr("class", "circle-background");
      let circle2_ = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_2 + "," + centerY_2 + ")")
          .attr("class", "circle-background");

      let circle1 = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_1 + "," + centerY_1 + ")");
      let circle2 = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_2 + "," + centerY_2 + ")");

      // calculate points of intersections
      const generalHeight = Math.sqrt(vennRadius ** 2 - (offset / 2) ** 2);
      const C1__C2_X_up = centerX_3;
      const C1__C2_Y_up = centerY_1 - generalHeight;
      const C1__C2_X_down = centerX_3;
      const C1__C2_Y_down = centerY_1 + generalHeight;

      //treat "triHeight" as the hypoteneuse of a 30.60.90 triangle.
      //this tells us the shift from the midpoint of a leg of the triangle
      //to the point of intersection
      const xDelta = (generalHeight * Math.sqrt(3)) / 2;
      const yDelta = generalHeight / 2;

      const xMidpointC1C3 = (centerX_1 + centerX_3) / 2;
      const xMidpointC2C3 = (centerX_2 + centerX_3) / 2;
      const yMidpointBoth = (centerY_1 + centerY_3) / 2;

      // calculate the rest of the points of intersection
      const xIsect2 = xMidpointC1C3 - xDelta;
      const yIsect2 = yMidpointBoth + yDelta;
      const xIsect3 = xMidpointC2C3 + xDelta;
      const yIsect3 = yMidpointBoth + yDelta;

      const xIsect5 = xMidpointC1C3 + xDelta;
      const yIsect5 = yMidpointBoth - yDelta;
      const xIsect6 = xMidpointC2C3 - xDelta;
      const yIsect6 = yMidpointBoth - yDelta;

      let xPoints = [C1__C2_X_up, xIsect2, xIsect3, C1__C2_X_down, xIsect5, xIsect6];
      let yPoints = [C1__C2_Y_up, yIsect2, yIsect3, C1__C2_Y_down, yIsect5, yIsect6];

      // three functions to create the paths using the points of intersection
      const intersectionOfTwoArea = ([x1, x2, x3, y1, y2, y3]) => {
        let path = `M ${x1} ${y1}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x2} ${y2}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x3} ${y3}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x1} ${y1}`;
        return path;
      };

      const singleSetArea = ([x1, x2, x3, y1, y2, y3]) => {
        let path = `M ${x1} ${y1}
             A ${vennRadius} ${vennRadius} 0 0 0 ${x2} ${y2}
             A ${vennRadius} ${vennRadius} 0 0 0 ${x3} ${y3}
             A ${vennRadius} ${vennRadius} 0 1 1 ${x1} ${y1}`;
        return path;
      };

      let ironPoints = [
        [1, 5, 4],
      ];
      let ironPointsNames = [
        [this.sets[0], this.sets[1]].sort(),
      ]
      let sunPoints = [
        [4, 5, 1],
        [1, 6, 4],
      ];
      let sunPointsNames = [
        [this.sets[1]],
        [this.sets[0]],
      ]
      let roundedTriPoints = [
          [5, 4, 6]
      ];
      let roundedTriNames = [
        [this.sets[1], this.sets[2], this.sets[0]].sort(),
      ]

      const compareArrays = (arr1, arr2) => {
        return arr1.length === arr2.length && arr1.every((val, index) => val === arr2[index]);
      }

      console.log("our universal friends are ", this.universal)
      console.log("the things are", ironPointsNames)
      // find common
      let hash_these = ironPointsNames.filter((arr) => {
        return this.universal.some((arr2) => {
          return compareArrays(arr, arr2);
        });
      });

      console.log(hash_these, "hash these");

      // three functions to iterate over points and append paths
      let i = 0;
      let ironFill = "#9f9f9f";
      for (const points of ironPoints) {
        const ptCycle = points
            .map((i) => xPoints[i - 1])
            .concat(points.map((i) => yPoints[i - 1]));
        const shape = intersectionOfTwoArea(ptCycle);
        const theId = String(points[0]) + String(points[1]) + String(points[2]);

        // if points is contained in hash_these
        if (hash_these.some((arr) => {
          return compareArrays(arr, ironPointsNames[i]);
        })) {
          // they are the same, so we need to hatch it
          console.log("hatch it");
          g.append("path")
              .attr("id", theId)
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "url(#diagonalHatch)")
              .attr("opacity", 0.5);
          areas_of_diagram.push(new Area(theId, "hashed", ironFill, ironPointsNames[i]));
        } else {
          console.log("dont hatch it");
          g.append("path")
              .attr("id", theId)
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", ironFill)
              .attr("opacity", 0.4);
          areas_of_diagram.push(new Area(theId, "clear", ironFill, ironPointsNames[i]));
        }

        console.log(this.universal, "universal ", ironPointsNames[i]);

        i++;
      }

      // find common
      hash_these = sunPointsNames.filter((arr) => {
        return this.universal.some((arr2) => {
          return compareArrays(arr, arr2);
        });
      });
      console.log(hash_these, "hash these");

      i = 0;
      let sunFill = "#8f8f8f";
      for (const points of sunPoints) {
        const ptCycle = points
            .map((i) => xPoints[i - 1])
            .concat(points.map((i) => yPoints[i - 1]));
        const shape = singleSetArea(ptCycle);
        const theId = String(points[0]) + String(points[1]) + String(points[2]);

        // if points is contained in hash_these
        if (hash_these.some((arr) => {
          return compareArrays(arr, sunPointsNames[i]);
        })) {
          // they are the same, so we need to hatch it
          console.log("hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "url(#diagonalHatch)")
              .attr("opacity", 1);
          areas_of_diagram.push(new Area(theId, "hashed", sunFill, sunPointsNames[i]));
        } else {
          console.log("dont hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", sunFill)
              .attr("opacity", 1);
          areas_of_diagram.push(new Area(theId, "clear", sunFill, sunPointsNames[i]));
        }
        i++;
      }
      console.log(areas_of_diagram);

      // this is the function that will be called when the user clicks on a segment
      g.selectAll("path.segment").on("click", function () {
        const svg = d3.select(this);
        console.log(svg);
        console.log(svg.attr('id'));
        if (areas_of_diagram.find(e => e.id === svg.attr('id')).state === "hashed"){
          let area = areas_of_diagram.find(e => e.id === svg.attr('id'))
          area.state = "clear";
          svg.transition().attr("fill", area.color);
        } else {
          areas_of_diagram.find(e => e.id === svg.attr('id')).state = "hashed"; // mark the area as hatched
          if (svg.attr('id') === "Universum") {
            svg.transition().attr("fill", "url(#universumHatch)");
          } else {
            svg.transition().attr("fill", "url(#diagonalHatch)");
          }
        }
      });

      var tooltip = d3.select("body")
          .append("div")
          .style("position", "absolute")
          .style("z-index", "10")
          .style("visibility", "hidden")
          .style("background-color", "rgb(54, 54, 54)")
          .style("padding", ".8rem");

      var vis = d3.select("body").append("svg:svg")
          .attr("width", 0)
          .attr("height", 0);

      // hover over a segment and get its description
      g.selectAll("path.segment").on("mousemove", function (event) {
        const svg = d3.select(this);
        tooltip.text("ID plochy: " + svg.attr('id'));
        tooltip.style("visibility", "visible");
        tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");
        svg.style("", "url(#drop-shadow)");
      });

      g.selectAll("path.segment").on("mouseout", function (event) {
        tooltip.style("visibility", "hidden");
        const svg = d3.select(this);
      });

      g.append("text")
          .text("Ω")
          .attr("x", (this.width - 30))
          .attr("y", 50)
          .style('fill', '#323232')
          .style('font-size', '1.5rem');

      g.append("text")
          .text(this.sets[0])
          .attr("x", centerX_1 - vennRadius - 20)
          .attr("y", centerY_1 - vennRadius*0.9)
          .style('fill', '#323232');

      g.append("text")
          .text(this.sets[1])
          .attr("x", centerX_2 + vennRadius - 20)
          .attr("y", centerY_2 - vennRadius*0.9)
          .style('fill', '#323232');

    },
    venn3: function(){
      let g = this.prepare();
      let areas_of_diagram = [];

      // center of first circle
      const centerX_1 = 220;
      const centerY_1 = 150;
      const vennRadius = 100;

      const factor = 1.26;
      const offset = factor * vennRadius;
      // center of second circle
      const centerX_2 = centerX_1 + offset;
      const centerY_2 = centerY_1; //creating new var for clarity
      // center of third circle
      const centerX_3 = centerX_1 + offset / 2;
      const centerY_3 = centerY_1 + (Math.sqrt(3) * offset) / 2;

      areas_of_diagram.push(this.universum_hatch_check(g));

      // add circles to svg (The ones with _ are background circles)
      let circle1_ = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_1 + "," + centerY_1 + ")")
              .attr("class", "circle-background");
      let circle2_ = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_2 + "," + centerY_2 + ")")
          .attr("class", "circle-background");
      let circle3_ = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_3 + "," + centerY_3 + ")")
          .attr("class", "circle-background");

      let circle1 = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_1 + "," + centerY_1 + ")");
      let circle2 = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_2 + "," + centerY_2 + ")");
      let circle3 = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_3 + "," + centerY_3 + ")");

      // calculate points of intersections
      const generalHeight = Math.sqrt(vennRadius ** 2 - (offset / 2) ** 2);
      const C1__C2_X_up = centerX_3;
      const C1__C2_Y_up = centerY_1 - generalHeight;
      const C1__C2_X_down = centerX_3;
      const C1__C2_Y_down = centerY_1 + generalHeight;

      //treat "triHeight" as the hypoteneuse of a 30.60.90 triangle.
      //this tells us the shift from the midpoint of a leg of the triangle
      //to the point of intersection
      const xDelta = (generalHeight * Math.sqrt(3)) / 2;
      const yDelta = generalHeight / 2;

      const xMidpointC1C3 = (centerX_1 + centerX_3) / 2;
      const xMidpointC2C3 = (centerX_2 + centerX_3) / 2;
      const yMidpointBoth = (centerY_1 + centerY_3) / 2;

      // calculate the rest of the points of intersection
      const xIsect2 = xMidpointC1C3 - xDelta;
      const yIsect2 = yMidpointBoth + yDelta;
      const xIsect3 = xMidpointC2C3 + xDelta;
      const yIsect3 = yMidpointBoth + yDelta;

      const xIsect5 = xMidpointC1C3 + xDelta;
      const yIsect5 = yMidpointBoth - yDelta;
      const xIsect6 = xMidpointC2C3 - xDelta;
      const yIsect6 = yMidpointBoth - yDelta;

      let xPoints = [C1__C2_X_up, xIsect2, xIsect3, C1__C2_X_down, xIsect5, xIsect6];
      let yPoints = [C1__C2_Y_up, yIsect2, yIsect3, C1__C2_Y_down, yIsect5, yIsect6];

      // three functions to create the paths using the points of intersection
      const intersectionOfTwoArea = ([x1, x2, x3, y1, y2, y3]) => {
        let path = `M ${x1} ${y1}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x2} ${y2}
             A ${vennRadius} ${vennRadius} 0 0 0 ${x3} ${y3}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x1} ${y1}`;
        return path;
      };

      const singleSetArea = ([x1, x2, x3, y1, y2, y3]) => {
        let path = `M ${x1} ${y1}
             A ${vennRadius} ${vennRadius} 0 0 0 ${x2} ${y2}
             A ${vennRadius} ${vennRadius} 0 0 0 ${x3} ${y3}
             A ${vennRadius} ${vennRadius} 0 1 1 ${x1} ${y1}`;
        return path;
      };

      const intersectionOfThreeArea = ([x1, x2, x3, y1, y2, y3]) => {
        let path = `M ${x1} ${y1}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x2} ${y2}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x3} ${y3}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x1} ${y1}`;
        return path;
      };

      let ironPoints = [
        [1, 5, 6],
        [3, 4, 5],
        [2, 6, 4],
      ];
      let ironPointsNames = [
          [this.sets[0], this.sets[1]].sort(),
          [this.sets[1], this.sets[2]].sort(),
          [this.sets[2], this.sets[0]].sort(),
      ]
      let sunPoints = [
        [3, 5, 1],
        [2, 4, 3],
        [1, 6, 2],
      ];
      let sunPointsNames = [
        [this.sets[1]],
        [this.sets[2]],
        [this.sets[0]],
      ]
      let roundedTriPoints = [[5, 4, 6]];
      let roundedTriNames = [
        [this.sets[1], this.sets[2], this.sets[0]].sort(),
      ]

      const compareArrays = (arr1, arr2) => {
        return arr1.length === arr2.length && arr1.every((val, index) => val === arr2[index]);
      }

      console.log("our universal friends are ", this.universal)
      console.log("the things are", ironPointsNames)
      // find common
      let hash_these = ironPointsNames.filter((arr) => {
        return this.universal.some((arr2) => {
          return compareArrays(arr, arr2);
        });
      });

      console.log(hash_these, "hash these");

      // three functions to iterate over points and append paths
      let i = 0;
      let ironFill = "#9f9f9f";
      for (const points of ironPoints) {
        const ptCycle = points
            .map((i) => xPoints[i - 1])
            .concat(points.map((i) => yPoints[i - 1]));
        const shape = intersectionOfTwoArea(ptCycle);
        const theId = String(points[0]) + String(points[1]) + String(points[2]);

        // if points is contained in hash_these
        if (hash_these.some((arr) => {
          return compareArrays(arr, ironPointsNames[i]);
        })) {
          // they are the same, so we need to hatch it
          console.log("hatch it");
          g.append("path")
              .attr("id", theId)
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "url(#diagonalHatch)")
              .attr("opacity", 0.5);
          areas_of_diagram.push(new Area(theId, "hashed", ironFill, ironPointsNames[i]));
        } else {
          console.log("dont hatch it");
          g.append("path")
              .attr("id", theId)
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", ironFill)
              .attr("opacity", 0.4);
          areas_of_diagram.push(new Area(theId, "clear", ironFill, ironPointsNames[i]));
        }

        console.log(this.universal, "universal ", ironPointsNames[i]);

        i++;
      }

      // find common
      hash_these = sunPointsNames.filter((arr) => {
        return this.universal.some((arr2) => {
          return compareArrays(arr, arr2);
        });
      });
      console.log(hash_these, "hash these");

      i = 0;
      let sunFill = "#8f8f8f";
      for (const points of sunPoints) {
        const ptCycle = points
            .map((i) => xPoints[i - 1])
            .concat(points.map((i) => yPoints[i - 1]));
        const shape = singleSetArea(ptCycle);
        const theId = String(points[0]) + String(points[1]) + String(points[2]);

        // if points is contained in hash_these
        if (hash_these.some((arr) => {
          return compareArrays(arr, sunPointsNames[i]);
        })) {
          // they are the same, so we need to hatch it
          console.log("hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "url(#diagonalHatch)")
              .attr("opacity", 1);
          areas_of_diagram.push(new Area(theId, "hashed", sunFill, sunPointsNames[i]));
        } else {
          console.log("dont hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", sunFill)
              .attr("opacity", 1);
          areas_of_diagram.push(new Area(theId, "clear", sunFill, sunPointsNames[i]));
        }
        i++;
      }

      // find common
      hash_these = roundedTriNames.filter((arr) => {
        return this.universal.some((arr2) => {
          return compareArrays(arr, arr2);
        });
      });
      console.log(hash_these, "hash these !");

      for (const points of roundedTriPoints) {
        const ptCycle = points
            .map((i) => xPoints[i - 1])
            .concat(points.map((i) => yPoints[i - 1]));
        const shape = intersectionOfThreeArea(ptCycle);
        const theId = String(points[0]) + String(points[1]) + String(points[2]);

        // if points is contained in hash_these
        if (hash_these.some((arr) => {
          return compareArrays(arr, roundedTriNames[0]);
        })) {
          // they are the same, so we need to hatch it
          console.log("hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "url(#diagonalHatch)")
              .attr("opacity", 1);
          areas_of_diagram.push(new Area(theId, "hashed", "#aa86c5", roundedTriNames[0]));
        } else {
          console.log("dont hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "#aa86c5")
              .attr("opacity", 1);
          areas_of_diagram.push(new Area(theId, "clear", "#aa86c5", roundedTriNames[0]));
        }
      }

      console.log(areas_of_diagram);

      // this is the function that will be called when the user clicks on a segment
      g.selectAll("path.segment").on("click", function () {
        const svg = d3.select(this);
        console.log(svg);
        console.log(svg.attr('id'));
        if (areas_of_diagram.find(e => e.id === svg.attr('id')).state === "hashed"){
          let area = areas_of_diagram.find(e => e.id === svg.attr('id'))
          area.state = "clear";
          svg.transition().attr("fill", area.color);
        } else {
          areas_of_diagram.find(e => e.id === svg.attr('id')).state = "hashed"; // mark the area as hatched
          if (svg.attr('id') === "Universum") {
              svg.transition().attr("fill", "url(#universumHatch)");
            } else {
            svg.transition().attr("fill", "url(#diagonalHatch)");
          }
        }
      });

      var tooltip = d3.select("body")
          .append("div")
          .style("position", "absolute")
          .style("z-index", "10")
          .style("visibility", "hidden")
          .style("background-color", "rgb(54, 54, 54)")
          .style("padding", ".8rem");

      var vis = d3.select("body").append("svg:svg")
          .attr("width", 0)
          .attr("height", 0);

      // hover over a segment and get its description
      g.selectAll("path.segment").on("mousemove", function (event) {
        const svg = d3.select(this);
        tooltip.text("ID plochy: " + svg.attr('id'));
        tooltip.style("visibility", "visible");
        tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");
        svg.style("", "url(#drop-shadow)");
      });

      g.selectAll("path.segment").on("mouseout", function (event) {
        tooltip.style("visibility", "hidden");
        const svg = d3.select(this);
      });

      let __sets_identifiers = [
        [this.sets[0]],
        [this.sets[1]],
        [this.sets[2]],

        [this.sets[0], this.sets[1]],
        [this.sets[1], this.sets[2]],
        [this.sets[0], this.sets[2]],

        [this.sets[0], this.sets[1], this.sets[2]],
      ];

      // positions as [x, y]; corresponds to __sets_identifiers
      let __sets_positions = [
        [centerX_1 - 20, centerY_1 - 20],
        [centerX_2 + 60, centerY_2 - 20],
        [centerX_3 + 20, centerY_3 + 60],

        [centerX_3 + 20, centerY_2 - 20],
        [xMidpointC2C3 + 40, yMidpointBoth + 20],
        [xMidpointC1C3, yMidpointBoth + 20],

        [centerX_3 + 20, yMidpointBoth - 10],
      ]

      console.log(__sets_identifiers);

      let position_me = (index, key, character) => {
        const pos = __sets_positions[index];
        console.log(pos, key, "pos, key");
        // background for the text
        g.append("circle")
            .attr("r", 14)
            .attr("transform", "translate(" + (pos[0] - 20) + "," + (pos[1] - 10) + ")")
            .attr("class", character === "?" ? "question-background" : "set-background")
        // the "X" or "?"
        g.append("text")
            .text(character)
            .attr("x", pos[0] - (character === "?" ? 27 : 28))
            .attr("y", pos[1] - 5)
            .style('fill', '#323232')
            .attr("class", character === "?" ? "question-text" : "set-text")
            .style('font-size', '1.2rem');
        // the variable
        g.append("text")
            .text(key)
            .attr("x", pos[0] - (character === "?" ? 18 : 18))
            .attr("y", pos[1] - 1)
            .style('fill', '#323232')
            .attr("class", character === "?" ? "question-text" : "set-text")
            .style('font-size', '.8rem');
      }

      /*for (let pos of __sets_positions) {
        let key = "x";
        position_me(pos, key);
      }*/

      // existential
      console.log(this.existential, "existential");
      for (const position in __sets_identifiers){
        for(let key in this.existential) {
          console.log("the size is: " + this.existential[key].length);
          for (let all in this.existential[key]) {
            if (compareArrays(this.existential[key][all], __sets_identifiers[position])) {
              console.log("found it");
              console.log(this.existential[key][all], __sets_identifiers[position]);
              position_me(position, key, this.existential[key].length === 1 ? "x" : "?");

            }
          }
          /*
          console.log(key[0].toString())
          if (key[0].toString() == position.toString()) {
            console.log(this.existential[key][0], "existential key");
            console.log(__sets_identifiers.indexOf(this.existential[key][0]), "index of");
          } else {
            console.log("not found");
          }
          */
        }
      }


      console.log(this.existential instanceof Array)

      g.append("text")
          .text("Ω")
          .attr("x", (this.width - 30))
          .attr("y", 50)
          .style('fill', '#323232')
          .style('font-size', '1.5rem');

      g.append("text")
          .text(this.sets[0])
          .attr("x", centerX_1 - vennRadius)
          .attr("y", centerY_1 - vennRadius*0.8)
          .style('fill', '#323232');

      g.append("text")
          .text(this.sets[1])
          .attr("x", centerX_2 + vennRadius)
          .attr("y", centerY_2 - vennRadius*0.8)
          .style('fill', '#323232');

      g.append("text")
          .text(this.sets[2])
          .attr("x", centerX_3)
          .attr("y", centerY_3 + vennRadius*1.3)
          .style('fill', '#323232');
/*
      // add the text labels
      g.append("text")
          .text("1")
          .attr("x", C1__C2_X_up)
          .attr("y", C1__C2_Y_up)
          .style('fill', 'white')

      g.append("text")
          .text("2")
          .attr("x", xIsect2)
          .attr("y", yIsect2)
          .style('fill', 'white')


      g.append("text")
          .text("3")
          .attr("x", xIsect3)
          .attr("y", yIsect3)
          .style('fill', 'white')


      g.append("text")
          .text("4")
          .attr("x", C1__C2_X_down)
          .attr("y", C1__C2_Y_down)
          .style('fill', 'white')


      g.append("text")
          .text("5")
          .attr("x", xIsect5)
          .attr("y", yIsect5)
          .style('fill', 'white')


      g.append("text")
          .text("6")
          .attr("x", xIsect6)
          .attr("y", yIsect6)
          .style('fill', 'white')
*/


    },
    venn4: function(){
      let g = this.prepare();
      let areas_of_diagram = [];

      // center of first circle
      const centerX_1 = 220;
      const centerY_1 = 150;
      const vennRadius = 100;

      const factor = 1.26;
      const offset = factor * vennRadius;
      // center of second circle
      const centerX_2 = centerX_1 + offset;
      const centerY_2 = centerY_1; //creating new var for clarity
      // center of third circle
      const centerX_3 = centerX_1;
      const centerY_3 = centerY_1 + (Math.sqrt(3) * offset) / 2;
      // center of fourth circle
      const centerX_4 = centerX_1 + offset;
      const centerY_4 = centerY_1 + (Math.sqrt(3) * offset) / 2;

      areas_of_diagram.push(this.universum_hatch_check(g));

      // add circles to svg (The ones with _ are background circles)
      let circle1_ = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_1 + "," + centerY_1 + ")")
          .attr("class", "circle-background");
      let circle2_ = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_2 + "," + centerY_2 + ")")
          .attr("class", "circle-background");
      let circle3_ = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_3 + "," + centerY_3 + ")")
          .attr("class", "circle-background");
      let circle4_ = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_4 + "," + centerY_4 + ")")
          .attr("class", "circle-background");

      let circle1 = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_1 + "," + centerY_1 + ")");
      let circle2 = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_2 + "," + centerY_2 + ")");
      let circle3 = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_3 + "," + centerY_3 + ")");
      let circle4 = g.append("circle").attr("r", vennRadius).attr("transform", "translate(" + centerX_4 + "," + centerY_4 + ")");

      // calculate points of intersections
      const generalHeight = Math.sqrt(vennRadius ** 2 - (offset / 2) ** 2);


      //treat "triHeight" as the hypoteneuse of a 30.60.90 triangle.
      //this tells us the shift from the midpoint of a leg of the triangle
      //to the point of intersection
      const xDelta = (generalHeight * Math.sqrt(3)) / 2;
      const yDelta = generalHeight;

      const xMidpointC1C3 = (centerX_1 + centerX_3) / 2;
      const xMidpointC2C3 = (centerX_2 + centerX_3) / 2;
      const yMidpointBoth = (centerY_1 + centerY_3) / 2;

      const x_intersect_1 = centerX_1 + offset / 2;
      const y_intersect_1 = centerY_1 - generalHeight;

      const x_intersect_2 = centerX_1 - generalHeight;
      const y_intersect_2 = centerY_1 + generalHeight - 20;

      const x_intersect_3 = centerX_3 + generalHeight - 20;
      const y_intersect_3 = centerY_3 + generalHeight;

      const x_intersect_4 = centerX_4 + generalHeight;
      const y_intersect_4 = centerY_2 + generalHeight - 20;

      const x_intersect_5 = centerX_2 - generalHeight - 20;
      const y_intersect_5 = centerY_3 - generalHeight;

      const x_intersect_6 = centerX_1 + generalHeight + 20;
      const y_intersect_6 = centerY_3 - generalHeight;

      const x_intersect_7 = centerX_3 + generalHeight + 20;
      const y_intersect_7 = centerY_2 + generalHeight + 20;

      const x_intersect_8 = centerX_2 - generalHeight - 20;
      const y_intersect_8 = centerY_2 + generalHeight + 20;

      const x_intersect_9 = centerX_3 + generalHeight + 20;
      const y_intersect_9 = centerY_4 - generalHeight;

      const x_intersect_10 = centerX_1 - generalHeight - 20;
      const y_intersect_10 = centerY_4 + generalHeight;

      const x_intersect_11 = centerX_2 + generalHeight + 20;
      const y_intersect_11 = centerY_1 + generalHeight;

      const x_intersect_12 = centerX_4 - generalHeight;
      const y_intersect_12 = centerY_1 + generalHeight - 20;


      let xPoints = [x_intersect_1, x_intersect_2, x_intersect_3, x_intersect_4, x_intersect_5, x_intersect_6, x_intersect_7, x_intersect_8, x_intersect_9, x_intersect_10, x_intersect_11, x_intersect_12];
      let yPoints = [y_intersect_1, y_intersect_2, y_intersect_3, y_intersect_4, y_intersect_5, y_intersect_6, y_intersect_7, y_intersect_8, y_intersect_9, y_intersect_10, y_intersect_11, y_intersect_12];


      // three functions to create the paths using the points of intersection
      const intersectionOfTwoArea = ([x1, x2, x3, y1, y2, y3]) => {
        let path = `M ${x1} ${y1}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x2} ${y2}
             A ${vennRadius} ${vennRadius} 0 0 0 ${x3} ${y3}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x1} ${y1}`;
        return path;
      };

      const singleSetArea = ([x1, x2, x3, y1, y2, y3]) => {
        let path = `M ${x1} ${y1}
             A ${vennRadius} ${vennRadius} 0 0 0 ${x2} ${y2}
             A ${vennRadius} ${vennRadius} 0 0 0 ${x3} ${y3}
             A ${vennRadius} ${vennRadius} 0 1 1 ${x1} ${y1}`;
        return path;
      };

      const intersectionOfThreeArea = ([x1, x2, x3, y1, y2, y3]) => {
        let path = `M ${x1} ${y1}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x2} ${y2}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x3} ${y3}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x1} ${y1}`;
        return path;
      };

      let ironPoints = [
        [1, 5, 6],
        [3, 4, 5],
        [2, 6, 4],
      ];
      let ironPointsNames = [
        [this.sets[0], this.sets[1]].sort(),
        [this.sets[1], this.sets[2]].sort(),
        [this.sets[2], this.sets[0]].sort(),
      ]
      let sunPoints = [
        [3, 5, 1],
        [2, 4, 3],
        [1, 6, 2],
      ];
      let sunPointsNames = [
        [this.sets[1]],
        [this.sets[2]],
        [this.sets[0]],
      ]
      let roundedTriPoints = [[5, 4, 6]];
      let roundedTriNames = [
        [this.sets[1], this.sets[2], this.sets[0]].sort(),
      ]

      const compareArrays = (arr1, arr2) => {
        return arr1.length === arr2.length && arr1.every((val, index) => val === arr2[index]);
      }

      console.log("our universal friends are ", this.universal)
      console.log("the things are", ironPointsNames)
      // find common
      let hash_these = ironPointsNames.filter((arr) => {
        return this.universal.some((arr2) => {
          return compareArrays(arr, arr2);
        });
      });

      console.log(hash_these, "hash these");

      // three functions to iterate over points and append paths
      let i = 0;
      let ironFill = "#9f9f9f";
      for (const points of ironPoints) {
        const ptCycle = points
            .map((i) => xPoints[i - 1])
            .concat(points.map((i) => yPoints[i - 1]));
        const shape = intersectionOfTwoArea(ptCycle);
        const theId = String(points[0]) + String(points[1]) + String(points[2]);

        // if points is contained in hash_these
        if (hash_these.some((arr) => {
          return compareArrays(arr, ironPointsNames[i]);
        })) {
          // they are the same, so we need to hatch it
          console.log("hatch it");

          g.append("path")
              .attr("id", theId)
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "url(#diagonalHatch)")
              .attr("opacity", 0.0);
          areas_of_diagram.push(new Area(theId, "hashed", ironFill, ironPointsNames[i]));
        } else {
          console.log("dont hatch it");
          g.append("path")
              .attr("id", theId)
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", ironFill)
              .attr("opacity", 0.0);
          areas_of_diagram.push(new Area(theId, "clear", ironFill, ironPointsNames[i]));
        }

        console.log(this.universal, "universal ", ironPointsNames[i]);

        i++;
      }

      // find common
      hash_these = sunPointsNames.filter((arr) => {
        return this.universal.some((arr2) => {
          return compareArrays(arr, arr2);
        });
      });
      console.log(hash_these, "hash these");

      i = 0;
      let sunFill = "#8f8f8f";
      for (const points of sunPoints) {
        const ptCycle = points
            .map((i) => xPoints[i - 1])
            .concat(points.map((i) => yPoints[i - 1]));
        const shape = singleSetArea(ptCycle);
        const theId = String(points[0]) + String(points[1]) + String(points[2]);

        // if points is contained in hash_these
        if (hash_these.some((arr) => {
          return compareArrays(arr, sunPointsNames[i]);
        })) {
          // they are the same, so we need to hatch it
          console.log("hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "url(#diagonalHatch)")
              .attr("opacity", 1);
          areas_of_diagram.push(new Area(theId, "hashed", sunFill, sunPointsNames[i]));
        } else {
          console.log("dont hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", sunFill)
              .attr("opacity", 0);
          areas_of_diagram.push(new Area(theId, "clear", sunFill, sunPointsNames[i]));
        }
        i++;
      }

      // find common
      hash_these = roundedTriNames.filter((arr) => {
        return this.universal.some((arr2) => {
          return compareArrays(arr, arr2);
        });
      });
      console.log(hash_these, "hash these !");

      for (const points of roundedTriPoints) {
        const ptCycle = points
            .map((i) => xPoints[i - 1])
            .concat(points.map((i) => yPoints[i - 1]));
        const shape = intersectionOfThreeArea(ptCycle);
        const theId = String(points[0]) + String(points[1]) + String(points[2]);

        // if points is contained in hash_these
        if (hash_these.some((arr) => {
          return compareArrays(arr, roundedTriNames[0]);
        })) {
          // they are the same, so we need to hatch it
          console.log("hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "url(#diagonalHatch)")
              .attr("opacity", 0);
          areas_of_diagram.push(new Area(theId, "hashed", "#aa86c5", roundedTriNames[0]));
        } else {
          console.log("dont hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "#aa86c5")
              .attr("opacity", 0);
          areas_of_diagram.push(new Area(theId, "clear", "#aa86c5", roundedTriNames[0]));
        }
      }

      console.log(areas_of_diagram);

      // this is the function that will be called when the user clicks on a segment
      g.selectAll("path.segment").on("click", function () {
        const svg = d3.select(this);
        console.log(svg);
        console.log(svg.attr('id'));
        if (areas_of_diagram.find(e => e.id === svg.attr('id')).state === "hashed"){
          let area = areas_of_diagram.find(e => e.id === svg.attr('id'))
          area.state = "clear";
          svg.transition().attr("fill", area.color);
        } else {
          areas_of_diagram.find(e => e.id === svg.attr('id')).state = "hashed"; // mark the area as hatched
          if (svg.attr('id') === "Universum") {
            svg.transition().attr("fill", "url(#universumHatch)");
          } else {
            svg.transition().attr("fill", "url(#diagonalHatch)");
          }
        }
      });

      var tooltip = d3.select("body")
          .append("div")
          .style("position", "absolute")
          .style("z-index", "10")
          .style("visibility", "hidden")
          .style("background-color", "rgb(54, 54, 54)")
          .style("padding", ".8rem");

      var vis = d3.select("body").append("svg:svg")
          .attr("width", 0)
          .attr("height", 0);

      // hover over a segment and get its description
      g.selectAll("path.segment").on("mousemove", function (event) {
        const svg = d3.select(this);
        tooltip.text("ID plochy: " + svg.attr('id'));
        tooltip.style("visibility", "visible");
        tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");
        svg.style("", "url(#drop-shadow)");
      });

      g.selectAll("path.segment").on("mouseout", function (event) {
        tooltip.style("visibility", "hidden");
        const svg = d3.select(this);
      });

      g.append("text")
          .text("Ω")
          .attr("x", (this.width - 30))
          .attr("y", 50)
          .style('fill', '#323232')
          .style('font-size', '1.5rem');

      g.append("text")
          .text(this.sets[0])
          .attr("x", centerX_1 - vennRadius)
          .attr("y", centerY_1 - vennRadius*0.8)
          .style('fill', '#323232');

      g.append("text")
          .text(this.sets[1])
          .attr("x", centerX_2 + vennRadius)
          .attr("y", centerY_2 - vennRadius*0.8)
          .style('fill', '#323232');

      g.append("text")
          .text(this.sets[2])
          .attr("x", centerX_3)
          .attr("y", centerY_3 + vennRadius*1.3)
          .style('fill', '#323232');

            // add the text labels
            g.append("text")
                .text("1")
                .attr("x", x_intersect_1)
                .attr("y", y_intersect_1)
                .style('fill', 'white')

            g.append("text")
                .text("2")
                .attr("x", x_intersect_2)
                .attr("y", y_intersect_2)
                .style('fill', 'white')


            g.append("text")
                .text("3")
                .attr("x", x_intersect_3)
                .attr("y", y_intersect_3)
                .style('fill', 'white')


            g.append("text")
                .text("4")
                .attr("x", x_intersect_4)
                .attr("y", y_intersect_4)
                .style('fill', 'white')


            g.append("text")
                .text("5")
                .attr("x", x_intersect_5)
                .attr("y", y_intersect_5)
                .style('fill', 'white')


            g.append("text")
                .text("6")
                .attr("x", x_intersect_6)
                .attr("y", y_intersect_6)
                .style('fill', 'white')

            g.append("text")
                .text("7")
                .attr("x", x_intersect_7)
                .attr("y", y_intersect_7)
                .style('fill', 'white')


            g.append("text")
                .text("8")
                .attr("x", x_intersect_8)
                .attr("y", y_intersect_8)
                .style('fill', 'white')
            g.append("text")
                .text("9")
                .attr("x", x_intersect_9)
                .attr("y", y_intersect_9)
                .style('fill', 'white')
            g.append("text")
                .text("10")
                .attr("x", x_intersect_10)
                .attr("y", y_intersect_10)
                .style('fill', 'white')
            g.append("text")
                .text("11")
                .attr("x", x_intersect_11)
                .attr("y", y_intersect_11)
                .style('fill', 'white')
            g.append("text")
                .text("12")
                .attr("x", x_intersect_12)
                .attr("y", y_intersect_12)
                .style('fill', 'white')

      g.append("text").text("?").attr("x", centerX_1).attr("y", centerY_1)
          .style('fill', 'white');

    }
  },
  // called when the component is created and inserted into the DOM
  mounted: function () {
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
        console.log("no type specified");
    }
    console.log("created venn of size " + this.vennSize);
  },
};
</script>