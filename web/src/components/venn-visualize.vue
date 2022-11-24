<!-- https://axios-http.com/docs/post_example -->

<template>
  <div class="canvasControls">
    <div class="left">
      <p>Funkce diagramu:</p>
      <p id="canvasMessage">zpráva</p>
    </div>
    <div class="right">
      <div class="canvasButton" id="empty" @click="activate('empty')">
        <img src="../assets/icons/empty.svg" title="Vyprázdnit">
      </div>
      <div class="canvasButton" id="question" @click="activate('question')">
        <img src="../assets/icons/iconmonstr-question-thin.svg" title="Přidat otazník">
      </div>
      <div class="canvasButton" id="hatched" @click="activate('hatched')">
        <img src="../assets/icons/hashed.svg" title="Vyšrafovat">
      </div>
    </div>
  </div>
  <div class="canvasWrapper">
    <svg width="500" height="400" id="canvas"></svg>
  </div>
</template>

<script>
import * as d3 from 'd3'

export default {
  name: 'vennVisualizer',
  props: {
    vennSize: Number
  },
  data() {
    return {
      msg: '',
      currentModifierButton: null
    };
  },
  methods: {
    // sets the current active button to the one that was clicked on
    activate: function(button){
      if(this.currentModifierButton !== null){
        document.getElementById(this.currentModifierButton).classList.remove('activeCanvasControls');
      }
      document.getElementById(button).classList.add('activeCanvasControls');
      this.currentModifierButton = button;
    },
    // this creates the venn diagram
    venn3: function(){
      console.log(this.vennSize);
      console.log("venn");
      class Area {
        constructor(id, state, color) {
          this.id = id;
          this.state = state; // clear | hashed | questioning
          this.color = color;
          this.comment = "";
        }
      }

      let svg = d3.select("#canvas");

      const margin = {
        top: 0,
        right: 20,
        bottom: 30,
        left: 40,
      };
      //const width = svg.attr("width") - margin.left - margin.right;
      //const height = +svg.attr("height") - margin.top - margin.bottom;

      // add hatching pattern to svg
      let pattern = svg.append("pattern").attr("id", "diagonalHatch").attr("patternUnits", "userSpaceOnUse").attr("width", 8).attr("height", 8);
      pattern.append("path").attr("d", "M-2,2 l4,-4 M0,8 l8,-8 M6,10 l4,-4").attr("style", "stroke: #000; stroke-width: 2px");

      const g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
      console.log(g);

      // center of first circle
      const centerX_1 = 150;
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
      let sunPoints = [
        [3, 5, 1],
        [2, 4, 3],
        [1, 6, 2],
      ];
      let roundedTriPoints = [[5, 4, 6]];

      let areas_of_diagram = [];
      
      // three functions to iterate over points and append paths
      for (const points of ironPoints) {
        const ptCycle = points
            .map((i) => xPoints[i - 1])
            .concat(points.map((i) => yPoints[i - 1]));
        const shape = intersectionOfTwoArea(ptCycle);
        const theId = String(points[0]) + String(points[1]) + String(points[2]);

        g.append("path")
            .attr("id", theId)
            .attr("d", shape)
            .attr("class", "segment")
            .attr("fill", "#9f9f9f")
            .attr("opacity", 0.4);
        areas_of_diagram.push(new Area(theId, "clear", "#9f9f9f"));
      }

      for (const points of sunPoints) {
        const ptCycle = points
            .map((i) => xPoints[i - 1])
            .concat(points.map((i) => yPoints[i - 1]));
        const shape = singleSetArea(ptCycle);
        const theId = String(points[0]) + String(points[1]) + String(points[2]);

        g.append("path")
            .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
            .attr("d", shape)
            .attr("class", "segment")
            .attr("fill", "#2d2d2d")
            .attr("opacity", 0.4);
        areas_of_diagram.push(new Area(theId, "clear", "#2d2d2d"));
      }

      for (const points of roundedTriPoints) {
        const ptCycle = points
            .map((i) => xPoints[i - 1])
            .concat(points.map((i) => yPoints[i - 1]));
        const shape = intersectionOfThreeArea(ptCycle);
        const theId = String(points[0]) + String(points[1]) + String(points[2]);

        g.append("path")
            .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
            .attr("d", shape)
            .attr("class", "segment")
            .attr("fill", "#aa86c5")
            .attr("opacity", 0.4);
        areas_of_diagram.push(new Area(theId, "clear", "#aa86c5"));
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
          areas_of_diagram.find(e => e.id === svg.attr('id')).state = "hashed";
          svg.transition().attr("fill", "url(#diagonalHatch)");
        }
        console.log(areas_of_diagram);
      });

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

      g.append("text").text("?").attr("x", centerX_1).attr("y", centerY_1)
          .style('fill', 'white');

    }
  },
  // called when the component is created and inserted into the DOM
  mounted: function () {
    this.venn3();
    console.log("created");
  },
};
</script>