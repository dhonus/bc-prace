import d3Element from "@/components/d3Element";
export default class Area {
    constructor(id, state, color, assignment) {
        this.id = id;
        this.state = state; // clear | hashed | questioning
        this.color = color;
        this.comment = "";
        // this corresponds to the areas we get from the API.
        // Hardcoded in each of the venn functions because the API doesn't return the areas of the same name every time
        this.assignment = assignment;
        this.question = false;
        this.variable = "";
        this.questionElement = new d3Element(); // this is the actual d3 element that we use to draw the question mark
        this.existential = [];
    }
}