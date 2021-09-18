var a = [];
a.push(JSON.parse(localStorage.getItem('note')));
localStorage.setItem('note', JSON.stringify(a));

document.addEventListener('DOMContentLoaded', function() {  

    let one_note = document.querySelectorAll('.note');


    one_note.forEach(one_note => {
        one_note.onclick = function() {
            let note = one_note.dataset.note_id;
            note_menu(note);
        }
    })
})

function note_menu(note) {
    edit = document.getElementById(note);
    is_form = document.getElementById(`edit-form-${note}`)
    if (is_form) {
        return;
    }
    var note_div = document.getElementById(`note-${note}`);
    var note_div_text = document.getElementById(`note-${note}-text`);
    var div_button_container = document.getElementById(`button-container-${note}`);
    // This part of the if-else shows the note text
    if(edit) {
        div_button_container.style.visibility = "hidden";
        div_button_container.style.height = 0;
        note_div_text.style.visibility = "visible";
        note_div_text.style.height = 250;
        div_button_container.innerHTML = "";
    // This part of the if-else shows the buttons
    } else {
        note_div_text.style.visibility = "hidden"
        note_div_text.style.height = 0
        div_button_container.style.visibility = "visible"
        div_button_container.style.height = 50

        var edit_button = document.createElement("button");
        edit_button.textContent = "Edit";
        edit_button.classList.add("note_edit_button");
        edit_button.id = note;

        var errase_button = document.createElement("button")
        errase_button.textContent = "Errase"
        errase_button.classList.add("note_errase_button");
        errase_button.id = note;

        div_button_container.appendChild(edit_button);
        div_button_container.appendChild(errase_button);

        edit_button.onclick = function() {
            note_div_text.style.visibility = "hidden";
            note_div_text.style.height = 0;
            div_button_container.style.visibility = "hidden";
            div_button_container.style.height = 0;
            edit_note(edit_button.id, note_div_text.textContent)
        }
      
        errase_button.onclick = function() {
            errase_note(errase_button.id)
        }
    
    }



}

function errase_note(note) {
    console.log("the errase button is working");
    fetch(`/delete/${note}`)
    .then(response => response.json())
    .then(email => {
        var note_div = document.getElementById(`note-${note}`);
        note_div.remove()
    });
}

function edit_note(note, note_text) {
    var note_div = document.getElementById(`note-${note}`);
    var edit_form = document.createElement('form');
    edit_form.setAttribute("method", "post");
    edit_form.setAttribute("action", `edit/${note}/`);
    edit_form.setAttribute("id", `edit-form-${note}`)
    edit_form.setAttribute("class", "edit_form_class")

    var input_form = document.createElement('textarea');
    input_form.innerHTML = note_text;
    input_form.setAttribute("type", "text");
    input_form.setAttribute("class", "edit_text_note");
    edit_form.appendChild(input_form)

    var submit_button = document.createElement("input");
    submit_button.setAttribute("type", "button");
    submit_button.setAttribute("value", "Submit");
    submit_button.setAttribute("class", "note_submit_button")
    edit_form.appendChild(submit_button)

    console.log("the edit button is working");
    note_div.appendChild(edit_form)

    submit_button.onclick = function () {
        console.log("the errase button is working");
        new_note_text = input_form.value;
        fetch(`/edit/${note}/`, {
            method:"POST",
            headers:{
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                note_id: note,
                new_text: new_note_text,
            }),

        })
        .then(response => response.json())
        .then(response => {
            note_div.removeChild(edit_form)
            var note_div_text = document.getElementById(`note-${note}-text`);
            note_div_text.textContent = new_note_text;
            note_menu(note);
        });
    }
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');