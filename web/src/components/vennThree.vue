
<script>
import Area from "@/components/Area";
import * as d3 from "d3";
import d3Element from "@/components/d3Element";

export default {
  name: "vennThree",
  methods: {
    venn3: function(thisInstanceWillActAsUserInput, area_combinations){
      let g = this.prepare();
      // center of first circle
      const centerX_1 = 220;
      const centerY_1 = 145;
      const vennRadius = 100;

      const factor = 1.26;
      const offset = factor * vennRadius;
      // center of second circle
      const centerX_2 = centerX_1 + offset;
      const centerY_2 = centerY_1; //creating new var for clarity
      // center of third circle
      const centerX_3 = centerX_1 + offset / 2;
      const centerY_3 = centerY_1 + (Math.sqrt(3) * offset) / 2;

      this.areas_of_diagram.push(this.universum_hatch_check(g, !thisInstanceWillActAsUserInput));

      let keys = {};
      for (let key in this.counts) {
          for (let value in this.counts[key]) {
              if (keys[this.counts[key][value]] === undefined) {
                  keys[this.counts[key][value]] = [];
              }
              keys[this.counts[key][value]].push(key);
          }
      }

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

      const xDelta = (generalHeight * Math.sqrt(3)) / 2;
      const yDelta = generalHeight / 2;

      const xMidpointC1C3 = (centerX_1 + centerX_3) / 2;
      const xMidpointC2C3 = (centerX_2 + centerX_3) / 2;
      const yMidpointBoth = (centerY_1 + centerY_3) / 2;

      const x_intersect_1 = centerX_3;
      const y_intersect_1 = centerY_1 - generalHeight;

      const x_intersect_2 = xMidpointC1C3 - xDelta;
      const y_intersect_2 = yMidpointBoth + yDelta;

      const x_intersect_3 = xMidpointC2C3 + xDelta;
      const y_intersect_3 = yMidpointBoth + yDelta;

      const x_intersect_4 = centerX_3;
      const y_intersect_4 = centerY_1 + generalHeight;

      const x_intersect_5 = xMidpointC1C3 + xDelta;
      const y_intersect_5 = yMidpointBoth - yDelta;

      const x_intersect_6 = xMidpointC2C3 - xDelta;
      const y_intersect_6 = yMidpointBoth - yDelta;

      let xPoints = [x_intersect_1, x_intersect_2, x_intersect_3, x_intersect_4, x_intersect_5, x_intersect_6];
      let yPoints = [y_intersect_1, y_intersect_2, y_intersect_3, y_intersect_4, y_intersect_5, y_intersect_6];

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

      console.log(this.keys, "keeys")

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
          const arr = keys[ironPointsNames[i].join(",")];
          for (let value in arr) {
              if (document.getElementById("diagonalHatch-" + ironPointsNames[i] + arr[value]) !== null){
                  g.append("path")
                    .attr("id", theId)
                    .attr("name", ironPointsNames[i])
                    .attr("d", shape)
                    .attr("class", "segment")
                    .attr("fill", "url(#diagonalHatch-" + ironPointsNames[i] + arr[value] +")")
                    .attr("opacity", 0.4);
                  continue;
              }
              let pattern = g.append("pattern").attr("id", "diagonalHatch-" + ironPointsNames[i] + arr[value]).attr("patternUnits", "userSpaceOnUse").attr("width", 12).attr("height", 12);
              pattern.append("path").attr("d", "M-3,3 l6,-6 M0,12 l12,-12 M9,15 l6,-6").attr("style", "stroke: #3f3f3f; stroke-width: 1.2px;")
              // add some spacing to the stroke
              pattern.attr("patternTransform", "rotate("+ arr[value] * 45 +" 0 0)")

              g.append("path")
                    .attr("id", theId)
                    .attr("name", ironPointsNames[i])
                    .attr("d", shape)
                    .attr("class", "segment")
                    .attr("fill", "url(#diagonalHatch-" + ironPointsNames[i] + arr[value] +")")
                    .attr("opacity", 0.4);
          }
          this.areas_of_diagram.push(new Area(theId, "hashed", ironFill, ironPointsNames[i]));
        } else {
          console.log("dont hatch it");
          g.append("path")
              .attr("id", theId)
              .attr("name", ironPointsNames[i])
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", ironFill)
              .attr("opacity", 0.4);
          this.areas_of_diagram.push(new Area(theId, "clear", ironFill, ironPointsNames[i]));
        }
        i++;
      }

      // find common
      hash_these = sunPointsNames.filter((arr) => {
        return this.universal.some((arr2) => {
          return compareArrays(arr, arr2);
        });
      });

      i = 0;
      let sunFill = "#e2e2e2";
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
          const arr = keys[sunPointsNames[i].join(",")];
          for (let value in arr) {
              if (document.getElementById("diagonalHatch-" + sunPointsNames[i] + arr[value]) !== null){
                  g.append("path")
                    .attr("id", theId)
                    .attr("name", sunPointsNames[i])
                    .attr("d", shape)
                    .attr("class", "segment")
                    .attr("fill", "url(#diagonalHatch-" + sunPointsNames[i]  + arr[value] +")")
                    .attr("opacity", 0.4);
                  continue;
              }
              let pattern = g.append("pattern").attr("id", "diagonalHatch-" + sunPointsNames[i] + arr[value]).attr("patternUnits", "userSpaceOnUse").attr("width", 12).attr("height", 12);
              pattern.append("path").attr("d", "M-3,3 l6,-6 M0,12 l12,-12 M9,15 l6,-6").attr("style", "stroke: #3f3f3f; stroke-width: 1.2px;")
              pattern.attr("patternTransform", "rotate("+ arr[value] * 45 +" 0 0)")

              g.append("path")
                    .attr("id", theId)
                    .attr("name", sunPointsNames[i])
                    .attr("d", shape)
                    .attr("class", "segment")
                    .attr("fill", "url(#diagonalHatch-" + sunPointsNames[i] + arr[value] +")")
                    .attr("opacity", 0.4);
          }
          this.areas_of_diagram.push(new Area(theId, "hashed", sunFill, sunPointsNames[i]));
        } else {
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("name", sunPointsNames[i])
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", sunFill)
              .attr("opacity", 1);
          this.areas_of_diagram.push(new Area(theId, "clear", sunFill, sunPointsNames[i]));
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
          const arr = keys[roundedTriNames[0].join(",")];
          for (let value in arr) {
              if (document.getElementById("diagonalHatch-" + roundedTriNames[0] + arr[value]) !== null){
                  g.append("path")
                    .attr("id", theId)
                    .attr("name", roundedTriNames[0])
                    .attr("d", shape)
                    .attr("class", "segment")
                    .attr("fill", "url(#diagonalHatch-" + roundedTriNames[0]  + arr[value] +")")
                    .attr("opacity", 0.4);
                  continue;
              }
              let pattern = g.append("pattern").attr("id", "diagonalHatch-" + roundedTriNames[0] + arr[value]).attr("patternUnits", "userSpaceOnUse").attr("width", 12).attr("height", 12);
              pattern.append("path").attr("d", "M-3,3 l6,-6 M0,12 l12,-12 M9,15 l6,-6").attr("style", "stroke: #3f3f3f; stroke-width: 1.2px;")
              pattern.attr("patternTransform", "rotate("+ arr[value] * 45 +" 0 0)")

              g.append("path")
                    .attr("id", theId)
                    .attr("name", roundedTriNames[0])
                    .attr("d", shape)
                    .attr("class", "segment")
                    .attr("fill", "url(#diagonalHatch-" + roundedTriNames[0] + arr[value] +")")
                    .attr("opacity", 0.4);
          }
          this.areas_of_diagram.push(new Area(theId, "hashed", "#929292", roundedTriNames[0]));
        } else {
          console.log("dont hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("name", roundedTriNames[0])
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "#929292")
              .attr("opacity", 1);
          this.areas_of_diagram.push(new Area(theId, "clear", "#929292", roundedTriNames[0]));
        }
      }

      console.log(this.areas_of_diagram);

      // this is the function that will be called when the user clicks on a segment
      g.selectAll("path.segment").on("click", (e) => {
        if (!this.thisInstanceWillActAsUserInput) {
          return;
        }
        const svg = d3.select(e.currentTarget)
        console.log(svg);
        console.log(svg.attr('id'));
        if (this.areas_of_diagram.find(e => e.id === svg.attr('id')).state === "hashed"){
          let area = this.areas_of_diagram.find(e => e.id === svg.attr('id'))
          area.state = "clear";
          svg.transition().attr("fill", area.color);
        } else {
          this.areas_of_diagram.find(e => e.id === svg.attr('id')).state = "hashed"; // mark the area as hatched
          if (svg.attr('id') === "Universum") {
            svg.transition().attr("fill", "url(#universumHatch)");
          } else {
            svg.transition().attr("fill", "url(#diagonalHatch)");
          }
        }
      });

      let tooltip = d3.select("body")
        .append("div")
        .attr("class", "bubble-thing")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("visibility", "hidden")
        .style("background-color", "rgb(54, 54, 54)")
        .style("padding", ".8rem");

      // hover over a segment and get its description
      g.selectAll("path.segment").on("mousemove", function (event) {
        const finding = (element) => element === svg.attr("name");
        const svg = d3.select(this);
        tooltip.text("Oblast: " + area_combinations.findIndex(finding));
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
        ["Ω"],

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
        [centerX_1 - 110, centerY_1 + 110],

        [centerX_3 + 20, centerY_2 - 20],
        [xMidpointC2C3 + 40, yMidpointBoth + 20],
        [xMidpointC1C3, yMidpointBoth + 20],

        [centerX_3 + 20, yMidpointBoth - 10],
      ]

      console.log(__sets_identifiers);

      let position_me = (index, key, character) => {
        const pos = __sets_positions[index];

        let el = new d3Element();
        el.index = index;

        // this is done because a single position can be taken by multiple "x"
        // it will produce something like x_x,y,z instead of just the last one. e.g. x_z
        if (key !== undefined){
          if (this.positioned[index] === undefined || this.positioned[index].length === 0) {
            this.positioned[index] = [];
            this.positioned[index].push(key);
          } else {
            this.positioned[index].push(key);
          }
        } else if (this.positioned[index].length === 0){
          return el;
        }

        console.log(index, "pos, key, index");
        // background for the text
        el.circle = g.append("circle");
        el.circle
            .attr("r", 14 + this.positioned[index].length * 3)
            .attr("transform", "translate(" + (pos[0] - 20) + "," + (pos[1] - 10) + ")")
            .attr("class", character === "?" ? "question-background" : "set-background")
        // the "X" or "?"
        el.text = g.append("text");
        el.text
            .text(character)
            .attr("x", pos[0] - (character === "?" ? 27 : 28) - (this.positioned[index].length -1)*4)
            .attr("y", pos[1] - 5)
            .style('fill', '#323232')
            .attr("class", character === "?" ? "question-text" : "set-text")
            .style('font-size', '1.2rem');
        // the variable
        el.var = g.append("text");
        el.var
            .text(character === "?" ? key : this.positioned[index])
            .attr("x", pos[0] - (character === "?" ? 18 : 18) - (this.positioned[index].length -1)*4)
            .attr("y", pos[1] - 1)
            .style('fill', '#323232')
            .attr("class", character === "?" ? "question-text" : "set-text")
            .style('font-size', '.8rem');

        if (character === "?"){
          this.positioned[index].pop();
        }
        return el;
      }

      // existential
      console.log(this.existential, "existential");
      for (const position in __sets_identifiers){
        for(let key in this.existential) {
          console.log("the size is: " + this.existential[key].length);

          for (let all in this.existential[key]) {
            if (compareArrays(this.existential[key][all], __sets_identifiers[position])) {
              console.log(this.existential[key][all], __sets_identifiers[position]);
              console.log("bad", this.bad);
              // if this.existential[key][any] is in bad[key] then it is a bad existential
              if (this.bad[key] !== undefined && this.bad[key].length > 0){
                for (let bad in this.bad[key]){
                  if (compareArrays(this.bad[key][bad], this.existential[key][all])){
                    position_me(position, key, "?");
                  }
                }
              }  else if (this.emptyDict(this.bad)){
                position_me(position, key, "x");
              }
            }
          }
        }
      }

      console.log(this.existential instanceof Array)

      //user added areas
      let user_added_areas = {};
      let wipe = (index) => {
        return this.wipe(index);
      };

      // this is the function that will be called when the user clicks on a segment
      g.selectAll("path.segment").on("contextmenu", (e) => {
        const svg = d3.select(e.currentTarget)
        console.log(svg);
        console.log(svg.attr('id'));

        let theVar = this.entryVariable;
        if (theVar === undefined || theVar === null || theVar.length === 0){
          theVar = "x";
        }
        // check if theVar is a lowercase letter
        if (theVar.length !== 1 || !theVar.match(/[a-z]/i)){
          // set class of ref
          this.$refs.entryVariableInput.classList.add("bad");
          theVar = "x"
          this.entryVariable = "x";
        } else {
          this.$refs.entryVariableInput.classList.remove("bad");
        }
        let area = this.areas_of_diagram.find(e => e.id === svg.attr('id'));


        let found = false;
        if (area.questionElement.index !== -1)
          for (let i = 0; i < this.positioned[area.questionElement.index].length; i++){
            if (this.positioned[area.questionElement.index][i] === theVar){
              this.positioned[area.questionElement.index].splice(i, 1);
              found = true;
            }
          }

        if (area.questionElement.circle !== null){
          try {
            area.questionElement.circle.remove();
            area.questionElement.text.remove();
            area.questionElement.var.remove();
          } catch (e) {
            console.log(e);
          }
        }

        let i = 0;
        for (const ass in __sets_identifiers){
          console.log(ass);
          if (compareArrays(__sets_identifiers[ass], area.assignment)){
            console.log("found it at index: " + i);
            area.questionElement = position_me(i, found ? undefined : theVar, "x");
            if (found){
              // remove theVar from the existential
              for (let j = 0; j < area.existential.length; j++){
                if (area.existential[j] === theVar){
                  area.existential.splice(j, 1);
                }
              }
            } else {
              area.existential.push(theVar);
            }
          }
          i++;
        }

        console.log(this.areas_of_diagram, " <- has been modified and our friend is ");
      });


      g.append("text")
          .text("Ω")
          .attr("x", (this.width - 30))
          .attr("y", 50)
          .style('fill', '#323232')
          .style('font-size', '1.5rem');

      g.append("text")
          .text(this.sets[0] + "'")
          .attr("x", centerX_1 - vennRadius)
          .attr("y", centerY_1 - vennRadius*0.8)
          .style('fill', '#323232');

      g.append("text")
          .text(this.sets[1] + "'")
          .attr("x", centerX_2 + vennRadius)
          .attr("y", centerY_2 - vennRadius*0.8)
          .style('fill', '#323232');

      g.append("text")
          .text(this.sets[2] + "'")
          .attr("x", centerX_3)
          .attr("y", centerY_3 + vennRadius*1.2)
          .style('fill', '#323232');
    },
  }
}
</script>
