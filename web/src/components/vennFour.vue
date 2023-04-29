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
      const centerX_1 = 220;
      const centerY_1 = 150;
      const vennRadius = 100;

      const factor = 1.10;
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

      this.areas_of_diagram.push(this.universum_hatch_check(g));

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
      const triHeight = Math.sqrt(vennRadius**2 - (offset / 2)**2)
      const xDelta = (generalHeight * Math.sqrt(3)) / 2;
      const yDelta = triHeight;

      //https://cs.wikibooks.org/wiki/Geometrie/Numerick%C3%BD_v%C3%BDpo%C4%8Det_pr%C5%AFniku_dvou_kru%C5%BEnic
      const getCenter = (firstX, secondX, firstY, secondY, flip) => {
        let d = Math.sqrt((firstX - secondX) ** 2 + (firstY - secondY) ** 2);
        let sx = firstX  + ((d/2)/d)*(secondX - firstX);
        let sy = firstY  + ((d/2)/d)*(secondY - firstY);
        let m = d/2;
        let v = Math.sqrt((vennRadius ** 2) - (m) ** 2);
        if (flip)
          return {
            "x": (sx + (v/d)*(firstY - secondY)),
            "y": (sy - (v/d)*(firstX - secondX))
          }
        else
          return {
            "x": (sx - (v/d)*(firstY - secondY)),
            "y": (sy + (v/d)*(firstX - secondX))
          }
      }

      let center;
      const xMidpointC1C3 = (centerX_1 + centerX_3) / 2;
      const xMidpointC2C3 = (centerX_2 + centerX_3) / 2;
      const yMidpointBoth = (centerY_1 + centerY_2) / 2;

      center = getCenter(centerX_1, centerX_2, centerY_1, centerY_2, false);
      const x_intersect_1 = center["x"];
      const y_intersect_1 = center["y"];

      center = getCenter(centerX_1, centerX_3, centerY_1, centerY_3, true);
      const x_intersect_2 = center["x"];
      const y_intersect_2 = center["y"];

      center = getCenter(centerX_4, centerX_3, centerY_4, centerY_3, false);
      const x_intersect_3 = center["x"];
      const y_intersect_3 = center["y"];

      center = getCenter(centerX_4, centerX_2, centerY_4, centerY_2, true);
      const x_intersect_4 = center["x"];
      const y_intersect_4 = center["y"];

      center = getCenter(centerX_3, centerX_2, centerY_3, centerY_2, false);
      const x_intersect_5 = center["x"];
      const y_intersect_5 = center["y"];

      center = getCenter(centerX_1, centerX_4, centerY_1, centerY_4, false);
      const x_intersect_6 = center["x"];
      const y_intersect_6 = center["y"];

      center = getCenter(centerX_2, centerX_3, centerY_2, centerY_3, false);
      const x_intersect_7 = center["x"];
      const y_intersect_7 = center["y"];

      center = getCenter(centerX_1, centerX_4, centerY_1, centerY_4, true);
      const x_intersect_8 = center["x"];
      const y_intersect_8 = center["y"];

      center = getCenter(centerX_2, centerX_4, centerY_2, centerY_4, true);
      const x_intersect_9 = center["x"];
      const y_intersect_9 = center["y"];

      center = getCenter(centerX_1, centerX_3, centerY_1, centerY_3, false);
      const x_intersect_10 = center["x"];
      const y_intersect_10 = center["y"];

      center = getCenter(centerX_3, centerX_4, centerY_3, centerY_4, false);
      const x_intersect_11 = center["x"];
      const y_intersect_11 = center["y"];

      center = getCenter(centerX_1, centerX_2, centerY_1, centerY_2, true);
      const x_intersect_12 = center["x"];
      const y_intersect_12 = center["y"];


      let xPoints = [x_intersect_1, x_intersect_2, x_intersect_3, x_intersect_4, x_intersect_5, x_intersect_6, x_intersect_7, x_intersect_8, x_intersect_9, x_intersect_10, x_intersect_11, x_intersect_12];
      let yPoints = [y_intersect_1, y_intersect_2, y_intersect_3, y_intersect_4, y_intersect_5, y_intersect_6, y_intersect_7, y_intersect_8, y_intersect_9, y_intersect_10, y_intersect_11, y_intersect_12];


      // three functions to create the paths using the points of intersection
      const intersectionOfTwoArea = ([x1, x2, x3, x4, y1, y2, y3, y4]) => {
        let path = `M ${x1} ${y1}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x2} ${y2}
             A ${vennRadius} ${vennRadius} 0 0 0 ${x3} ${y3}
             A ${vennRadius} ${vennRadius} 0 0 0 ${x4} ${y4}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x1} ${y1}`;
        return path;
      };

      const singleSetArea = ([x1, x2, x3, y1, y2, y3]) => {
        let path = `M ${x1} ${y1}
             A ${vennRadius} ${vennRadius} 0 0 0 ${x2} ${y2}
             A ${vennRadius} ${vennRadius} 0 0 0 ${x3} ${y3}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x1} ${y1}`;
        return path;
      };

      const intersectionOfThreeArea = ([x1, x2, x3, y1, y2, y3]) => {
        let path = `M ${x1} ${y1}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x2} ${y2}
             A ${vennRadius} ${vennRadius} 0 0 0 ${x3} ${y3}
             A ${vennRadius} ${vennRadius} 0 0 1 ${x1} ${y1}`;
        return path;
      };
      const intersectionOfFourArea = ([x1, x2, x3, x4, y1, y2, y3, y4]) => {
        let path = `M ${x1} ${y1}
             A ${vennRadius} ${vennRadius} 0 0 0 ${x2} ${y2}
             A ${vennRadius} ${vennRadius} 0 0 0 ${x4} ${y4}
             A ${vennRadius} ${vennRadius} 0 0 0 ${x3} ${y3}
             A ${vennRadius} ${vennRadius} 0 0 0 ${x1} ${y1}`;
        return path;
      };

      let twoSetAreas = [
        [1, 6, 11, 5],
        [2, 5, 9, 8],
        [3, 8, 12, 7],
        [4, 7, 10, 6],
      ];
      let twoSetAreasNames = [
        [this.sets[0], this.sets[1]].sort(),
        [this.sets[0], this.sets[2]].sort(),
        [this.sets[2], this.sets[3]].sort(),
        [this.sets[1], this.sets[3]].sort(),
      ]
      let singleSetAreas = [
        [4, 6, 1],
        [2, 8, 3],
        [1, 5, 2],
        [3, 7, 4],
      ];
      let singleSetAreaNames = [
        [this.sets[1]],
        [this.sets[2]],
        [this.sets[0]],
        [this.sets[3]],
      ]
      let intersectionOfThreeAreas = [
        [5, 11, 9],
        [8, 9, 12],
        [7, 12, 10],
        [6, 10, 11],
      ];
      let intersectionOfThreeAreasNames = [
        [this.sets[0], this.sets[1], this.sets[2]].sort(),
        [this.sets[0], this.sets[2], this.sets[3]].sort(),
        [this.sets[1], this.sets[2], this.sets[3]].sort(),
        [this.sets[0], this.sets[1], this.sets[3]].sort(),
      ]
      let intersectionOfFourAreas = [
        [10, 11, 12, 9],
      ];
      let intersectionOfFourAreasNames = [
        [this.sets[0], this.sets[1], this.sets[2], this.sets[3]].sort(),
      ]

      const compareArrays = (arr1, arr2) => {
        return arr1.length === arr2.length && arr1.every((val, index) => val === arr2[index]);
      }

      console.log("our universal friends are ", this.universal)
      console.log("the things are", twoSetAreasNames)
      // find common
      let hash_these = twoSetAreasNames.filter((arr) => {
        return this.universal.some((arr2) => {
          return compareArrays(arr, arr2);
        });
      });

      console.log(hash_these, "hash these");

      // three functions to iterate over points and append paths
      let i = 0;
      let ironFill = "#9f9f9f";
      for (const points of twoSetAreas) {
        const ptCycle = points
            .map((i) => xPoints[i - 1])
            .concat(points.map((i) => yPoints[i - 1]));
        const shape = intersectionOfTwoArea(ptCycle);
        const theId = String(points[0]) + String(points[1]) + String(points[2]);

        // if points is contained in hash_these
        if (hash_these.some((arr) => {
          return compareArrays(arr, twoSetAreasNames[i]);
        })) {
          // they are the same, so we need to hatch it
          g.append("path")
              .attr("id", theId)
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "url(#diagonalHatch)")
              .attr("opacity", 0.8);
          this.areas_of_diagram.push(new Area(theId, "hashed", ironFill, twoSetAreasNames[i]));
        } else {
          g.append("path")
              .attr("id", theId)
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", ironFill)
              .attr("opacity", 0.8);
          this.areas_of_diagram.push(new Area(theId, "clear", ironFill, twoSetAreasNames[i]));
        }
        i++;
      }

      // find common
      hash_these = singleSetAreaNames.filter((arr) => {
        return this.universal.some((arr2) => {
          return compareArrays(arr, arr2);
        });
      });
      console.log(hash_these, "hash these");

      i = 0;
      let sunFill = "#e2e2e2";
      for (const points of singleSetAreas) {
        const ptCycle = points
            .map((i) => xPoints[i - 1])
            .concat(points.map((i) => yPoints[i - 1]));
        const shape = singleSetArea(ptCycle);
        const theId = String(points[0]) + String(points[1]) + String(points[2]);

        // if points is contained in hash_these
        if (hash_these.some((arr) => {
          return compareArrays(arr, singleSetAreaNames[i]);
        })) {
          // they are the same, so we need to hatch it
          console.log("hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "url(#diagonalHatch)")
              .attr("opacity", 1);
          this.areas_of_diagram.push(new Area(theId, "hashed", sunFill, singleSetAreaNames[i]));
        } else {
          console.log("dont hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", sunFill)
              .attr("opacity", 1);
          this.areas_of_diagram.push(new Area(theId, "clear", sunFill, singleSetAreaNames[i]));
        }
        i++;
      }

      i = 0;
      // find common
      hash_these = intersectionOfThreeAreasNames.filter((arr) => {
        return this.universal.some((arr2) => {
          return compareArrays(arr, arr2);
        });
      });
      console.log(hash_these, "hash these !");

      for (const points of intersectionOfThreeAreas) {
        const ptCycle = points
            .map((i) => xPoints[i - 1])
            .concat(points.map((i) => yPoints[i - 1]));
        const shape = intersectionOfThreeArea(ptCycle);
        const theId = String(points[0]) + String(points[1]) + String(points[2]);

        // if points is contained in hash_these
        if (hash_these.some((arr) => {
          return compareArrays(arr, intersectionOfThreeAreasNames[i]);
        })) {
          // they are the same, so we need to hatch it
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "url(#diagonalHatch)")
              .attr("opacity", 0.8);
          this.areas_of_diagram.push(new Area(theId, "hashed", "#868585", intersectionOfThreeAreasNames[i]));
        } else {
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "#868585")
              .attr("opacity", 0.8);
          this.areas_of_diagram.push(new Area(theId, "clear", "#868585", intersectionOfThreeAreasNames[i]));
        }
        i++;
      }

      for (const points of intersectionOfFourAreas) {
        const ptCycle = points
            .map((i) => xPoints[i - 1])
            .concat(points.map((i) => yPoints[i - 1]));
        const shape = intersectionOfFourArea(ptCycle);
        const theId = String(points[0]) + String(points[1]) + String(points[2]) + String(points[3]);

        // if points is contained in hash_these
        if (hash_these.some((arr) => {
          return compareArrays(arr, intersectionOfFourAreasNames[0]);
        })) {
          // they are the same, so we need to hatch it
          console.log("hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]) + String(points[3]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "url(#diagonalHatch)")
              .attr("opacity", 0.8);
          this.areas_of_diagram.push(new Area(theId, "hashed", "#626262", intersectionOfFourAreasNames[0]));
        } else {
          console.log("dont hatch it");
          g.append("path")
              .attr("id", String(points[0]) + String(points[1]) + String(points[2]) + String(points[3]))
              .attr("d", shape)
              .attr("class", "segment")
              .attr("fill", "#626262")
              .attr("opacity", 0.8);
          this.areas_of_diagram.push(new Area(theId, "clear", "#626262", intersectionOfFourAreasNames[0]));
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
      /*g.selectAll("path.segment").on("mousemove", function (event) {
        const svg = d3.select(this);
        tooltip.text("ID plochy: " + svg.attr('id'));
        tooltip.style("visibility", "visible");
        tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");
        svg.style("", "url(#drop-shadow)");
      });*/

      g.selectAll("path.segment").on("mouseout", function (event) {
        tooltip.style("visibility", "hidden");
        const svg = d3.select(this);
      });

      let __sets_identifiers = [
        [this.sets[0]],
        [this.sets[1]],
        [this.sets[2]],
        [this.sets[3]],

        [this.sets[0], this.sets[1]],
        [this.sets[0], this.sets[2]],
        [this.sets[2], this.sets[3]],
        [this.sets[1], this.sets[3]],

        [this.sets[0], this.sets[1], this.sets[2]],
        [this.sets[0], this.sets[1], this.sets[3]],
        [this.sets[0], this.sets[2], this.sets[3]],
        [this.sets[1], this.sets[2], this.sets[3]],

        [this.sets[0], this.sets[1], this.sets[2], this.sets[3]],
      ];

      // positions as [x, y]; corresponds to __sets_identifiers
      let __sets_positions = [
        [centerX_1, centerY_1 - 40],
        [centerX_2 + 40, centerY_1 - 40],
        [centerX_3, centerY_3 + 60],
        [centerX_4 + 40, centerY_4 + 60],

        [x_intersect_1 + 20, centerY_2 - 20],
        [x_intersect_2 + 60, y_intersect_2 + 8],
        [x_intersect_1 + 20, y_intersect_3 - 40],
        [x_intersect_4 - 40, y_intersect_2 + 8],

        [x_intersect_9 + 25, y_intersect_9 - 22],
        [x_intersect_6 + 3, y_intersect_11 + 13],
        [x_intersect_8 + 37, y_intersect_8 - 10],
        [x_intersect_6 + 3, y_intersect_8 - 10],

        [x_intersect_1 + 20, y_intersect_9 + 8],
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
          .attr("x", centerX_1 - vennRadius)
          .attr("y", centerY_3 + vennRadius)
          .style('fill', '#323232');
      g.append("text")
          .text(this.sets[3] + "'")
          .attr("x", centerX_2 + vennRadius)
          .attr("y", centerY_4 + vennRadius)
          .style('fill', '#323232');

    }
  },
}
</script>
