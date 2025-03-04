type Edge = { id: string }; 

export default class BasicBlock {
    label:string;
    background_color: string;
    id: string;
    ingoing_edge_color: string;
    instructions: string[];
    last_instruction: string;
    outgoing_edges: Edge[];

    constructor(
        label:string,
        background_color: string,
        id: string,
        ingoing_edge_color: string,
        instructions: string[],
        last_instruction: string,
        outgoing_edges: Edge[]
    ) {
        this.label = label;
        this.background_color = background_color;
        this.id = id;
        this.ingoing_edge_color = ingoing_edge_color;
        this.instructions = instructions;
        this.last_instruction = last_instruction;
        this.outgoing_edges = outgoing_edges;
    }

    get_outgoing_edges_number(): number {
        return this.outgoing_edges.length;
    }
}
