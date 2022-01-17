// little script to delete note from list
function deleteNote(noteId) {// take this noteId
  fetch("/delete-note", {//send to this endpoint
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {//get result
    window.location.href = "/wall";//update page to home page aka refresh
  });
}