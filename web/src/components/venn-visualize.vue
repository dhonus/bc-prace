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
  <div class="canvasWrapper">
    <svg width="600" height="400" ref="canvas"></svg>
  </div>
</template>

<script>
import * as d3 from 'd3'

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
      currentModifierButton: null
    };
  },
  methods: {
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
    // this creates the venn diagram
    venn3: function(){
      console.log(this.vennSize);
      console.log("venn");

      console.log(this.universal, "universal");

      this.msg = 'Velikost: ' + this.vennSize;
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

      let svg = d3.select(this.$refs.canvas);

      const margin = {
        top: 0,
        right: 20,
        bottom: 30,
        left: 20,
      };
      const width = svg.attr("width") - margin.left - margin.right;
      const height = +svg.attr("height") - margin.top - margin.bottom;

      // add hatching pattern to svg
      let pattern = svg.append("pattern").attr("id", "diagonalHatch").attr("patternUnits", "userSpaceOnUse").attr("width", 8).attr("height", 8);
      pattern.append("path").attr("d", "M-2,2 l4,-4 M0,8 l8,-8 M6,10 l4,-4").attr("style", "stroke: #000; stroke-width: 2px");

      const g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
      console.log(g);

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

      // add square to svg
      let universum = g.append("rect")
        .attr("x", 0)
        .attr("y", 20)
        .attr("width", width)
        .attr("height", height)
        .attr("fill", "none")
        .attr("stroke", "#9782ae");


      // add circles to svg
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

      let areas_of_diagram = [];

      const compareArrays = (arr1, arr2) => {
        return arr1.length === arr2.length && arr1.every((val, index) => val === arr2[index]);
      }

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
              .attr("opacity", 0.3);
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
              .attr("opacity", 0.6);
          areas_of_diagram.push(new Area(theId, "hashed", sunFill, sunPointsNames[i]));
        } else {
          console.log("dont hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", sunFill)
              .attr("opacity", 0.6);
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
              .attr("opacity", 0.8);
          areas_of_diagram.push(new Area(theId, "hashed", "#aa86c5", roundedTriNames[0]));
        } else {
          console.log("dont hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "#aa86c5")
              .attr("opacity", 0.8);
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
          areas_of_diagram.find(e => e.id === svg.attr('id')).state = "hashed";
          svg.transition().attr("fill", "url(#diagonalHatch)");
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
          .attr("x", (width - 30))
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
      g.append("text").text("?").attr("x", centerX_1).attr("y", centerY_1)
          .style('fill', 'white');

    }
  },
  // called when the component is created and inserted into the DOM
  mounted: function () {
    switch (this.vennSize) {
      case 1:
        break;
      case 2:
        break;
      case 3:
        this.venn3();
        break;
      case 4:
        break;
      default:
        console.log("no type specified");
    }
    console.log("created venn of size " + this.vennSize);
  },
};
</script>