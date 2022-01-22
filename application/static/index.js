// little script to delete note from list
function deleteNote(noteId) {// take this noteId
  fetch("/delete-note", {//send to this endpoint
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {//get result
    window.location.href = "/wall";//update page to home page aka refresh
  });
}

// script to add a new button to upload body images
var id = 1;
var newinput = function() {
  var parent = document.getElementById("body_img_div");
  var field = document.createElement("input");
  field.id = "img" + id;
  field.type = "file";
  // field.style = "display:block;";
  field.className = "form-control";
  field.name = "body_imgs";
  field.accept = ".jpg,.png,.gif";
  var label = document.createElement("label");
  label.setAttribute = ("for", "img" + id);
  label.innerHTML= id + " : ";
  div = document.createElement("div");
  div.id = "img" + id + "div";
  parent.appendChild(document.createElement("BR"));
  div.appendChild(label);
  div.appendChild(field);
  parent.appendChild(div);
  id += 1;
}

// function hideAlert() {
//   setTimeout(function(){$("#alert").hide()}, 300);
// }

// $("#alert").fadeTo(2000, 500).slideUp(500, function(){
//     $("#alert").slideUp(500);
// });

// $("#alert").delay(4000).slideUp(200, function() {
//     $(this).alert('close');
// });

// $(document).ready(function() {
//     // show the alert
//     setTimeout(function() {
//         $("alert").alert('close');
//     }, 2000);
// });

// $(".alert-dismissible").fadeTo(2000, 500).slideUp(500, function(){
//     $(".alert-dismissible").alert('close');
// });