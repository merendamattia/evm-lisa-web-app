const addressField = document.getElementById("address");
const bytecodeField = document.getElementById("bytecode");

const error_alert = document.querySelector('#error-alert');
const message_error_alert = document.querySelector('#message-error-alert');

let bb = []

document.getElementById('form-analyses').addEventListener("submit", function(event) {
    event.preventDefault();

    button_run_spinner.style.display = "block";
    button_run.setAttribute("disabled", true);

    const params = {
        address: addressField.value, 
        bytecode: bytecodeField.value 
    };

    fetch("/run-command", {
        method: "POST",
        headers: {
            "Content-Type": "application/json", 
        },
        body: JSON.stringify(params),
    })
    .then(function(response) {
        if (!response.ok) {
            throw new Error(`Errore nella risposta del server: ${response.statusText}`);
        }
        return response.json();
    })
    .then(function(data) {
        console.log(data['basic-blocks']['basic_blocks']);
       bb = data['basic-blocks']['basic_blocks'];
       renderCFG(data['basic-blocks']['basic_blocks'])
    })
    .catch(function(error) {
        console.error("Errore durante la richiesta:", error);

        if (error.response) {
            error.response.json().then(function(errorData) {
                message_error_alert.textContent = errorData.error || "Si è verificato un errore";
            });
        } else {
            message_error_alert.textContent = error.message || "Si è verificato un errore sconosciuto";
        }

        error_alert.style.display = 'block';
    })
    .finally(function() {
        button_run_spinner.style.display = "none";
        button_run.removeAttribute("disabled");
    });
});

function renderCFG (bb) {

    const editor = new Drawflow(document.getElementById("drawflow"));
    editor.start();
    editor.editor_mode = 'edit'
    editor.reroute = true;
    editor.reroute_fix_curvature = true;

    const data = {
        name: ''
    };

    //editor.addNode(name, inputs, outputs, posx, posy, class, data, html);

    let bb_list = [];

    bb.forEach(element => {
        bb_list.push(
            new BasicBlock(
                element['background-color'],
                element.id,
                element['ingoing-edge-color'],
                element.instructions,
                element['lastInstruction'],
                element.outgoingEdges
            )
        );
    });

    console.log(bb_list);

    bb_list.forEach(element => {

        console.log(element)

        editor.addNode(
            element.id,
            1,
            element.get_outgoing_edges_number(),
            100,
            200, 
            'outgoing',
            data, 
            'ciao'
        )

        console.log('nodo aggiunto')
    });

}

/* 


editor.addNode('foo', 1, 1, 100, 200, 'foo', data, 'Foo');
editor.addNode('bar', 1, 1, 400, 100, 'bar', data, 'Bar A');
editor.addNode('bar', 1, 1, 400, 300, 'bar', data, 'Bar B');
editor.addConnection(1, 2, "output_1", "input_1");
editor.addConnection(1, 3, "output_1", "input_1");

*/
