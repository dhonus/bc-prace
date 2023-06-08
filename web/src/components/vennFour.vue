<script>
import Area from "@/components/Area";
import * as d3 from "d3";
import d3Element from "@/components/d3Element";

export default {
  name: "vennFour",
  methods: {
    venn4: function(){
      let g = this.prepare();

      // center of first circle
      let centerX_1 = 190;
      let centerY_1 = 150;
      const vennRadius = 110;

      const factor = 1.10;
      const offset = factor * vennRadius;
      // center of second circle
      let centerX_2 = centerX_1 + offset;
      let centerY_2 = centerY_1; //creating new var for clarity
      // center of third circle
      const centerX_3 = centerX_1;
      const centerY_3 = centerY_1 + vennRadius*1.3/2;
      // center of fourth circle
      const centerX_4 = centerX_1 + vennRadius*1.5/2;
      const centerY_4 = centerY_1;

      this.areas_of_diagram.push(this.universum_hatch_check(g));

      let rect1__ = g.append("rect").attr("x", centerX_1 - vennRadius).attr("y", centerY_1 - vennRadius).attr("width", vennRadius*3.6).attr("height", vennRadius*1.3)
          .attr("class", "circle-background-white");
      let rect2__ = g.append("rect").attr("x", centerX_1 - vennRadius).attr("y", centerY_1 - vennRadius).attr("height", vennRadius*3).attr("width", vennRadius * 1.5)
          .attr("class", "circle-background-white");
      let rect3__ = g.append("rect").attr("x", centerX_3 - vennRadius).attr("y", centerY_3 - vennRadius).attr("width", vennRadius*3).attr("height", vennRadius*1.3)
          .attr("class", "circle-background-white");
      let rect4__ = g.append("rect").attr("x", centerX_4 - vennRadius).attr("y", centerY_4 - vennRadius).attr("height", vennRadius*2.6).attr("width", vennRadius*1.5)
          .attr("class", "circle-background-white");

      let rect1_ = g.append("rect").attr("x", centerX_1 - vennRadius).attr("y", centerY_1 - vennRadius).attr("width", vennRadius*3.6).attr("height", vennRadius*1.3)
          .attr("class", "circle-background");
      let rect2_ = g.append("rect").attr("x", centerX_1 - vennRadius).attr("y", centerY_1 - vennRadius).attr("height", vennRadius*3).attr("width", vennRadius * 1.5)
          .attr("class", "circle-background");
      let rect3_ = g.append("rect").attr("x", centerX_3 - vennRadius).attr("y", centerY_3 - vennRadius).attr("width", vennRadius*3).attr("height", vennRadius*1.3)
          .attr("class", "circle-background");
      let rect4_ = g.append("rect").attr("x", centerX_4 - vennRadius).attr("y", centerY_4 - vennRadius).attr("height", vennRadius*2.6).attr("width", vennRadius*1.5)
          .attr("class", "circle-background");


      let rect1 = g.append("rect").attr("x", centerX_1 - vennRadius).attr("y", centerY_1 - vennRadius).attr("width", vennRadius*3.6).attr("height", vennRadius*1.3)
          .attr("class", "circle");
      let rect2 = g.append("rect").attr("x", centerX_1 - vennRadius).attr("y", centerY_1 - vennRadius).attr("height", vennRadius*3).attr("width", vennRadius * 1.5)
          .attr("class", "circle");
      let rect3 = g.append("rect").attr("x", centerX_3 - vennRadius).attr("y", centerY_3 - vennRadius).attr("width", vennRadius*3).attr("height", vennRadius*1.3)
          .attr("class", "circle");
      let rect4 = g.append("rect").attr("x", centerX_4 - vennRadius).attr("y", centerY_4 - vennRadius).attr("height", vennRadius*2.6).attr("width", vennRadius*1.5)
          .attr("class", "circle");

      let center = {"x": centerX_1 - vennRadius * 1.2, "y": centerY_1-vennRadius};

      let origin = {"x": centerX_1 - vennRadius, "y": centerY_1-vennRadius};
      const x_intersect_1 = origin["x"];
      const y_intersect_1 = origin["y"]
      console.log(center)

      // this looks more complicated than it is.
      const row_2_X = origin["x"] + vennRadius*3*1.5/2 - vennRadius*1.5;

      const x_intersect_2 = origin["x"] + vennRadius* 3.6;
      const y_intersect_2 = origin["y"];

      const x_intersect_3 = origin["x"];
      const y_intersect_3 = origin["y"] + vennRadius*1.3;

      const x_intersect_4 = origin["x"] + vennRadius*3.6;
      const y_intersect_4 = origin["y"] + vennRadius*1.3;

      const x_intersect_5 = origin["x"] + vennRadius*1.5;
      const y_intersect_5 = origin["y"];

      const x_intersect_6 = origin["x"];
      const y_intersect_6 = origin["y"] + vennRadius*3;

      const x_intersect_7 = origin["x"] + vennRadius*1.5;
      const y_intersect_7 = origin["y"] + vennRadius*3;

      const x_intersect_8 = origin["x"] + vennRadius*3;
      const y_intersect_8 = origin["y"] + vennRadius*1.3;

      const x_intersect_9 = origin["x"] + vennRadius*1.5;
      const y_intersect_9 = origin["y"] + vennRadius*2.6;

      const x_intersect_10 = origin["x"] + vennRadius*3*1.5/2;
      const y_intersect_10 = origin["y"];

      const x_intersect_11 = origin["x"] + vennRadius*3*1.5/2;
      const y_intersect_11 = origin["y"] + vennRadius*1.3;

      const x_intersect_12 = origin["x"] + vennRadius*3*1.5/2;
      const y_intersect_12 = origin["y"] + vennRadius*2.6;

      const x_intersect_13 = row_2_X
      const y_intersect_13 = origin["y"] + vennRadius*1.3;

      const x_intersect_14 = row_2_X;
      const y_intersect_14 = origin["y"];

      const x_intersect_15 = centerX_3 - vennRadius;
      const y_intersect_15 = centerY_3 - vennRadius;

      const x_intersect_16 = row_2_X;
      const y_intersect_16 = centerY_3 - vennRadius;

      const x_intersect_17 = origin["x"] + vennRadius*1.5;
      const y_intersect_17 = centerY_3 - vennRadius;

      const x_intersect_18 = origin["x"] + vennRadius*3*1.5/2;
      const y_intersect_18 = centerY_3 - vennRadius;

      const x_intersect_19 = origin["x"] + vennRadius*1.5;
      const y_intersect_19 = origin["y"] + vennRadius*1.3;

      const x_intersect_20 = origin["x"] + vennRadius*3;
      const y_intersect_20 = centerY_3 - vennRadius;

      const x_intersect_21 = origin["x"];
      const y_intersect_21 = centerY_3 - vennRadius + vennRadius*1.3;

      const x_intersect_22 = row_2_X;
      const y_intersect_22 = centerY_3 - vennRadius + vennRadius*1.3;

      const x_intersect_23 = origin["x"] + vennRadius*1.5;
      const y_intersect_23 = centerY_3 - vennRadius + vennRadius*1.3;

      const x_intersect_24 = origin["x"] + vennRadius*3*1.5/2;
      const y_intersect_24 = centerY_3 - vennRadius + vennRadius*1.3;

      const x_intersect_25 = row_2_X;
      const y_intersect_25 = origin["y"] + vennRadius*2.6;

      const x_intersect_26 = origin["x"] + vennRadius*3;
      const y_intersect_26 = centerY_3 - vennRadius + vennRadius*1.3;

      let xPoints = [x_intersect_1, x_intersect_2, x_intersect_3, x_intersect_4, x_intersect_5, x_intersect_6, x_intersect_7, x_intersect_8, x_intersect_9, x_intersect_10, x_intersect_11, x_intersect_12, x_intersect_13, x_intersect_14, x_intersect_15, x_intersect_16, x_intersect_17, x_intersect_18, x_intersect_19, x_intersect_20, x_intersect_21, x_intersect_22, x_intersect_23, x_intersect_24, x_intersect_25, x_intersect_26];
      let yPoints = [y_intersect_1, y_intersect_2, y_intersect_3, y_intersect_4, y_intersect_5, y_intersect_6, y_intersect_7, y_intersect_8, y_intersect_9, y_intersect_10, y_intersect_11, y_intersect_12, y_intersect_13, y_intersect_14, y_intersect_15, y_intersect_16, y_intersect_17, y_intersect_18, y_intersect_19, y_intersect_20, y_intersect_21, y_intersect_22, y_intersect_23, y_intersect_24, y_intersect_25, y_intersect_26];

      let squareAreas = [
        [1, 14, 15, 16], //
        [14, 5, 16, 17], //
        [5, 10, 17, 18], //
        [15, 16, 3, 13], //
        [16, 17, 13, 19], //
        [17, 18, 19, 11], //
        [3, 13, 21, 22], //
        [13, 19, 22, 23], //
        [19, 11, 23, 24],
        [22, 23, 25, 9],
        [23, 24, 9, 12],
        [18, 20, 11, 8],
        [11, 8, 24, 26]
      ];

      let squareNames = [
        [this.sets[0], this.sets[1]].sort(),//
        [this.sets[0], this.sets[1], this.sets[3]].sort(), //
        [this.sets[0], this.sets[3]].sort(), //
        [this.sets[0], this.sets[1], this.sets[2]].sort(),//
        [this.sets[0], this.sets[1], this.sets[2], this.sets[3]].sort(), //
        [this.sets[0], this.sets[2], this.sets[3]].sort(),//
        [this.sets[1], this.sets[2]].sort(), //
        [this.sets[1], this.sets[2], this.sets[3]].sort(), //
        [this.sets[2], this.sets[3]].sort(),
        [this.sets[1], this.sets[3]].sort(),
        [this.sets[3]].sort(),
        [this.sets[0], this.sets[2]].sort(),
        [this.sets[2]].sort(),
      ];

      let fills = [
          "#9f9f9f",
          "#6c6c6c",
          "#9f9f9f",
          "#6c6c6c",
          "#565656",
          "#6c6c6c",
          "#9f9f9f",
          "#6c6c6c",
          "#9f9f9f",
          "#9f9f9f",
          "#cccccc",
          "#9f9f9f",
          "#cccccc",
      ]

      const l_areas = [
        [10, 2, 4, 8, 20, 18],
        [21, 6, 7, 9, 25, 22]
      ]
      const l_names = [
        [this.sets[0]],
        [this.sets[1]]
      ]

      console.log(squareNames.length, squareAreas.length)

      const compareArrays = (arr1, arr2) => {
        return arr1.length === arr2.length && arr1.every((val, index) => val === arr2[index]);
      }

      console.log("our universal friends are ", this.universal)
      console.log("the things are", squareNames)
      // find common
      let hash_these = squareNames.filter((arr) => {
        return this.universal.some((arr2) => {
          return compareArrays(arr, arr2);
        });
      });

      console.log(hash_these, "hash these");

       const intersectionOfTwoArea = ([x2, x1, x3, x4, y1, y2, y3, y4]) => {
        return `M ${x1} ${y1} L ${x2} ${y2} L ${x3} ${y3} L ${x4} ${y4} Z`;
      };

       const createLShapePath = ([x1, x2, x3, x4, x5, x6, y1, y2, y3, y4, y5, y6]) => {
           console.log("creating L shape path", x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6)
          return `M ${x1} ${y1} L ${x2} ${y2} L ${x3} ${y3} L ${x4} ${y4} L ${x5} ${y5} L ${x6} ${y6} Z`;
       };

      // three functions to iterate over points and append paths
      let i = 0;
      for (const points of squareAreas) {
        const ptCycle = points
            .map((i) => xPoints[i - 1])
            .concat(points.map((i) => yPoints[i - 1]));
        const shape = intersectionOfTwoArea(ptCycle);
        const theId = String(points[0]) + String(points[1]) + String(points[2]);

        // if points is contained in hash_these
        if (hash_these.some((arr) => {
          return compareArrays(arr, squareNames[i]);
        })) {
          // they are the same, so we need to hatch it
          g.append("path")
              .attr("id", theId)
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "url(#diagonalHatch)")
              .attr("opacity", 0.8);
          this.areas_of_diagram.push(new Area(theId, "hashed", fills[i], squareNames[i]));
        } else {
          g.append("path")
              .attr("id", theId)
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", fills[i])
              .attr("opacity", 0.5);
          this.areas_of_diagram.push(new Area(theId, "clear", fills[i], squareNames[i]));
        }
        i++;
      }

      // find more hatchable areas
      hash_these = l_names.filter((arr) => {
        return this.universal.some((arr2) => {
          return compareArrays(arr, arr2);
        });
      });

      // three functions to iterate over points and append paths
      i = 0;
      for (const points of l_areas) {
        const ptCycle = points
            .map((i) => xPoints[i - 1])
            .concat(points.map((i) => yPoints[i - 1]));
        const shape = createLShapePath(ptCycle);
        const theId = String(points[0]) + String(points[1]) + String(points[2] + String(points[3]) + String(points[4]) + String(points[5]));

        // if points is contained in hash_these
        if (hash_these.some((arr) => {
          return compareArrays(arr, l_names[i]);
        })) {
          // they are the same, so we need to hatch it
          g.append("path")
              .attr("id", theId)
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "url(#diagonalHatch)")
              .attr("opacity", 0.8);
          this.areas_of_diagram.push(new Area(theId, "hashed", "#cccccc", l_names[i]));
        } else {
          g.append("path")
              .attr("id", theId)
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "#cccccc")
              .attr("opacity", 0.5);
          this.areas_of_diagram.push(new Area(theId, "clear", "#cccccc", l_names[i]));
        }
        i++;
      }

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

      var tooltip = d3.select("body")
          .append("div")
          .style("position", "absolute")
          .style("z-index", "10")
          .style("visibility", "hidden")
          .style("background-color", "rgb(54, 54, 54)")
          .style("padding", ".8rem");

      const vis = d3.select("body").append("svg:svg")
          .attr("width", 0)
          .attr("height", 0);

      g.selectAll("path.segment").on("mouseout", function (event) {
        tooltip.style("visibility", "hidden");
        const svg = d3.select(this);
      });

      let __sets_identifiers = [
        [this.sets[0]],
        [this.sets[1]],
        [this.sets[2]],
        [this.sets[3]],
        ["Ω"],

        [this.sets[0], this.sets[1]],
        [this.sets[0], this.sets[2]],
        [this.sets[2], this.sets[3]],
        [this.sets[1], this.sets[3]],
        [this.sets[1], this.sets[2]],
        [this.sets[0], this.sets[3]],

        [this.sets[0], this.sets[1], this.sets[2]],
        [this.sets[0], this.sets[1], this.sets[3]],
        [this.sets[0], this.sets[2], this.sets[3]],
        [this.sets[1], this.sets[2], this.sets[3]],

        [this.sets[0], this.sets[1], this.sets[2], this.sets[3]],
      ];

      // positions as [x, y]; corresponds to __sets_identifiers
      let __sets_positions = [
        [x_intersect_10 + vennRadius*1.2, y_intersect_2 + 40],
        [x_intersect_6 + vennRadius/2, y_intersect_25 + 10],
        [x_intersect_11 + vennRadius/2 + 8, y_intersect_8 + 45],
        [x_intersect_23 + vennRadius/2 + 8, y_intersect_24 + 40],
        [centerX_1 + 300, centerY_1 + 150],

        [origin["x"] + 60, origin["y"] + 45],
        [x_intersect_18 + vennRadius/2 + 8, y_intersect_20 + 45],
        [x_intersect_19 + vennRadius/2 + 8, y_intersect_11 + 45],
        [x_intersect_22 + vennRadius/2 + 8, y_intersect_23 + 45],
        [x_intersect_3 + vennRadius/2 + 8, y_intersect_13 + 45],
        [x_intersect_5 + vennRadius/2 + 8, y_intersect_10 + 45],

        [x_intersect_15 + vennRadius/2 + 8, y_intersect_16 + 45],
        [x_intersect_14 + vennRadius/2 + 8, y_intersect_5 + 45],
        [x_intersect_17 + vennRadius/2 + 8, y_intersect_18 + 45],
        [x_intersect_13 + vennRadius/2 + 8, y_intersect_19 + 45],

        [x_intersect_16 + vennRadius/2 + 8, y_intersect_17 + 45],
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
              } else {
                position_me(position, key, "x");
              }
            }
          }
        }
      }


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
/*
      g.append("text")
          .text("1")
          .attr("x", x_intersect_1)
          .attr("y", y_intersect_1)
          .style('fill', '#323232');
      g.append("text")
          .text("2")
          .attr("x", x_intersect_2)
          .attr("y", y_intersect_2)
          .style('fill', '#323232');
      g.append("text")
          .text("3")
          .attr("x", x_intersect_3)
          .attr("y", y_intersect_3)
          .style('fill', '#323232');
      g.append("text")
          .text("4")
          .attr("x", x_intersect_4)
          .attr("y", y_intersect_4)
          .style('fill', '#323232');
      g.append("text")
          .text("5")
          .attr("x", x_intersect_5)
          .attr("y", y_intersect_5)
          .style('fill', '#323232');
      g.append("text")
          .text("6")
          .attr("x", x_intersect_6)
          .attr("y", y_intersect_6)
          .style('fill', '#323232');
      g.append("text")
          .text("7")
          .attr("x", x_intersect_7)
          .attr("y", y_intersect_7)
          .style('fill', '#323232');
      g.append("text")
          .text("8")
          .attr("x", x_intersect_8)
          .attr("y", y_intersect_8)
          .style('fill', '#323232');
      g.append("text")
          .text("9")
          .attr("x", x_intersect_9)
          .attr("y", y_intersect_9)
          .style('fill', '#323232');
      g.append("text")
          .text("10")
          .attr("x", x_intersect_10)
          .attr("y", y_intersect_10)
          .style('fill', '#323232');
      g.append("text")
          .text("11")
          .attr("x", x_intersect_11)
          .attr("y", y_intersect_11)
          .style('fill', '#323232');
      g.append("text")
          .text("12")
          .attr("x", x_intersect_12)
          .attr("y", y_intersect_12)
          .style('fill', '#323232');

      g.append("text")
          .text("13")
          .attr("x", x_intersect_13)
          .attr("y", y_intersect_13)
          .style('fill', '#323232');

      g.append("text")
          .text("14")
          .attr("x", x_intersect_14)
          .attr("y", y_intersect_14)
          .style('fill', '#323232');
      g.append("text")
          .text("15")
          .attr("x", x_intersect_15)
          .attr("y", y_intersect_15)
          .style('fill', '#323232');
      g.append("text")
          .text("16")
          .attr("x", x_intersect_16)
          .attr("y", y_intersect_16)
          .style('fill', '#323232');
      g.append("text")
          .text("17")
          .attr("x", x_intersect_17)
          .attr("y", y_intersect_17)
          .style('fill', '#323232');
      g.append("text")
          .text("18")
          .attr("x", x_intersect_18)
          .attr("y", y_intersect_18)
          .style('fill', '#323232');
      g.append("text")
          .text("19")
          .attr("x", x_intersect_19)
          .attr("y", y_intersect_19)
          .style('fill', '#323232');
      g.append("text")
          .text("20")
          .attr("x", x_intersect_20)
          .attr("y", y_intersect_20)
          .style('fill', '#323232');
      g.append("text")
          .text("21")
          .attr("x", x_intersect_21)
          .attr("y", y_intersect_21)
          .style('fill', '#323232');
      g.append("text")
          .text("24")
          .attr("x", x_intersect_24)
          .attr("y", y_intersect_24)
          .style('fill', '#323232');
      g.append("text")
          .text("22")
          .attr("x", x_intersect_22)
          .attr("y", y_intersect_22)
          .style('fill', '#323232');
      g.append("text")
          .text("23")
          .attr("x", x_intersect_23)
          .attr("y", y_intersect_23)
          .style('fill', '#323232');

      g.append("text")
          .text("25")
          .attr("x", x_intersect_25)
          .attr("y", y_intersect_25)
          .style('fill', '#323232');
      g.append("text")
          .text("26")
          .attr("x", x_intersect_26)
          .attr("y", y_intersect_26)
          .style('fill', '#323232');
*/
      g.append("text")
          .text(this.sets[0] + "'")
          .attr("x", origin["x"] + vennRadius*3.7)
          .attr("y", centerY_1 - vennRadius*0.76)
          .style('fill', '#323232');

      g.append("text")
          .text(this.sets[1] + "'")
          .attr("x", origin["x"] + vennRadius*1.6)
          .attr("y", centerY_1 + vennRadius*1.85)
          .style('fill', '#323232');

      g.append("text")
          .text(this.sets[2] + "'")
          .attr("x", centerX_2 + vennRadius-2)
          .attr("y", centerY_4 + vennRadius * 0.5)
          .style('fill', '#323232');
      g.append("text")
          .text(this.sets[3] + "'")
          .attr("x", centerX_2 + vennRadius * 0.2)
          .attr("y", centerY_4 + vennRadius * 1.15)
          .style('fill', '#323232');

    }
  },
}
</script>
