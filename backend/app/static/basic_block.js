class BasicBlock {

    constructor (background_color, id, ingoing_edge_color, instructions, last_instruction, outgoing_edges) {

        this.background_color=background_color;
        this.id=id;
        this.ingoing_edge_color=ingoing_edge_color;
        this.instructions=instructions;
        this.last_instruction=last_instruction;
        this.outgoing_edges=outgoing_edges;

    }

    get_outgoing_edges_number(){
        if (typeof this.outgoing_edges !== "undefined") {
            return this.outgoing_edges.length;
        }

        return 0;
    }

}